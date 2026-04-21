---
title: Monotype Translation Crew
emoji: 🔤
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# Monotype Translation Crew

AI-powered translation tool built with CrewAI and FastAPI. Translates Excel files (.xlsx), PDFs, and Word documents (.docx) into French, German, Brazilian Portuguese, Japanese, and Latin American Spanish — guided by Monotype brand standards and approved terminology.

## Setup

Set the following **secrets** in your Space settings (Settings → Repository secrets):

| Secret | Description |
|--------|-------------|
| `OPENAI_API_KEY` | OpenAI API key used by CrewAI agents and batch translation |
| `MODEL` | Model to use, e.g. `openai/gpt-4.1-2025-04-14` |
