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

## The data model — read this first

Every function receives a **`list` of objects**, never a list of strings. The
objects are the `@dataclass` instances defined in `camera_events/models.py`:

```python
@dataclass(frozen=True)
class CameraEvent:
    event_id: str
    camera_id: str
    timestamp_millis: int
    adult_count: int
    child_count: int


@dataclass(frozen=True)
class DetectionEvent:
    timestamp_millis: int
    adult_count: int
    child_count: int
```

So an input list is built like this — real `CameraEvent` objects, not text:

```python
events = [
    CameraEvent(event_id="e1", camera_id="cam-1", timestamp_millis=1000, adult_count=0, child_count=0),
    CameraEvent(event_id="e2", camera_id="cam-1", timestamp_millis=2000, adult_count=1, child_count=0),
]
```

Every "Input" block in the examples below is constructing objects exactly like
this. When you access a field, you use attribute access (`event.camera_id`),
**not** string parsing.

The data classes (`CameraEvent`, `DetectionEvent`) are provided — don't change
them. `CameraAggregationResult` is a starting point you may refine (see
Exercise 4).

## Where to work

| Exercise | File |
| --- | --- |
| 1 & 2 (warm-ups) | `camera_events/basics.py` |
| 3 & 4 | `camera_events/aggregator.py` |
| 5 | `camera_events/alerts.py` |

Work through them in order — 1 and 2 are quick warm-ups to get you used to the
data model; 3, 4 and 5 are the main exercises.

---

## Exercise 1 — Count events per camera (warm-up)

A gentle warm-up. You receive a list of `CameraEvent` objects. Count how many
events each camera produced.

Implement:

```python
def count_events_per_camera(events: list[CameraEvent] | None) -> dict[str, int]
```

Rules:

1. If the input list is `None`, return an empty dict.
2. Ignore `None` events.
3. Ignore events where `camera_id` is `None`.
4. Return a mapping from `camera_id` to the number of events for that camera.

### Example

Input:

```python
events = [
    CameraEvent(event_id="e1", camera_id="cam-1", timestamp_millis=1000, adult_count=1, child_count=0),
    CameraEvent(event_id="e2", camera_id="cam-1", timestamp_millis=2000, adult_count=0, child_count=0),
    CameraEvent(event_id="e3", camera_id="cam-2", timestamp_millis=1500, adult_count=0, child_count=0),
]
```

Expected result:

```python
{"cam-1": 2, "cam-2": 1}
```

---

## Exercise 2 — Total people per camera (warm-up)

Still a warm-up. For each camera, add up the number of people it saw across all
of its events, where a single event's people count is `adult_count + child_count`.

Implement:

```python
def total_people_per_camera(events: list[CameraEvent] | None) -> dict[str, int]
```

Rules:

1. If the input list is `None`, return an empty dict.
2. Ignore `None` events.
3. Ignore events where `camera_id` is `None`.
4. Return a mapping from `camera_id` to the summed `adult_count + child_count`
   across that camera's events.

### Example

Input:

```python
events = [
    CameraEvent(event_id="e1", camera_id="cam-1", timestamp_millis=1000, adult_count=2, child_count=1),
    CameraEvent(event_id="e2", camera_id="cam-1", timestamp_millis=2000, adult_count=0, child_count=3),
    CameraEvent(event_id="e3", camera_id="cam-2", timestamp_millis=1500, adult_count=1, child_count=0),
]
```

Expected result:

```python
{"cam-1": 6, "cam-2": 1}   # cam-1: (2+1) + (0+3) = 6,  cam-2: 1+0 = 1
```

---

## Exercise 3 — Deduplicate and aggregate camera events

You receive camera detection events from a queue. Some messages may be
duplicated.

Implement:

```python
def latest_event_by_camera(events: list[CameraEvent] | None) -> dict[str, CameraEvent]
```

Rules:

1. If the input list is `None`, return an empty dict.
2. Ignore `None` events.
3. Ignore events where `event_id` is `None`.
4. Ignore events where `camera_id` is `None`.
5. Ignore duplicate `event_id`.
6. Group events by `camera_id`.
7. For each camera, return the latest event by `timestamp_millis`.
8. If two valid events for the same camera have the same timestamp, keep the one
   that appeared **last** in the input list.

**Important:** if the same `event_id` appears more than once, only the **first**
occurrence counts — even if the duplicate has a newer timestamp, it must be
ignored.

### Example

Input:

```python
events = [
    CameraEvent(event_id="e1", camera_id="cam-1", timestamp_millis=1000, adult_count=0, child_count=0),
    CameraEvent(event_id="e2", camera_id="cam-1", timestamp_millis=2000, adult_count=0, child_count=0),
    CameraEvent(event_id="e3", camera_id="cam-2", timestamp_millis=1500, adult_count=0, child_count=0),
    CameraEvent(event_id="e1", camera_id="cam-1", timestamp_millis=3000, adult_count=0, child_count=0),
]
```

Expected result (a dict of `camera_id` -> `CameraEvent` object):

```python
{
    "cam-1": CameraEvent(event_id="e2", camera_id="cam-1", timestamp_millis=2000, adult_count=0, child_count=0),
    "cam-2": CameraEvent(event_id="e3", camera_id="cam-2", timestamp_millis=1500, adult_count=0, child_count=0),
}
```

The last `e1` is ignored because `event_id="e1"` was already seen.

---

## Exercise 4 — Return aggregation metadata

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

```python
events = [
    CameraEvent(event_id="e1", camera_id="cam-1", timestamp_millis=1000, adult_count=0, child_count=0),
    CameraEvent(event_id="e2", camera_id="cam-1", timestamp_millis=2000, adult_count=0, child_count=0),
    CameraEvent(event_id="e1", camera_id="cam-1", timestamp_millis=3000, adult_count=0, child_count=0),
    CameraEvent(event_id="e2", camera_id="cam-1", timestamp_millis=4000, adult_count=0, child_count=0),
]
```

Expected result:

```python
CameraAggregationResult(
    latest_by_camera={
        "cam-1": CameraEvent(event_id="e2", camera_id="cam-1", timestamp_millis=2000, adult_count=0, child_count=0),
    },
    ignored_duplicate_count=2,
)
```

The second `e1` and the second `e2` are ignored. Note: only ignored **duplicate
event IDs** count — `None`/invalid events do not.

---

## Exercise 5 — Detect child-alone alert windows

You receive detection events for **one** camera as a list of `DetectionEvent`
objects. Events may arrive ordered or unordered.

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

1. If the input is `None` or empty, return `False`.
2. If `window_millis <= 0`, return `False`.
3. Ignore `None` events.
4. Events may arrive out of order — sort them by `timestamp_millis`.
5. If multiple events share the same timestamp, keep the **last** one from the
   original input order.
6. The alert opens only if the child-alone state lasts continuously for at least
   `window_millis`.
7. Any event with `adult_count > 0` breaks the current window.
8. Any event with `child_count == 0` breaks the current window.

### Example 1 — opens

```python
events = [
    DetectionEvent(timestamp_millis=1000, adult_count=0, child_count=1),
    DetectionEvent(timestamp_millis=2000, adult_count=0, child_count=1),
    DetectionEvent(timestamp_millis=3000, adult_count=0, child_count=1),
]
should_open_child_alone_alert(events, window_millis=2000)   # -> True  (3000 - 1000 = 2000)
```

### Example 2 — adult breaks the window

```python
events = [
    DetectionEvent(timestamp_millis=1000, adult_count=0, child_count=1),
    DetectionEvent(timestamp_millis=2000, adult_count=1, child_count=1),
    DetectionEvent(timestamp_millis=3000, adult_count=0, child_count=1),
    DetectionEvent(timestamp_millis=4000, adult_count=0, child_count=1),
]
should_open_child_alone_alert(events, window_millis=2000)   # -> False
```

### Example 3 — duplicate timestamp keeps last input event

```python
events = [
    DetectionEvent(timestamp_millis=1000, adult_count=0, child_count=1),
    DetectionEvent(timestamp_millis=2000, adult_count=0, child_count=1),
    DetectionEvent(timestamp_millis=2000, adult_count=1, child_count=1),
    DetectionEvent(timestamp_millis=3000, adult_count=0, child_count=1),
]
should_open_child_alone_alert(events, window_millis=2000)   # -> False  (last event at 2000 has an adult)
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

1. If `late_tolerance_millis < 0`, return `False`.
2. Normalize duplicate timestamps as before.
3. Sort events as before.
4. Track the gap between consecutive normalized events.
5. If the gap is greater than `late_tolerance_millis`, reset the current
   child-alone window.

---

Good luck — focus on clean, readable code and be ready to talk through your
reasoning (data structures chosen, edge cases, and time complexity).
