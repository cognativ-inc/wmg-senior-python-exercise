"""Tests for Exercise 5 (and its follow-up) — see README.md."""

from camera_events import DetectionEvent, should_open_child_alone_alert


# ---------------------------------------------------------------------
# Exercise 5 — two-argument version
# ---------------------------------------------------------------------


def test_ex5_opens_when_window_reached():
    events = [
        DetectionEvent(1000, 0, 1),
        DetectionEvent(2000, 0, 1),
        DetectionEvent(3000, 0, 1),
    ]

    assert should_open_child_alone_alert(events, 2000) is True


def test_ex5_adult_breaks_window():
    events = [
        DetectionEvent(1000, 0, 1),
        DetectionEvent(2000, 1, 1),
        DetectionEvent(3000, 0, 1),
        DetectionEvent(4000, 0, 1),
    ]

    assert should_open_child_alone_alert(events, 2000) is False


def test_ex5_duplicate_timestamp_keeps_last_input_event():
    events = [
        DetectionEvent(1000, 0, 1),
        DetectionEvent(2000, 0, 1),
        DetectionEvent(2000, 1, 1),
        DetectionEvent(3000, 0, 1),
    ]

    assert should_open_child_alone_alert(events, 2000) is False


def test_ex5_handles_unordered_input():
    events = [
        DetectionEvent(3000, 0, 1),
        DetectionEvent(1000, 0, 1),
        DetectionEvent(2000, 0, 1),
    ]

    assert should_open_child_alone_alert(events, 2000) is True


def test_ex5_no_child_breaks_window():
    events = [
        DetectionEvent(1000, 0, 1),
        DetectionEvent(2000, 0, 0),
        DetectionEvent(3000, 0, 1),
    ]

    assert should_open_child_alone_alert(events, 2000) is False


def test_ex5_edge_cases_return_false():
    ok = [
        DetectionEvent(1000, 0, 1),
        DetectionEvent(3000, 0, 1),
    ]

    assert should_open_child_alone_alert(None, 2000) is False
    assert should_open_child_alone_alert([], 2000) is False
    assert should_open_child_alone_alert(ok, 0) is False
    assert should_open_child_alone_alert(ok, -1) is False


# ---------------------------------------------------------------------
# Exercise 5 — follow-up with late_tolerance_millis
# ---------------------------------------------------------------------


def test_ex5_followup_large_gap_resets_window():
    events = [
        DetectionEvent(1000, 0, 1),
        DetectionEvent(5000, 0, 1),
        DetectionEvent(6000, 0, 1),
    ]

    # Continuous in wall-clock terms, but the 1000 -> 5000 gap (4000) exceeds
    # the tolerance, so the window resets and never reaches 2000ms.
    assert should_open_child_alone_alert(events, 2000, 1500) is False


def test_ex5_followup_within_tolerance_opens():
    events = [
        DetectionEvent(1000, 0, 1),
        DetectionEvent(2000, 0, 1),
        DetectionEvent(3000, 0, 1),
    ]

    assert should_open_child_alone_alert(events, 2000, 1500) is True


def test_ex5_followup_negative_tolerance_returns_false():
    events = [
        DetectionEvent(1000, 0, 1),
        DetectionEvent(3000, 0, 1),
    ]

    assert should_open_child_alone_alert(events, 2000, -1) is False
