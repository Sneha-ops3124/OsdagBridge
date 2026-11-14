
from osdagbridge.core.bridge_types.plate_girder import analyser


class FakeLoadCase:
    def __init__(self, name):
        self.name = name
        self.load_groups = []

    def add_load(self, load):
        self.load_groups.append({"load": load})


class FakeModel:
    def __init__(self):
        self.added_cases = []

    def add_load_case(self, load_case, load_factor=1.0):
        self.added_cases.append((load_case, load_factor))


def make_load_case(name, load):
    case = FakeLoadCase(name)
    case.add_load(load)
    return case


def test_dead_load_combination_includes_sidl_but_excludes_wearing_course(monkeypatch):
    def fake_create_load_case(name):
        return FakeLoadCase(name)

    monkeypatch.setattr(
        analyser.og, "create_load_case", fake_create_load_case
    )

    bridge = analyser.BridgeGrillageModel()
    bridge.model = FakeModel()

    barrier = object()
    railing = object()
    median = object()
    self_weight = object()
    deck = object()
    footpath = object()
    wearing_course = object()

    bridge.crash_barrier_load_case = make_load_case("barrier", barrier)
    bridge.railing_load_case = make_load_case("railing", railing)
    bridge.median_load_case = make_load_case("median", median)

    bridge.self_weight_load_case = make_load_case("SW", self_weight)
    bridge.deck_load_case = make_load_case("DD", deck)
    bridge.footpath_load_case = make_load_case("footpath", footpath)
    bridge.wearing_course_load = make_load_case("DW", wearing_course)

    sidl = bridge.create_sidl_combination(partial_safety_factor=1.0)

    assert [entry["load"] for entry in sidl.load_groups] == [
        barrier, railing, median
    ]

    dead_load = bridge.create_dead_load_combination(
        partial_safety_factor=1.0
    )

    assert [entry["load"] for entry in dead_load.load_groups] == [
        self_weight,
        deck,
        footpath,
        barrier,
        railing,
        median,
    ]

    assert [entry["load"] for entry in bridge.wearing_course_load.load_groups] == [
        wearing_course
    ]

    assert bridge.model.added_cases == [
        (sidl, 1.0),
        (dead_load, 1.0),
    ]
