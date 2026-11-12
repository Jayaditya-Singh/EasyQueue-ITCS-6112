from sqlalchemy.orm import Session

from app.config import DEFAULT_SERVICE_DURATION
from app.constants.enums import QueueStatus
from app.repositories.queue_repo import get_active_queue
from app.repositories.service_repo import get_service_by_id


def get_average_service_duration(
        db: Session,
        service_id: int
):
    service = get_service_by_id(db, service_id)

    if service and service.estimated_duration:
        return service.estimated_duration

    return DEFAULT_SERVICE_DURATION


def entry_duration(entry) -> int:
    if entry.service and entry.service.estimated_duration:
        return entry.service.estimated_duration

    return DEFAULT_SERVICE_DURATION


def estimate_wait_for_entries_ahead(entries_ahead) -> int:
    """Wait time = total expected service time of everyone ahead in line.

    Uses each person's own service duration, so someone behind a Driving Test
    (30 min) waits longer than someone behind a License Renewal (10 min).
    """
    return sum(entry_duration(entry) for entry in entries_ahead)


def estimate_wait_time(
        db: Session,
        position: int,
        service_id: int
):
    """Estimated wait for a new spot at `position` (1 = front of the line)."""
    queue = get_active_queue(db)
    people_ahead = max(position - 1, 0)

    return estimate_wait_for_entries_ahead(queue[:people_ahead])


def estimate_service_start_time(
        db: Session,
        position: int,
        service_id: int
):
    return estimate_wait_time(db, position, service_id)


def recalculate_queue(db: Session):
    """Renumber positions 1..n with no gaps and refresh every wait estimate.

    Called whenever someone joins, leaves, or changes status.
    """
    queue = get_active_queue(db)

    for index, entry in enumerate(queue):
        entry.position = index + 1

        if entry.status == QueueStatus.WAITING.value:
            entry.estimated_wait_time = estimate_wait_for_entries_ahead(queue[:index])
        else:
            # Already called or being served: nothing left to wait for
            entry.estimated_wait_time = 0

    db.commit()

    return queue


def get_queue_metrics(db: Session):
    queue = get_active_queue(db)
    waiting = [e for e in queue if e.status == QueueStatus.WAITING.value]

    average_wait = 0.0
    if waiting:
        average_wait = sum(e.estimated_wait_time or 0 for e in waiting) / len(waiting)

    return {
        "total_customers": len(queue),
        "waiting_customers": len(waiting),
        "average_wait_time": round(average_wait, 1),
        "longest_wait_time": max((e.estimated_wait_time or 0 for e in waiting), default=0),
    }
