from sqlalchemy.orm import Session

from app.constants.enums import QueueStatus, StaffActionType
from app.repositories.customer_repo import get_customer_by_id
from app.repositories.history_repo import log_action
from app.repositories.queue_repo import (
    add_customer_to_queue,
    get_active_queue,
    get_latest_queue_entry_by_customer_id,
    get_queue_entry_by_customer_id,
    remove_customer_from_queue,
)
from app.repositories.service_repo import get_service_by_id, get_service_by_name
from app.services.errors import ConflictError, NotFoundError
from app.services.prediction_service import estimate_wait_time, recalculate_queue


def resolve_service(
        db: Session,
        service_id: int | None = None,
        service_type: str | None = None
):
    """Find a service by id or by name (the frontend sends the name)."""
    service = None

    if service_id is not None:
        service = get_service_by_id(db, service_id)
    elif service_type:
        service = get_service_by_name(db, service_type)

    if not service:
        raise NotFoundError(f"Unknown service: {service_type or service_id}")

    return service


def join_queue(
        db: Session,
        customer_id: int,
        service_id: int | None = None,
        service_type: str | None = None
):
    customer = get_customer_by_id(db, customer_id)

    if not customer:
        raise NotFoundError("Customer does not exist.")

    if get_queue_entry_by_customer_id(db, customer_id):
        raise ConflictError("Customer is already in the queue.")

    service = resolve_service(db, service_id, service_type)

    position = len(get_active_queue(db)) + 1

    entry = add_customer_to_queue(
        db=db,
        customer_id=customer_id,
        service_id=service.service_id,
        position=position,
        estimated_wait_time=estimate_wait_time(db, position, service.service_id)
    )

    recalculate_queue(db)
    db.refresh(entry)

    return entry


def leave_queue(
        db: Session,
        customer_id: int
):
    entry = remove_customer_from_queue(db, customer_id)

    if not entry:
        raise NotFoundError("Customer is not in the queue.")

    log_action(db, customer_id, StaffActionType.CUSTOMER_LEFT.value)
    recalculate_queue(db)

    return entry


def get_queue_status(
        db: Session,
        customer_id: int
):
    """The customer's current entry, or their last one if they already left
    or were served (so the status page can say "COMPLETED")."""
    entry = (
        get_queue_entry_by_customer_id(db, customer_id)
        or get_latest_queue_entry_by_customer_id(db, customer_id)
    )

    if not entry:
        raise NotFoundError("Customer has no queue entry.")

    return entry


def get_current_queue(
        db: Session
):
    return get_active_queue(db)


def get_customer_position(
        db: Session,
        customer_id: int
):
    queue_entry = get_queue_entry_by_customer_id(db, customer_id)

    if not queue_entry:
        return None

    return queue_entry.position


def get_estimated_wait_time(
        db: Session,
        customer_id: int
):
    queue_entry = get_queue_entry_by_customer_id(db, customer_id)

    if not queue_entry:
        return None

    return queue_entry.estimated_wait_time
