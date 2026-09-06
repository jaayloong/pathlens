import pytest

from pathlens.priority import PriorityEngine, PriorityWeights
from pathlens.types import Detection


def det(name="person", x=50, depth=0.5, approaching=False, conf=0.9):
    return Detection(name, conf, (x - 10, 20, x + 10, 80), 100, 100, depth=depth, approaching=approaching)


def test_near_center_vehicle_outranks_far_side_person():
    engine = PriorityEngine()
    vehicle = engine.rank_one(det("car", x=50, depth=0.1, approaching=True))
    person = engine.rank_one(det("person", x=10, depth=0.9))
    assert vehicle.score > person.score


def test_weights_must_sum_to_one():
    with pytest.raises(ValueError):
        PriorityEngine(PriorityWeights(confidence=0.5))
