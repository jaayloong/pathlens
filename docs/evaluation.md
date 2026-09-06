# Evaluation Plan

PathLens should be evaluated on recorded navigation scenarios rather than judged only by detector accuracy.

## Scenario labels
For each short clip, annotate visible candidate items with relevance:

- `0`: irrelevant
- `1`: useful context
- `2`: important
- `3`: immediate hazard / critical guidance

## Primary metrics

- **NDCG**: does PathLens rank the most relevant items first?
- **Precision@K**: among the top K alerts, how many are actually important?
- **Hazard recall**: fraction of relevance-3 hazards surfaced above the alert threshold.
- **Alert count per minute**: measures information overload.
- **Latency / FPS**: measures real-time feasibility.

## Baselines

1. Detector confidence only
2. Distance only
3. Semantic-risk only
4. Full PathLens priority score

## Ablations

Remove one term at a time from the full model:

- no path relevance
- no distance
- no motion
- no semantic risk

Do not put numbers in the README until the experiment has actually been run and the raw prediction/annotation files are committed or otherwise reproducible.
