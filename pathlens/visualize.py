from __future__ import annotations

import cv2

from .types import RankedDetection


def draw_ranked(frame, ranked: list[RankedDetection], limit: int = 8):
    canvas = frame.copy()
    for item in ranked[:limit]:
        d = item.detection
        x1, y1, x2, y2 = map(int, d.bbox)
        label = f"{d.class_name}  priority={item.score:.2f}"
        cv2.rectangle(canvas, (x1, y1), (x2, y2), (255, 255, 255), 2)
        cv2.putText(canvas, label, (x1, max(20, y1 - 7)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
    return canvas
