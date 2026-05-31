# KARTRIX-BACKEND

Official DARTRIX Core Architecture blueprint.

## What this repository contains
- `main.py` — FastAPI command parser/executor
- `index.html` — lightweight frontend with fetch-based command actions
- `README.md` — blueprint and provider integration reference

## Run locally
```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

## API

### `POST /parse`
Parses raw text into a structured `Command`.

Example:
```json
{
  "text": "summarize the latest report"
}
```

### `POST /execute`
Executes a structured `Command`.

Example:
```json
{
  "command": {
    "action": "summarize",
    "target": "latest report",
    "args": {
      "raw": "summarize the latest report"
    },
    "provider": "gpt",
    "model": "gpt-4.1"
  }
}
```

## Integration reference

### Gemini
```python
from google import genai

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=command.args.get("raw", "")
)
```

### GPT
```python
from openai import OpenAI

client = OpenAI()
response = client.responses.create(
    model=command.model or "gpt-4.1",
    input=command.args.get("raw", "")
)
```

### Ollama
```python
import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": command.model or "llama3.1",
        "prompt": command.args.get("raw", ""),
        "stream": False,
    },
    timeout=60,
)
```

## Frontend flow
1. Enter a command in the text area.
2. Click Parse to send it to `/parse`.
3. Click Execute to send the structured `Command` to `/execute`.
4. Read the JSON response in the output panel.
