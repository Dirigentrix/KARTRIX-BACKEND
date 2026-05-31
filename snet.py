from dataclasses import asdict, dataclass
from typing import Any, Dict, Literal, Optional


EngineMode = Literal["Flow", "Alert", "Stop"]
ModeSignal = Literal["SAFE", "CHECK", "ALERT"]
StabilityFlag = Literal["TRUE", "PARTIAL", "FALSE"]
GateState = Literal["OPEN", "LOCKED"]


@dataclass
class SNetState:
    external_noise: float = 0.0
    internal_noise: float = 0.0
    anomaly_score: float = 0.0
    alert_signal: float = 0.0
    engine_mode: EngineMode = "Flow"
    mode_signal: ModeSignal = "SAFE"
    stability_flag: StabilityFlag = "TRUE"
    ren12_override: GateState = "OPEN"
    k12_gate: GateState = "OPEN"
    ren12_status: Optional[str] = None
    k12_status: Optional[str] = None
    intent_override: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SNetAgent:
    def __init__(self) -> None:
        self.state = SNetState()

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    @staticmethod
    def _normalize_mode_signal(value: Optional[str]) -> Optional[ModeSignal]:
        if value is None:
            return None
        normalized = str(value).strip().upper()
        if normalized in {"SAFE", "CHECK", "ALERT"}:
            return normalized  # type: ignore[return-value]
        return None

    @staticmethod
    def _normalize_stability_flag(value: Optional[str]) -> Optional[StabilityFlag]:
        if value is None:
            return None
        normalized = str(value).strip().upper()
        if normalized in {"TRUE", "PARTIAL", "FALSE"}:
            return normalized  # type: ignore[return-value]
        return None

    @staticmethod
    def _derive_mode_signal(alert_signal: float) -> ModeSignal:
        if alert_signal < 0.3:
            return "SAFE"
        if alert_signal < 0.7:
            return "CHECK"
        return "ALERT"

    @staticmethod
    def _derive_stability_flag(alert_signal: float) -> StabilityFlag:
        if alert_signal < 0.3:
            return "TRUE"
        if alert_signal < 0.7:
            return "PARTIAL"
        return "FALSE"

    def evaluate(
        self,
        *,
        external_noise: Optional[float] = None,
        internal_noise: Optional[float] = None,
        anomaly_score: Optional[float] = None,
        intent_override: Optional[str] = None,
        ren12_status: Optional[str] = None,
        k12_status: Optional[str] = None,
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

        normalized_mode_signal = self._normalize_mode_signal(ren12_status)
        normalized_stability_flag = self._normalize_stability_flag(k12_status)

        self.state.ren12_status = ren12_status.strip().upper() if isinstance(ren12_status, str) and ren12_status.strip() else None
        self.state.k12_status = k12_status.strip().upper() if isinstance(k12_status, str) and k12_status.strip() else None

        self.state.mode_signal = normalized_mode_signal or self._derive_mode_signal(self.state.alert_signal)
        self.state.stability_flag = normalized_stability_flag or self._derive_stability_flag(self.state.alert_signal)

        return self.state

    def snapshot(self) -> Dict[str, Any]:
        return self.state.to_dict()
