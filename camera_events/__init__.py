"""Camera Events — backend interview exercises (Python).

See README.md for the full prompts. Implement the functions in
``aggregator.py`` (Exercises 1 & 2) and ``alerts.py`` (Exercise 3).
"""

from .models import CameraAggregationResult, CameraEvent, DetectionEvent
from .aggregator import aggregate_latest_event_by_camera, latest_event_by_camera
from .alerts import should_open_child_alone_alert

__all__ = [
    "CameraEvent",
    "DetectionEvent",
    "CameraAggregationResult",
    "latest_event_by_camera",
    "aggregate_latest_event_by_camera",
    "should_open_child_alone_alert",
]
