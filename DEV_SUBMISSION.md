---
title: "ReplyBuddy: the right words, still yours"
published: false
tags: devchallenge, weekendchallenge, hf26challenge
---

*This is a submission for the [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01).*

## What I built

ReplyBuddy is a small, local-first AI writing buddy for a friend who sometimes knows what they mean but gets stuck finding the right words. Paste a message, choose a tone, and get three concise replies to choose from. Add a few examples of how you normally text and it will use them as a style guide.

**Demo:** [Add a public demo URL or a short screen recording before publishing.]

**Code:** [Add the public repository URL before publishing.]

## The person behind the problem

I started with one real person: [describe your friend in a way they are comfortable sharing]. They told me that [add their actual words or a specific, true example of the problem]. I wanted to make a tool for that small moment—not another general-purpose chatbot.

I showed them the finished project and asked what felt useful, what felt off, and whether they would use it. **Their feedback:** [add their actual response after you ask them; don't invent a quote].

## How it works

The React interface sends the message, selected tone, optional context, and optional writing examples to a small FastAPI backend. The backend asks Ollama to run the open-weight Gemma 3 1B model on this computer and validates a structured set of three replies. The app has no account, database, analytics, or hosted AI API.

## Why open AI mattered here

A message to a friend can be personal. Running inference locally means the text does not need to be sent to a cloud AI provider; after the model is downloaded, generation can happen without an internet connection. The model is replaceable through one environment setting, so people can choose a model that fits their machine or preferences. Ollama is open source, and Gemma is an openly available set of model weights under Google's terms—this is an open-weight approach, not a claim that every model component uses an OSI-approved license.

## What I learned / what I'd improve

[Add what surprised you while building, one limitation you noticed when trying it with your friend, and what you would improve next. Be specific and honest.]

## Try it locally

See the setup instructions in the repository README. You need Node.js, Python, Ollama, and the Gemma 3 1B model. The first model download needs internet; inference runs locally afterward.

---

**Before publishing:** replace every bracketed placeholder with real details, ask your friend for consent before sharing their story or feedback, add a working demo/repository link or screenshots, change `published: false` to `published: true`, and verify the DEV submission template's required tags and dates. The challenge page lists the submission deadline as October 5, 2026 at 6:59 AM UTC (12:29 PM IST).
