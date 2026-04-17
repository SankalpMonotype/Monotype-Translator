---
title: Monotype Translation Crew
emoji: 🌐
colorFrom: gray
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Monotype Translation Crew

AI-powered UI string translation into French, German, Portuguese (pt-BR), Japanese, and Latin American Spanish — guided by Monotype brand standards.

## Setup

Set the following **secrets** in your Space settings (Settings → Repository secrets):

| Secret | Description |
|--------|-------------|
| `OPENAI_API_KEY` | OpenAI API key used by CrewAI agents |

Any other environment variables your CrewAI config requires (e.g. `OPENAI_MODEL_NAME`) can also be added as secrets.
