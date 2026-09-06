from __future__ import annotations

from .types import Detection


def horizontal_region(detection: Detection, center_threshold: float = 0.28) -> str:
    x = detection.normalized_x
    if x < -center_threshold:
        return "left"
    if x > center_threshold:
        return "right"
    return "ahead"


def path_relevance(detection: Detection, corridor_half_width: float = 0.45) -> float:
    """Triangular relevance score based on proximity to a forward image corridor.

    This is deliberately a simple baseline, not a claim of geometric free-space
    understanding. A future version can replace this with segmentation/ground-plane
    reasoning while preserving the same interface.
    """
    x = abs(detection.normalized_x)
    if x >= corridor_half_width:
        return 0.0
    return 1.0 - x / corridor_half_width


def distance_risk(detection: Detection) -> float:
    """Convert relative depth (0 near, 1 far) to a risk contribution."""
    if detection.depth is None:
        # Neutral prior when no depth estimator is enabled.
        return 0.5
    return max(0.0, min(1.0, 1.0 - detection.depth))
