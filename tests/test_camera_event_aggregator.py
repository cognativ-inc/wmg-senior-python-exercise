"""Tests for Exercises 1 and 2 — see README.md."""

from camera_events import (
    CameraEvent,
    aggregate_latest_event_by_camera,
    latest_event_by_camera,
)


# ---------------------------------------------------------------------
# Exercise 1 — latest_event_by_camera
# ---------------------------------------------------------------------


def test_ex1_groups_by_camera_and_keeps_latest_ignoring_later_duplicate():
    events = [
        CameraEvent("e1", "cam-1", 1000, 0, 0),
        CameraEvent("e2", "cam-1", 2000, 0, 0),
        CameraEvent("e3", "cam-2", 1500, 0, 0),
        CameraEvent("e1", "cam-1", 3000, 0, 0),
    ]

    result = latest_event_by_camera(events)

    assert len(result) == 2
    assert result["cam-1"].event_id == "e2"
    assert result["cam-2"].event_id == "e3"


def test_ex1_null_input_returns_empty_map():
    assert latest_event_by_camera(None) == {}


def test_ex1_duplicate_event_id_ignored_even_when_newer():
    events = [
        CameraEvent("e1", "cam-1", 1000, 0, 0),
        CameraEvent("e1", "cam-1", 9999, 0, 0),
    ]

    result = latest_event_by_camera(events)

    assert result["cam-1"].timestamp_millis == 1000


def test_ex1_ignores_null_and_invalid_events():
    events = [
        None,
        CameraEvent(None, "cam-1", 1000, 0, 0),
        CameraEvent("e1", None, 1000, 0, 0),
        CameraEvent("e2", "cam-1", 2000, 0, 0),
    ]

    result = latest_event_by_camera(events)

    assert len(result) == 1
    assert result["cam-1"].event_id == "e2"


def test_ex1_same_timestamp_keeps_last_in_input_order():
    events = [
        CameraEvent("e1", "cam-1", 2000, 0, 0),
        CameraEvent("e2", "cam-1", 2000, 0, 0),
    ]

    result = latest_event_by_camera(events)

    assert result["cam-1"].event_id == "e2"


def test_ex1_empty_list_returns_empty_map():
    assert latest_event_by_camera([]) == {}


# ---------------------------------------------------------------------
# Exercise 2 — aggregate_latest_event_by_camera
# ---------------------------------------------------------------------


def test_ex2_counts_ignored_duplicates():
    events = [
        CameraEvent("e1", "cam-1", 1000, 0, 0),
        CameraEvent("e2", "cam-1", 2000, 0, 0),
        CameraEvent("e1", "cam-1", 3000, 0, 0),
        CameraEvent("e2", "cam-1", 4000, 0, 0),
    ]

    result = aggregate_latest_event_by_camera(events)

    assert result.ignored_duplicate_count == 2
    assert result.latest_by_camera["cam-1"].event_id == "e2"
    assert result.latest_by_camera["cam-1"].timestamp_millis == 2000


def test_ex2_invalid_events_do_not_count_as_duplicates():
    events = [
        None,
        CameraEvent(None, "cam-1", 1000, 0, 0),
        CameraEvent("e1", None, 1000, 0, 0),
        CameraEvent("e2", "cam-1", 2000, 0, 0),
    ]

    result = aggregate_latest_event_by_camera(events)

    assert result.ignored_duplicate_count == 0


def test_ex2_null_input_returns_empty_result_with_zero_count():
    result = aggregate_latest_event_by_camera(None)

    assert result.latest_by_camera == {}
    assert result.ignored_duplicate_count == 0
