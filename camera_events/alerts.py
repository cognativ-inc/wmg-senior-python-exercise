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
    raise NotImplementedError("Not implemented yet (Exercise 3)")
