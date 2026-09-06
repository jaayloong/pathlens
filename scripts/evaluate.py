"""Evaluate ranking predictions against scenario relevance annotations.

Expected JSONL fields:
{"scene_id":"001", "items":[{"label":"car", "relevance":3, "score":0.9}, ...]}

This script intentionally evaluates supplied predictions; it does not fabricate
model results. Real PathLens experiments should export predictions from recorded
clips into this format.
"""
import argparse
import json
import math
from pathlib import Path


def dcg(relevances: list[int]) -> float:
    return sum((2**rel - 1) / math.log2(i + 2) for i, rel in enumerate(relevances))


def ndcg(items: list[dict]) -> float:
    predicted = sorted(items, key=lambda x: x["score"], reverse=True)
    ideal = sorted(items, key=lambda x: x["relevance"], reverse=True)
    denom = dcg([x["relevance"] for x in ideal])
    return 0.0 if denom == 0 else dcg([x["relevance"] for x in predicted]) / denom


def precision_at_k(items: list[dict], k: int, relevant_threshold: int = 2) -> float:
    ranked = sorted(items, key=lambda x: x["score"], reverse=True)[:k]
    if not ranked:
        return 0.0
    return sum(x["relevance"] >= relevant_threshold for x in ranked) / len(ranked)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("annotations", type=Path)
    parser.add_argument("--k", type=int, default=3)
    args = parser.parse_args()

    scenes = [json.loads(line) for line in args.annotations.read_text().splitlines() if line.strip()]
    if not scenes:
        raise SystemExit("No scenes found")

    ndcgs = [ndcg(scene["items"]) for scene in scenes]
    pks = [precision_at_k(scene["items"], args.k) for scene in scenes]
    print(f"Scenes: {len(scenes)}")
    print(f"Mean NDCG: {sum(ndcgs)/len(ndcgs):.4f}")
    print(f"Mean Precision@{args.k}: {sum(pks)/len(pks):.4f}")


if __name__ == "__main__":
    main()
