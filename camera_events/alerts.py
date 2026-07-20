"""Exercise 3 — see README.md for the full prompt."""

from __future__ import annotations

from .models import DetectionEvent


def should_open_child_alone_alert(
    events: list[DetectionEvent | None] | None,
    window_millis: int,
    late_tolerance_millis: int | None = None,
) -> bool:
    """Exercise 3 (plus the follow-up).

    Return ``True`` when the child-alone condition
    (``child_count > 0 and adult_count == 0``) holds continuously for at least
    ``window_millis``.

    The follow-up is folded in via the optional ``late_tolerance_millis``
    parameter (Python has no method overloading): when it is provided, a gap
    between two consecutive normalized events that is greater than the
    tolerance resets the current child-alone window. When it is ``None`` the
    tolerance rule does not apply. See README.md for the exact rules.
    """
    # TODO: implement (Exercise 3 + follow-up)
    # Rule 1
    if not events:
        return False
    if window_millis <= 0:
        return False
    if (
        late_tolerance_millis is not None
        and late_tolerance_millis < 0
    ):
        return False
    valid_events = [event for event in events if event is not None]
    if not valid_events:
        return False
    by_timestamp: dict[int, DetectionEvent] = {}
    for event in valid_events:
        by_timestamp[event.timestamp_millis] = event
    normalized_events = sorted(
        by_timestamp.values(),
        key=lambda event: event.timestamp_millis,
    )

    start_time: int | None = None
    previous_timestamp: int | None = None

    for event in normalized_events:
        if (
            previous_timestamp is not None
            and late_tolerance_millis is not None
            and event.timestamp_millis - previous_timestamp > late_tolerance_millis
        ):
            start_time = None
        previous_timestamp = event.timestamp_millis
        if event.adult_count > 0 or event.child_count == 0:
            start_time = None
            continue
        if start_time is None:
            start_time = event.timestamp_millis
        # Window reached?
        if event.timestamp_millis - start_time >= window_millis:
            return True
    return False