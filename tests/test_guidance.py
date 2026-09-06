from pathlens.guidance import GuidanceConfig, GuidancePolicy
from pathlens.priority import PriorityEngine
from pathlens.types import Detection


def test_cooldown_suppresses_repeat_alerts():
    d = Detection("car", 0.99, (40, 20, 60, 80), 100, 100, track_id=7, depth=0.1, approaching=True)
    ranked = PriorityEngine().rank([d])
    policy = GuidancePolicy(GuidanceConfig(min_score=0.1, cooldown_frames=10))
    assert policy.alerts(ranked, 0)
    assert policy.alerts(ranked, 1) == []
    assert policy.alerts(ranked, 10)
