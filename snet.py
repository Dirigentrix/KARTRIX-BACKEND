from dataclasses import asdict, dataclass
from typing import Any, Dict, Literal, Optional


EngineMode = Literal["Flow", "Alert", "Stop"]
GateState = Literal["OPEN", "LOCKED"]


@dataclass
class SNetState:
    external_noise: float = 0.0
    internal_noise: float = 0.0
    anomaly_score: float = 0.0
    alert_signal: float = 0.0
    engine_mode: EngineMode = "Flow"
    ren12_override: GateState = "OPEN"
    k12_gate: GateState = "OPEN"
    intent_override: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SNetAgent:
    def __init__(self) -> None:
        self.state = SNetState()

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    def evaluate(
        self,
        *,
        external_noise: Optional[float] = None,
        internal_noise: Optional[float] = None,
        anomaly_score: Optional[float] = None,
        intent_override: Optional[str] = None,
    ) -> SNetState:
        if external_noise is not None:
            self.state.external_noise = self._clamp(external_noise)
        if internal_noise is not None:
            self.state.internal_noise = self._clamp(internal_noise)
        if anomaly_score is not None:
            self.state.anomaly_score = self._clamp(anomaly_score)

        self.state.intent_override = intent_override

        alert_signal = (
            0.4 * self.state.external_noise
            + 0.3 * self.state.internal_noise
            + 0.3 * self.state.anomaly_score
        )

        if intent_override == "alarm":
            alert_signal = 1.0

        self.state.alert_signal = self._clamp(alert_signal)

        if self.state.alert_signal < 0.3:
            self.state.engine_mode = "Flow"
        elif self.state.alert_signal < 0.7:
            self.state.engine_mode = "Alert"
        else:
            self.state.engine_mode = "Stop"

        if self.state.alert_signal > 0.7:
            self.state.ren12_override = "LOCKED"
            self.state.k12_gate = "LOCKED"
        else:
            self.state.ren12_override = "OPEN"
            self.state.k12_gate = "OPEN"

        return self.state

    def snapshot(self) -> Dict[str, Any]:
        return self.state.to_dict()
