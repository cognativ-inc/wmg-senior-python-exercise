"""Exercises 3 and 4 — see README.md for the full prompts."""

from __future__ import annotations

from .models import CameraAggregationResult, CameraEvent


def latest_event_by_camera(
    events: list[CameraEvent | None] | None,
) -> dict[str, CameraEvent]:
    """Exercise 3.

    Return the latest :class:`CameraEvent` per ``camera_id``, ignoring
    duplicate ``event_id`` values and invalid events. See README.md for the
    exact rules.
    """
    # TODO: implement (Exercise 3)
    raise NotImplementedError("Not implemented yet (Exercise 3)")


def aggregate_latest_event_by_camera(
    events: list[CameraEvent | None] | None,
) -> CameraAggregationResult:
    """Exercise 4.

    Same behaviour as Exercise 3, but also report how many duplicate events
    were ignored — without side effects or external mutable state.
    """
    # TODO: implement (Exercise 4)
    raise NotImplementedError("Not implemented yet (Exercise 4)")
