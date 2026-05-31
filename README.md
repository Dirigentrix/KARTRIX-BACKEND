# KARTRIX-BACKEND

Official DARTRIX Core Architecture blueprint.

## What this repository contains
- `main.py` — FastAPI command parser/executor with S-NET state
- `snet.py` — SNetAgent safety and mode-switching layer
- `index.html` — lightweight frontend with fetch-based command actions and mode polling
- `README.md` — blueprint and provider integration reference

## Run locally
```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

## API

### `POST /parse`
Parses raw text into a structured `Command` and updates S-NET state.

Example:
```json
{
  "text": "summarize the latest report",
  "external_noise": 0.2,
  "internal_noise": 0.1,
  "anomaly_score": 0.1
}
```

### `POST /execute`
Executes a structured `Command` and returns the current S-NET state.

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

### `GET /state`
Returns the current broadcast S-NET snapshot:
- `alert_signal`
- `engine_mode`
- `ren12_override`
- `k12_gate`
- source noise fields

## S-NET logic
- `alert_signal = 0.4 * external_noise + 0.3 * internal_noise + 0.3 * anomaly_score`
- `intent_override == "alarm"` forces `alert_signal = 1.0`
- `engine_mode` thresholds:
  - `Flow` when `< 0.3`
  - `Alert` when `< 0.7`
  - `Stop` when `>= 0.7`
- `ren12_override` and `k12_gate` become `LOCKED` when `alert_signal > 0.7`

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
2. Click Parse to send it to `/parse` and refresh the current S-NET state.
3. Click Execute to send the structured `Command` to `/execute`.
4. The frontend polls `/state` so external dashboards can pick up `engine_mode`.
