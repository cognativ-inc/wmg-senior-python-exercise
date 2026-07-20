"""Exercises 1 and 2 — see README.md for the full prompts."""

from __future__ import annotations

from .models import CameraAggregationResult, CameraEvent


# from __future__ import annotations

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


def latest_event_by_camera(
    events: list[CameraEvent | None] | None,
) -> dict[str, CameraEvent]:
    if events is None:
        return {}
    
    
    seen_event_ids: set[str] = set()
    latest: dict[str, CameraEvent] = {}

    for event in events:
        if event is None:
            continue
        if event.event_id is None:
            continue
        if event.camera_id is None:
            continue
        if event.event_id in seen_event_ids:
            continue
        seen_event_ids.add(event.event_id)
        current_cam_id = latest.get(event.camera_id)
        if current_cam_id is None or event.timestamp_millis >= current_cam_id.timestamp_millis:
            latest[event.camera_id]=event
    return latest



def aggregate_latest_event_by_camera(
    events: list[CameraEvent | None] | None,
) -> CameraAggregationResult:
    """Exercise 2.

    Same behaviour as Exercise 1, but also report how many duplicate events
    were ignored — without side effects or external mutable state.
    """
    if events is None:
        return CameraAggregationResult({},0)
    seen_event_ids: set[str] = set()
    latest: dict[str, CameraEvent] = {}
    ignored_duplicate_count = 0

    for event in events:
        if event is None or event.event_id is None or event.camera_id is None:
            continue
        if event.event_id in seen_event_ids:
            ignored_duplicate_count += 1
            continue
        seen_event_ids.add(event.event_id)
        current_cam_id = latest.get(event.camera_id)
        #breakpoint()
        if current_cam_id is None or event.timestamp_millis >= current_cam_id.timestamp_millis:
            latest[event.camera_id]=event
    
    return CameraAggregationResult(latest,ignored_duplicate_count)

    # # TODO: implement (Exercise 2)
    # raise NotImplementedError("Not implemented yet (Exercise 2)")
