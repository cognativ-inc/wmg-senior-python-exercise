"""Tests for Exercises 1 and 2 (warm-ups) — see README.md."""

from camera_events import (
    CameraEvent,
    count_events_per_camera,
    total_people_per_camera,
)


# ---------------------------------------------------------------------
# Exercise 1 — count_events_per_camera
# ---------------------------------------------------------------------


def test_ex1_counts_events_grouped_by_camera():
    events = [
        CameraEvent("e1", "cam-1", 1000, 1, 0),
        CameraEvent("e2", "cam-1", 2000, 0, 0),
        CameraEvent("e3", "cam-2", 1500, 0, 0),
    ]

    result = count_events_per_camera(events)

    assert result == {"cam-1": 2, "cam-2": 1}


def test_ex1_null_input_returns_empty_map():
    assert count_events_per_camera(None) == {}


def test_ex1_ignores_null_and_missing_camera_id():
    events = [
        None,
        CameraEvent("e1", None, 1000, 0, 0),
        CameraEvent("e2", "cam-1", 2000, 0, 0),
    ]

    result = count_events_per_camera(events)

    assert result == {"cam-1": 1}


# ---------------------------------------------------------------------
# Exercise 2 — total_people_per_camera
# ---------------------------------------------------------------------


def test_ex2_sums_adults_and_children_per_camera():
    events = [
        CameraEvent("e1", "cam-1", 1000, 2, 1),
        CameraEvent("e2", "cam-1", 2000, 0, 3),
        CameraEvent("e3", "cam-2", 1500, 1, 0),
    ]

    result = total_people_per_camera(events)

    assert result == {"cam-1": 6, "cam-2": 1}


def test_ex2_null_input_returns_empty_map():
    assert total_people_per_camera(None) == {}


def test_ex2_ignores_null_and_missing_camera_id():
    events = [
        None,
        CameraEvent("e1", None, 1000, 5, 5),
        CameraEvent("e2", "cam-1", 2000, 1, 1),
    ]

    result = total_people_per_camera(events)

    assert result == {"cam-1": 2}
