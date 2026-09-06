import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("evaluate", Path(__file__).parents[1] / "scripts" / "evaluate.py")
evaluate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluate)


def test_perfect_ndcg_is_one():
    items = [
        {"relevance": 3, "score": 0.9},
        {"relevance": 2, "score": 0.8},
        {"relevance": 0, "score": 0.1},
    ]
    assert abs(evaluate.ndcg(items) - 1.0) < 1e-9
