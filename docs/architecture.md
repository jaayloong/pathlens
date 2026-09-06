# Architecture

PathLens separates **perception** from **decision-making**.

1. **Detector/tracker**: extracts object class, confidence, box, and persistent ID.
2. **Spatial layer**: converts image location into a coarse navigation-relative representation.
3. **Depth interface**: currently optional; accepts relative depth in `[0,1]`.
4. **Priority engine**: combines semantic risk, relative distance, path relevance, motion, and confidence.
5. **Guidance policy**: thresholds and suppresses repeated alerts.
6. **Evaluation**: compares rankings against human relevance annotations.

The first release deliberately uses a simple image-center corridor. It should be treated as a baseline, not as free-space estimation. Future experiments should compare it with semantic segmentation or ground-plane-aware path estimation.
