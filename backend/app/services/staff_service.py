from sqlalchemy.orm import Session

from app.constants.enums import QueueStatus, StaffActionType
from app.repositories.history_repo import log_action
from app.repositories.queue_repo import (
    count_by_status,
    get_queue_entry_by_customer_id,
    get_waiting_queue,
    update_queue_status,
)
from app.services.errors import ConflictError, NotFoundError
from app.services.prediction_service import recalculate_queue


def _change_status(
        db: Session,
        customer_id: int,
        allowed_from: tuple[str, ...],
        new_status: str,
        action: StaffActionType
):
    entry = get_queue_entry_by_customer_id(db, customer_id)

    if not entry:
        raise NotFoundError("Customer is not in the queue.")

    if entry.status not in allowed_from:
        raise ConflictError(
            f"Cannot change status from {entry.status} to {new_status}."
        )

    update_queue_status(db, customer_id, new_status)
    log_action(db, customer_id, action.value)
    recalculate_queue(db)
    db.refresh(entry)

    return entry


def call_next_customer(db: Session):
    """Call the first person who is still WAITING (skips anyone already
    called or being served). Returns None if nobody is waiting."""
    waiting = get_waiting_queue(db)

    if not waiting:
        return None

    return _change_status(
        db,
        waiting[0].customer_id,
        allowed_from=(QueueStatus.WAITING.value,),
        new_status=QueueStatus.CALLED.value,
        action=StaffActionType.CALLED,
    )


def start_service(
        db: Session,
        customer_id: int
):
    return _change_status(
        db,
        customer_id,
        allowed_from=(QueueStatus.WAITING.value, QueueStatus.CALLED.value),
        new_status=QueueStatus.IN_SERVICE.value,
        action=StaffActionType.STARTED_SERVICE,
    )


def complete_service(
        db: Session,
        customer_id: int
):
    return _change_status(
        db,
        customer_id,
        allowed_from=(QueueStatus.CALLED.value, QueueStatus.IN_SERVICE.value),
        new_status=QueueStatus.COMPLETED.value,
        action=StaffActionType.COMPLETED_SERVICE,
    )


def get_dashboard_summary(
        db: Session
):
    # Keys match StaffQueueSummary in app/schemas/staff_schema.py
    return {
        "waiting_customers": count_by_status(db, QueueStatus.WAITING.value),
        "called_customers": count_by_status(db, QueueStatus.CALLED.value),
        "customers_in_service": count_by_status(db, QueueStatus.IN_SERVICE.value),
        "customers_completed": count_by_status(db, QueueStatus.COMPLETED.value),
    }
