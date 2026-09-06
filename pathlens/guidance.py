from __future__ import annotations

from dataclasses import dataclass

from .spatial import horizontal_region
from .types import RankedDetection


@dataclass
class GuidanceConfig:
    min_score: float = 0.55
    cooldown_frames: int = 45
    max_alerts_per_frame: int = 2


class GuidancePolicy:
    """Turns ranked detections into sparse, repeat-suppressed guidance events."""

    def __init__(self, config: GuidanceConfig | None = None):
        self.config = config or GuidanceConfig()
        self._last_alert_frame: dict[str, int] = {}

    def _key(self, item: RankedDetection) -> str:
        d = item.detection
        identity = d.track_id if d.track_id is not None else horizontal_region(d)
        return f"{d.class_name}:{identity}"

    def _message(self, item: RankedDetection) -> str:
        d = item.detection
        position = horizontal_region(d)
        name = d.class_name.replace("_", " ")
        if d.approaching:
            return f"{name.capitalize()} approaching from the {position}." if position != "ahead" else f"{name.capitalize()} approaching ahead."
        if position == "ahead":
            return f"{name.capitalize()} ahead."
        return f"{name.capitalize()} to the {position}."

    def alerts(self, ranked: list[RankedDetection], frame_index: int) -> list[str]:
        output: list[str] = []
        for item in ranked:
            if item.score < self.config.min_score:
                continue
            key = self._key(item)
            last = self._last_alert_frame.get(key, -10**9)
            if frame_index - last < self.config.cooldown_frames:
                continue
            self._last_alert_frame[key] = frame_index
            output.append(self._message(item))
            if len(output) >= self.config.max_alerts_per_frame:
                break
        return output
