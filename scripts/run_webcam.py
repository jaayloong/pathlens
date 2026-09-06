import argparse
import time

import cv2

from pathlens.detector import YOLODetector
from pathlens.guidance import GuidancePolicy
from pathlens.priority import PriorityEngine
from pathlens.visualize import draw_ranked


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the PathLens webcam baseline")
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--model", default="yolo26n.pt")
    args = parser.parse_args()

    detector = YOLODetector(model_name=args.model)
    ranker = PriorityEngine()
    guidance = GuidancePolicy()
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera {args.camera}")

    frame_index = 0
    last_time = time.perf_counter()
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            detections = detector.detect(frame)
            ranked = ranker.rank(detections)
            alerts = guidance.alerts(ranked, frame_index)
            canvas = draw_ranked(frame, ranked)

            now = time.perf_counter()
            fps = 1.0 / max(now - last_time, 1e-6)
            last_time = now
            cv2.putText(canvas, f"FPS {fps:.1f}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
            if alerts:
                cv2.putText(canvas, alerts[0], (10, canvas.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                print(" | ".join(alerts))

            cv2.imshow("PathLens", canvas)
            frame_index += 1
            if cv2.waitKey(1) & 0xFF in (27, ord("q")):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
