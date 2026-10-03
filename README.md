# ReplyBuddy 💬

**The right words, still yours.** ReplyBuddy helps someone who gets stuck on what to say write a natural message in their own voice. Paste a message, pick a tone, and get three replies from a local AI model. Add a few text examples to make the suggestions feel more like you.

> Built for a friend who sometimes knows what they want to say—but not quite how to phrase it.

This project was created for DEV's [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01). The challenge asks participants to build something for a real person, make open-source AI central to the project, and publish a DEV post with the story and a demo. The submission deadline listed on the challenge page is **October 5, 2026 at 6:59 AM UTC (12:29 PM IST)**.

## What it does

- Generates **three** message replies in one of six tones: Friendly, Casual, Professional, Funny, Caring, or Polite.
- Lets you optionally provide example texts and situation context to personalize the suggestions.
- Copies each reply with one click.
- Runs generation locally through **Ollama + Gemma 3 1B**. After downloading the model, inference works without an internet connection.
- Keeps the app small: no login, database, analytics, or hosted AI API.

## How the open AI fits

The model is the part that creates the replies—not a thin UI over a closed-model API. A React frontend talks to a small FastAPI backend, which asks Ollama to run the open-weight Gemma 3 1B model on your computer. This keeps message text on the device and lets you replace the model with another Ollama-compatible model. Ollama is open-source software; Gemma's weights are openly available under Google's terms, so this project describes its model as **open-weight** rather than claiming every component has an OSI-approved open-source license.

The first model download needs internet access. Once installed, reply generation is local. The app does not save conversations. Its interface uses system fonts and does not load third-party analytics or hosted AI services.

## Run locally (Windows PowerShell)

### Prerequisites

- Python 3.11 or newer
- Node.js 20.19+ or 22.12+
- [Ollama for Windows](https://ollama.com/download)

Install the model once:

```powershell
ollama pull gemma3:1b
```

### 1. Set up the Python environment

Run from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements-dev.txt
```

If PowerShell blocks virtual-environment activation, use `\.venv\Scripts\python.exe` in place of `python` in the remaining commands.

Optional: copy `backend\.env.example` to `backend\.env` to change the local Ollama URL or model. Defaults are `http://localhost:11434` and `gemma3:1b`.

### 2. Start the API

In a terminal at the repository root:

```powershell
python -m uvicorn main:app --app-dir backend --reload
```

The API runs at `http://127.0.0.1:8000`; interactive API docs are at `http://127.0.0.1:8000/docs`.

### 3. Start the frontend

In a second terminal:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

Open the local URL printed by Vite (usually `http://localhost:5173`). Keep Ollama running while generating replies. If you use another model, set `OLLAMA_MODEL` in `backend\.env` and download that model with `ollama pull <model-name>`.

## Verify

From the repository root, with the virtual environment activated:

```powershell
python -m pytest backend\tests
cd frontend
npm.cmd run build
```

## Project layout

```text
backend/
	main.py                 FastAPI endpoints and Ollama integration
	requirements.txt        Runtime dependencies
	tests/                  API, prompt, and input-validation tests
frontend/
	src/App.jsx              ReplyBuddy interface
	src/styles.css           Responsive styling
	src/lib/api.js            Frontend/API client
DEV_SUBMISSION.md          Hacktoberfest article draft and submission checklist
CHALLENGE_CHECKLIST.md     Project completion and remaining participant tasks
```

## Challenge story and submission

The challenge is about one real person, not just a feature list. Ask your friend whether this solves a real frustration, get permission before sharing anything personal, and add their **actual** feedback to [DEV_SUBMISSION.md](DEV_SUBMISSION.md). That draft intentionally contains placeholders rather than inventing a friend, a quote, or a test result. Before publishing, add the public repository and demo/screen recording links, then use the DEV challenge submission template and its required tags: `#devchallenge`, `#weekendchallenge`, and `#hf26challenge`.

## License

This project is released under the MIT License. Gemma model weights are subject to [Google's Gemma terms](https://ai.google.dev/gemma/terms); they are not relicensed by this repository.