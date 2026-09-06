from __future__ import annotations

from dataclasses import dataclass

from .spatial import distance_risk, path_relevance
from .types import Detection, RankedDetection


DEFAULT_RISK = {
    "car": 0.90,
    "truck": 0.95,
    "bus": 0.95,
    "motorcycle": 0.90,
    "bicycle": 0.72,
    "person": 0.45,
    "traffic light": 0.70,
    "stop sign": 0.72,
    "bench": 0.25,
    "chair": 0.28,
}


@dataclass(frozen=True)
class PriorityWeights:
    semantic_risk: float = 0.30
    distance: float = 0.25
    path: float = 0.25
    motion: float = 0.15
    confidence: float = 0.05

    def validate(self) -> None:
        total = sum(self.__dict__.values())
        if abs(total - 1.0) > 1e-9:
            raise ValueError(f"priority weights must sum to 1.0, got {total:.4f}")


class PriorityEngine:
    def __init__(self, weights: PriorityWeights | None = None, risk_table: dict[str, float] | None = None):
        self.weights = weights or PriorityWeights()
        self.weights.validate()
        self.risk_table = {**DEFAULT_RISK, **(risk_table or {})}

    def rank_one(self, detection: Detection) -> RankedDetection:
        semantic = self.risk_table.get(detection.class_name.lower(), 0.20)
        distance = distance_risk(detection)
        path = path_relevance(detection)
        motion = 1.0 if detection.approaching else min(1.0, abs(detection.lateral_motion))
        confidence = max(0.0, min(1.0, detection.confidence))

        w = self.weights
        score = (
            w.semantic_risk * semantic
            + w.distance * distance
            + w.path * path
            + w.motion * motion
            + w.confidence * confidence
        )
        return RankedDetection(
            detection=detection,
            semantic_risk=semantic,
            distance_risk=distance,
            path_relevance=path,
            motion_risk=motion,
            confidence_term=confidence,
            score=score,
        )

    def rank(self, detections: list[Detection]) -> list[RankedDetection]:
        return sorted((self.rank_one(d) for d in detections), key=lambda x: x.score, reverse=True)
