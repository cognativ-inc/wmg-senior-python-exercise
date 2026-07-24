"""Camera Events — backend interview exercises (Python).

See README.md for the full prompts. Implement the functions in
``basics.py`` (Exercises 1 & 2, warm-ups), ``aggregator.py`` (Exercises 3 & 4)
and ``alerts.py`` (Exercise 5).
"""

from .models import CameraAggregationResult, CameraEvent, DetectionEvent
from .basics import count_events_per_camera, total_people_per_camera
from .aggregator import aggregate_latest_event_by_camera, latest_event_by_camera
from .alerts import should_open_child_alone_alert

__all__ = [
    "CameraEvent",
    "DetectionEvent",
    "CameraAggregationResult",
    "count_events_per_camera",
    "total_people_per_camera",
    "latest_event_by_camera",
    "aggregate_latest_event_by_camera",
    "should_open_child_alone_alert",
]
