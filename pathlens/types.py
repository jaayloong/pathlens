from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Detection:
    """Normalized object detection used by the PathLens reasoning stack."""

    class_name: str
    confidence: float
    bbox: tuple[float, float, float, float]
    frame_width: int
    frame_height: int
    track_id: Optional[int] = None
    depth: Optional[float] = None  # 0=near, 1=far (relative depth convention)
    approaching: bool = False
    lateral_motion: float = 0.0
    metadata: dict = field(default_factory=dict)

    @property
    def center(self) -> tuple[float, float]:
        x1, y1, x2, y2 = self.bbox
        return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)

    @property
    def normalized_x(self) -> float:
        """Horizontal center mapped to [-1, 1]."""
        x, _ = self.center
        if self.frame_width <= 0:
            return 0.0
        return max(-1.0, min(1.0, 2.0 * (x / self.frame_width) - 1.0))


@dataclass
class RankedDetection:
    detection: Detection
    semantic_risk: float
    distance_risk: float
    path_relevance: float
    motion_risk: float
    confidence_term: float
    score: float
