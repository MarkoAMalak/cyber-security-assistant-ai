# 🔐 Cyber Security Assistant AI

An AI-powered chat assistant for **cyber threat awareness and security guidance**,
built with Gradio and served by LLMs through the Groq API.

## Features

- Chat interface with conversation memory
- Choice of model (`llama-3.3-70b-versatile`, `llama-3.1-8b-instant`)
- Adjustable temperature and response length
- Cybersecurity-focused system prompt (threats, vulnerabilities, best practices, prevention)
- Starts cleanly even without an API key and shows a clear message instead of crashing

## Run locally

1. Get a free API key from https://console.groq.com/keys
2. Install and run:

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export GROQ_API_KEY="your_key_here"                   # Windows: set GROQ_API_KEY=your_key_here
python app.py
```

Open http://localhost:7860.

## Deploy to Hugging Face Spaces

Create a Gradio Space, upload `app.py` and `requirements.txt`, and add
`GROQ_API_KEY` under **Settings → Variables and secrets**.

## Tech stack

Python · Gradio · Groq API · Llama 3
