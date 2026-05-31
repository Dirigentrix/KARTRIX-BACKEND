from typing import Any, Dict, Literal, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="KARTRIX-BACKEND", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Command(BaseModel):
    action: str = Field(..., description="Primary command action")
    target: Optional[str] = Field(default=None, description="Optional target for the command")
    args: Dict[str, Any] = Field(default_factory=dict, description="Structured command arguments")
    provider: Optional[Literal["gemini", "gpt", "ollama"]] = Field(
        default=None,
        description="Preferred LLM provider",
    )
    model: Optional[str] = Field(default=None, description="Specific provider model name")


class ParseRequest(BaseModel):
    text: str
    provider: Optional[Literal["gemini", "gpt", "ollama"]] = None
    model: Optional[str] = None


class ExecuteRequest(BaseModel):
    command: Command


@app.get("/")
def root() -> Dict[str, str]:
    return {
        "name": "KARTRIX-BACKEND",
        "status": "ok",
        "blueprint": "DARTRIX Core Architecture",
    }


def parse_command_text(text: str, provider: Optional[str] = None, model: Optional[str] = None) -> Command:
    raw = text.strip()
    if not raw:
        return Command(action="noop", args={"raw": raw}, provider=provider, model=model)

    lowered = raw.lower()
    action = lowered.split()[0]
    target: Optional[str] = None

    for marker in (" for ", " on ", " to ", " into ", " at "):
        if marker in lowered:
            idx = lowered.index(marker)
            target = raw[idx + len(marker):].strip()
            break

    return Command(
        action=action,
        target=target,
        args={"raw": raw},
        provider=provider,
        model=model,
    )


@app.post("/parse", response_model=Command)
def parse(payload: ParseRequest) -> Command:
    return parse_command_text(payload.text, provider=payload.provider, model=payload.model)


@app.post("/execute")
def execute(payload: ExecuteRequest) -> Dict[str, Any]:
    command = payload.command
    result: Dict[str, Any] = {
        "status": "executed",
        "provider": command.provider or "local",
        "model": command.model,
        "command": command.model_dump(),
        "result": {
            "message": f"Executed action '{command.action}'",
            "target": command.target,
            "args": command.args,
        },
    }
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
