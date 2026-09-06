from pathlens.spatial import horizontal_region, path_relevance
from pathlens.types import Detection


def make_det(cx: float) -> Detection:
    return Detection("person", 0.9, (cx - 10, 20, cx + 10, 80), 100, 100)


def test_horizontal_regions():
    assert horizontal_region(make_det(10)) == "left"
    assert horizontal_region(make_det(50)) == "ahead"
    assert horizontal_region(make_det(90)) == "right"


def test_center_has_more_path_relevance():
    assert path_relevance(make_det(50)) > path_relevance(make_det(15))
