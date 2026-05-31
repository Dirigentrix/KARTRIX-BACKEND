from typing import Any, Dict, Literal, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from snet import SNetAgent

app = FastAPI(title="KARTRIX-BACKEND", version="1.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

snet_agent = SNetAgent()


class Command(BaseModel):
    action: str = Field(..., description="Primary command action")
    target: Optional[str] = Field(default=None, description="Optional target for the command")
    args: Dict[str, Any] = Field(default_factory=dict, description="Structured command arguments")
    provider: Optional[Literal["gemini", "gpt", "ollama"]] = Field(
        default=None,
        description="Preferred LLM provider",
    )
    model: Optional[str] = Field(default=None, description="Specific provider model name")


class SNetFeedback(BaseModel):
    external_noise: Optional[float] = None
    internal_noise: Optional[float] = None
    anomaly_score: Optional[float] = None
    intent_override: Optional[str] = None
    ren12_status: Optional[str] = None
    k12_status: Optional[str] = None


class ParseRequest(SNetFeedback):
    text: str
    provider: Optional[Literal["gemini", "gpt", "ollama"]] = None
    model: Optional[str] = None


class ExecuteRequest(SNetFeedback):
    command: Command


class FeedbackRequest(SNetFeedback):
    pass


@app.get("/")
def root() -> Dict[str, str]:
    return {
        "name": "KARTRIX-BACKEND",
        "status": "ok",
        "blueprint": "DARTRIX ENGINE v2",
    }


@app.get("/state")
def state() -> Dict[str, Any]:
    return snet_agent.snapshot()


@app.post("/feedback")
def feedback(payload: FeedbackRequest) -> Dict[str, Any]:
    snet_state = snet_agent.evaluate(
        external_noise=payload.external_noise,
        internal_noise=payload.internal_noise,
        anomaly_score=payload.anomaly_score,
        intent_override=payload.intent_override,
        ren12_status=payload.ren12_status,
        k12_status=payload.k12_status,
    )
    return {
        "status": "received",
        "snet_state": snet_state.to_dict(),
    }


def _coerce_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _extract_snet_inputs(
    *,
    external_noise: Optional[float] = None,
    internal_noise: Optional[float] = None,
    anomaly_score: Optional[float] = None,
    intent_override: Optional[str] = None,
    ren12_status: Optional[str] = None,
    k12_status: Optional[str] = None,
    args: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    args = args or {}
    resolved_intent_override = intent_override or args.get("intent_override")
    resolved_external_noise = external_noise if external_noise is not None else _coerce_float(args.get("external_noise"))
    resolved_internal_noise = internal_noise if internal_noise is not None else _coerce_float(args.get("internal_noise"))
    resolved_anomaly_score = anomaly_score if anomaly_score is not None else _coerce_float(args.get("anomaly_score"))
    resolved_ren12_status = ren12_status or args.get("ren12_status")
    resolved_k12_status = k12_status or args.get("k12_status")
    return {
        "external_noise": resolved_external_noise,
        "internal_noise": resolved_internal_noise,
        "anomaly_score": resolved_anomaly_score,
        "intent_override": resolved_intent_override,
        "ren12_status": resolved_ren12_status,
        "k12_status": resolved_k12_status,
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


@app.post("/parse")
def parse(payload: ParseRequest) -> Dict[str, Any]:
    command = parse_command_text(payload.text, provider=payload.provider, model=payload.model)
    intent_override = payload.intent_override or ("alarm" if command.action == "alarm" or payload.text.strip().lower() == "alarm" else None)
    snet_state = snet_agent.evaluate(
        **_extract_snet_inputs(
            args=command.args,
            external_noise=payload.external_noise,
            internal_noise=payload.internal_noise,
            anomaly_score=payload.anomaly_score,
            intent_override=intent_override,
            ren12_status=payload.ren12_status,
            k12_status=payload.k12_status,
        )
    )
    command.args["snet_state"] = snet_state.to_dict()
    return {
        "command": command.model_dump(),
        "engine_mode": snet_state.engine_mode,
        "snet_state": snet_state.to_dict(),
    }


@app.post("/execute")
def execute(payload: ExecuteRequest) -> Dict[str, Any]:
    command = payload.command
    intent_override = payload.intent_override or command.args.get("intent_override") or ("alarm" if command.action == "alarm" else None)
    snet_state = snet_agent.evaluate(
        **_extract_snet_inputs(
            args=command.args,
            external_noise=payload.external_noise,
            internal_noise=payload.internal_noise,
            anomaly_score=payload.anomaly_score,
            intent_override=intent_override,
            ren12_status=payload.ren12_status,
            k12_status=payload.k12_status,
        )
    )
    result: Dict[str, Any] = {
        "status": "executed",
        "provider": command.provider or "local",
        "model": command.model,
        "command": command.model_dump(),
        "engine_mode": snet_state.engine_mode,
        "snet_state": snet_state.to_dict(),
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
