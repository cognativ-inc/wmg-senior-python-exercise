"""Exercises 1 and 2 (warm-ups) — see README.md for the full prompts.

These two exercises are deliberately simple. They exist to get you comfortable
with the data model before the harder exercises: the input is always a
``list[CameraEvent]`` (a list of objects), never a list of strings.
"""

from __future__ import annotations

from .models import CameraEvent


def count_events_per_camera(
    events: list[CameraEvent | None] | None,
) -> dict[str, int]:
    """Exercise 1 (warm-up).

    Return how many events each ``camera_id`` produced. No deduplication and no
    timestamp logic — just count. See README.md for the exact rules.
    """
    # TODO: implement (Exercise 1)
    raise NotImplementedError("Not implemented yet (Exercise 1)")


def total_people_per_camera(
    events: list[CameraEvent | None] | None,
) -> dict[str, int]:
    """Exercise 2 (warm-up).

    Return, per ``camera_id``, the total number of people seen across all of
    that camera's events (``adult_count + child_count`` summed). See README.md
    for the exact rules.
    """
    # TODO: implement (Exercise 2)
    raise NotImplementedError("Not implemented yet (Exercise 2)")
