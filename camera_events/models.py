"""Data classes for the camera-events exercises.

``CameraEvent`` and ``DetectionEvent`` are provided for you — do not change
them. ``CameraAggregationResult`` is a starting point you may refine (see
Exercise 4).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CameraEvent:
    """A camera detection event received from a queue.

    This class is provided for you — do not change it.
    """

    event_id: str
    camera_id: str
    timestamp_millis: int
    adult_count: int
    child_count: int


@dataclass(frozen=True)
class DetectionEvent:
    """A detection event for a single camera.

    This class is provided for you — do not change it.
    """

    timestamp_millis: int
    adult_count: int
    child_count: int


@dataclass(frozen=True)
class CameraAggregationResult:
    """Result type for Exercise 4.

    Designing a clean return type is part of Exercise 4. This skeleton is
    provided so the project imports and the tests run; you are encouraged to
    refine it (immutability, defensive copies, naming) and to explain your
    choices to the interviewer.
    """

    latest_by_camera: dict[str, CameraEvent] = field(default_factory=dict)
    ignored_duplicate_count: int = 0
