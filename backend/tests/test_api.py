import asyncio
import json

import httpx

import backend.main as api

RealAsyncClient = httpx.AsyncClient


def call_api(method, path, **kwargs):
    async def send_request():
        async with RealAsyncClient(
            transport=httpx.ASGITransport(app=api.app),
            base_url="http://testserver",
        ) as client:
            return await client.request(method, path, **kwargs)

    return asyncio.run(send_request())


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def install_ollama_mock(monkeypatch, models=None, generated=None):
    calls = []

    class FakeAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def get(self, url):
            return FakeResponse({"models": models or []})

        async def post(self, url, json):
            calls.append({"url": url, "payload": json})
            return FakeResponse({"response": generated or "{}"})

    monkeypatch.setattr(api.httpx, "AsyncClient", FakeAsyncClient)
    return calls


def test_health_requires_the_configured_model_tag(monkeypatch):
    install_ollama_mock(monkeypatch, models=[{"name": "gemma3:1b"}])

    response = call_api("GET", "/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "ok": True,
        "ollama_available": True,
        "model_ready": True,
        "model": api.OLLAMA_MODEL,
    }


def test_health_does_not_accept_a_different_model_size(monkeypatch):
    other_size = api.OLLAMA_MODEL.rsplit(":", 1)[0] + ":4b"
    install_ollama_mock(monkeypatch, models=[{"name": other_size}])

    response = call_api("GET", "/api/health")

    assert response.status_code == 200
    assert response.json()["ollama_available"] is True
    assert response.json()["model_ready"] is False


def test_generate_calls_ollama_and_returns_three_replies(monkeypatch):
    expected_replies = ["Sure, tonight works!", "Absolutely, I can send them tonight.", "Yep, I'll get them over by tonight."]
    calls = install_ollama_mock(
        monkeypatch,
        generated=json.dumps({"replies": expected_replies}),
    )

    response = call_api(
        "POST",
        "/api/generate",
        json={
            "message": "Can you send the files by tonight?",
            "tone": "Friendly",
            "style_examples": "suree, no worries",
            "context": "This is a friend.",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"replies": expected_replies, "model": api.OLLAMA_MODEL}
    assert len(calls) == 1
    assert calls[0]["url"] == f"{api.OLLAMA_BASE_URL}/api/generate"
    assert calls[0]["payload"]["model"] == api.OLLAMA_MODEL
    assert json.loads(calls[0]["payload"]["prompt"])["message"] == "Can you send the files by tonight?"
    assert "friendly tone" in calls[0]["payload"]["system"]


def test_generate_rejects_invalid_tone_before_calling_ollama():
    response = call_api(
        "POST",
        "/api/generate",
        json={"message": "Hi", "tone": "Aggressive"},
    )

    assert response.status_code == 422
