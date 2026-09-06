from __future__ import annotations

from typing import Any

from .types import Detection


class YOLODetector:
    """Thin adapter around Ultralytics so the reasoning stack is model-agnostic."""

    def __init__(self, model_name: str = "yolo26n.pt", conf: float = 0.25, tracker: str = "bytetrack.yaml"):
        try:
            from ultralytics import YOLO
        except ImportError as exc:  # pragma: no cover - integration dependency
            raise RuntimeError("Install PathLens demo dependencies with `pip install -e .[demo]`") from exc

        self.model: Any = YOLO(model_name)
        self.conf = conf
        self.tracker = tracker

    def detect(self, frame) -> list[Detection]:
        height, width = frame.shape[:2]
        result = self.model.track(
            frame,
            persist=True,
            conf=self.conf,
            tracker=self.tracker,
            verbose=False,
        )[0]

        detections: list[Detection] = []
        boxes = result.boxes
        if boxes is None:
            return detections

        names = result.names
        for idx in range(len(boxes)):
            xyxy = boxes.xyxy[idx].detach().cpu().tolist()
            conf = float(boxes.conf[idx].detach().cpu())
            cls_id = int(boxes.cls[idx].detach().cpu())
            track_id = None
            if boxes.id is not None:
                track_id = int(boxes.id[idx].detach().cpu())
            detections.append(
                Detection(
                    class_name=str(names[cls_id]),
                    confidence=conf,
                    bbox=tuple(float(v) for v in xyxy),
                    frame_width=width,
                    frame_height=height,
                    track_id=track_id,
                )
            )
        return detections
