# PathLens

**PathLens is a computer-vision research prototype that investigates how to turn raw object detections into sparse, spatially useful accessibility guidance.**

Most object-detection demos answer *what is in the image?* PathLens focuses on a different question: **what is important enough to tell the user right now?**

> Status: early prototype. PathLens is not a validated mobility aid or safety system.

## Research question

> Can a context-aware ranking layer reduce unnecessary visual alerts while preserving recall of important environmental hazards compared with naive object reporting?

## Current pipeline

```text
Camera / Video
      ↓
Object Detection + Tracking
      ↓
Normalized Detections
      ↓
Spatial Reasoning
      ↓
Priority Score
      ↓
Temporal Guidance Policy
      ↓
Sparse User Alerts
```

The initial priority function combines five signals:

```text
priority =
    0.30 × semantic risk
  + 0.25 × distance risk
  + 0.25 × path relevance
  + 0.15 × motion risk
  + 0.05 × detector confidence
```

These weights are **baseline heuristics**, not claimed to be optimal. The project is designed so they can be compared and ablated experimentally.

## Features implemented

- Real-time YOLO detector/tracker adapter
- Model-agnostic normalized detection representation
- Left / ahead / right spatial reasoning
- Forward-corridor path relevance baseline
- Relative-depth interface
- Configurable context-aware priority engine
- Track-aware alert cooldown and suppression
- Webcam visualization
- NDCG and Precision@K evaluation utilities
- Unit tests and GitHub Actions CI

## Installation

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e .[demo,dev]
```

The first demo run downloads the configured Ultralytics model weights.

## Run the webcam demo

```bash
python scripts/run_webcam.py
```

Press `q` or `Esc` to quit.

## Run tests

```bash
pytest -q
```

## Evaluation

The repository intentionally contains **no claimed performance results yet**. Real results should be added only after recorded scenarios have been labeled and evaluated.

A planned evaluation compares:

1. detector-confidence-only ranking
2. distance-only ranking
3. semantic-risk-only ranking
4. full PathLens ranking

and then performs ablations that remove path, distance, motion, or semantic-risk terms.

See [`docs/evaluation.md`](docs/evaluation.md).

## Why this is not just an object detector

A camera can easily see many objects that are irrelevant to navigation. A high-confidence detection of a person far to the side may matter less than a lower-confidence vehicle entering the user's path. PathLens therefore separates **perception** from **decision-making** and treats alert selection as a ranking problem.

## Repository structure

```text
pathlens/               core library
  detector.py           YOLO adapter
  spatial.py            navigation-relative spatial features
  priority.py           ranking logic
  guidance.py           temporal alert policy
  visualize.py          debugging overlay
scripts/
  run_webcam.py         live baseline demo
  evaluate.py           ranking metrics
tests/                  deterministic unit tests
docs/                   architecture + research methodology
evaluation/             example schema; real data to be added later
configs/                 baseline configuration
```

## Roadmap

- [x] Detector + tracker baseline
- [x] Spatial priority baseline
- [x] Alert suppression
- [x] Ranking evaluation utilities
- [ ] Add monocular relative-depth estimator
- [ ] Estimate approach motion from tracked box/depth history
- [ ] Add accessibility-specific classes such as stairs / crosswalks / doors
- [ ] Record and annotate PathLens evaluation scenarios
- [ ] Benchmark baselines and ablations
- [ ] Add spoken guidance
- [ ] Build polished demo UI

## Responsible use

PathLens is an experimental computer-vision project. It may miss hazards, hallucinate detections, misjudge relevance, and behave differently across lighting, environments, camera motion, and users. It should not be used as a replacement for established mobility tools or professional accessibility guidance.

## License

Project source code is released under the MIT License. Third-party models and dependencies retain their own licenses and terms.
