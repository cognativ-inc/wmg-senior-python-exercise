# Python Backend Interview Exercises — Camera Events

Welcome, and thanks for taking the time. This is a small set of backend Python
exercises built around a stream of camera detection events.

## Setup

- **Python 3.10+** is required.
- Install the test dependency and run the tests:

  ```bash
  python -m pip install -r requirements.txt   # just pytest
  pytest
  ```

All tests currently **fail** because the functions are not implemented yet —
that is expected. Your job is to make them pass. You are welcome to add your own
tests as well.

## Where to work

| Exercise | File |
| --- | --- |
| 1 & 2 | `camera_events/aggregator.py` |
| 3 | `camera_events/alerts.py` |

The data classes (`CameraEvent`, `DetectionEvent`) in `camera_events/models.py`
are provided — don't change them. `CameraAggregationResult` is a starting point
you may refine (see Exercise 2).

---

## Exercise 1 — Deduplicate and aggregate camera events

You receive camera detection events from a queue. Some messages may be
duplicated.

```python
@dataclass(frozen=True)
class CameraEvent:
    event_id: str
    camera_id: str
    timestamp_millis: int
    adult_count: int
    child_count: int
```

Implement:

```python
def latest_event_by_camera(events: list[CameraEvent] | None) -> dict[str, CameraEvent]
```

Rules:

1. Ignore duplicate `event_id`.
2. Group events by `camera_id`.
3. For each camera, return the latest event by `timestamp_millis`.
4. If two valid events for the same camera have the same timestamp, keep the one
   that appeared **last** in the input list.
5. Ignore `None` events.
6. Ignore events where `event_id` is `None`.
7. Ignore events where `camera_id` is `None`.
8. If the input list is `None`, return an empty dict.

**Important:** if the same `event_id` appears more than once, only the **first**
occurrence counts — even if the duplicate has a newer timestamp, it must be
ignored.

### Example

Input:

```text
event_id="e1", camera_id="cam-1", timestamp_millis=1000
event_id="e2", camera_id="cam-1", timestamp_millis=2000
event_id="e3", camera_id="cam-2", timestamp_millis=1500
event_id="e1", camera_id="cam-1", timestamp_millis=3000
```

Expected result:

```text
cam-1 -> e2
cam-2 -> e3
```

The last `e1` is ignored because `event_id="e1"` was already seen.

---

## Exercise 2 — Return aggregation metadata

Evolve the previous solution. The function must still return the latest event by
camera, but it must **also** report how many duplicate events were ignored.

- Do not use global variables.
- Do not mutate an external counter.
- Design a clean return type.

Implement:

```python
def aggregate_latest_event_by_camera(events: list[CameraEvent] | None) -> CameraAggregationResult
```

The result should contain:

```python
latest_by_camera: dict[str, CameraEvent]
ignored_duplicate_count: int
```

### Example

Input:

```text
event_id="e1", camera_id="cam-1", timestamp_millis=1000
event_id="e2", camera_id="cam-1", timestamp_millis=2000
event_id="e1", camera_id="cam-1", timestamp_millis=3000
event_id="e2", camera_id="cam-1", timestamp_millis=4000
```

Expected:

```text
latest_by_camera:        cam-1 -> e2 at timestamp 2000
ignored_duplicate_count: 2
```

The second `e1` and the second `e2` are ignored. Note: only ignored **duplicate
event IDs** count — `None`/invalid events do not.

---

## Exercise 3 — Detect child-alone alert windows

You receive detection events for **one** camera. Events may arrive ordered or
unordered.

```python
@dataclass(frozen=True)
class DetectionEvent:
    timestamp_millis: int
    adult_count: int
    child_count: int
```

Implement:

```python
def should_open_child_alone_alert(events: list[DetectionEvent] | None, window_millis: int) -> bool
```

An alert should open when this condition holds **continuously** for at least
`window_millis`:

```python
child_count > 0 and adult_count == 0
```

Rules:

1. Events may arrive out of order.
2. Sort events by `timestamp_millis`.
3. If multiple events share the same timestamp, keep the **last** one from the
   original input order.
4. The alert opens only if the child-alone state lasts continuously for at least
   `window_millis`.
5. Any event with `adult_count > 0` breaks the current window.
6. Any event with `child_count == 0` breaks the current window.
7. Ignore `None` events.
8. If the input is `None` or empty, return `False`.
9. If `window_millis <= 0`, return `False`.

### Example 1 — opens

```text
timestamp_millis=1000, adult_count=0, child_count=1
timestamp_millis=2000, adult_count=0, child_count=1
timestamp_millis=3000, adult_count=0, child_count=1
window_millis = 2000   ->   True   (3000 - 1000 = 2000)
```

### Example 2 — adult breaks the window

```text
timestamp_millis=1000, adult_count=0, child_count=1
timestamp_millis=2000, adult_count=1, child_count=1
timestamp_millis=3000, adult_count=0, child_count=1
timestamp_millis=4000, adult_count=0, child_count=1
window_millis = 2000   ->   False
```

### Example 3 — duplicate timestamp keeps last input event

```text
timestamp_millis=1000, adult_count=0, child_count=1
timestamp_millis=2000, adult_count=0, child_count=1
timestamp_millis=2000, adult_count=1, child_count=1
timestamp_millis=3000, adult_count=0, child_count=1
window_millis = 2000   ->   False   (last event at 2000 has an adult)
```

### Follow-up — `late_tolerance_millis`

Once the basic version works, support an optional third parameter (Python has no
method overloading, so use a keyword/default argument):

```python
def should_open_child_alone_alert(
    events: list[DetectionEvent] | None,
    window_millis: int,
    late_tolerance_millis: int | None = None,
) -> bool
```

Added rules (apply only when `late_tolerance_millis` is provided):

1. Normalize duplicate timestamps as before.
2. Sort events as before.
3. Track the gap between consecutive normalized events.
4. If the gap is greater than `late_tolerance_millis`, reset the current
   child-alone window.
5. If `late_tolerance_millis < 0`, return `False`.

---

Good luck — focus on clean, readable code and be ready to talk through your
reasoning (data structures chosen, edge cases, and time complexity).
