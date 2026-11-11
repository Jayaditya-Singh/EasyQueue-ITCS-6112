from sqlalchemy.orm import Session

from app.repositories.customer_repo import (
    get_customer_by_id
)

from app.repositories.queue_repo import (
    add_customer_to_queue,
    get_queue_entry_by_customer_id,
    get_active_queue,
    remove_customer_from_queue
)

from app.services.prediction_service import (
    estimate_wait_time
)


def join_queue(
        db: Session,
        customer_id: int,
        service_id: int
):
    customer = get_customer_by_id(
        db,
        customer_id
    )

    if not customer:
        raise ValueError("Customer does not exist.")

    active_queue = get_active_queue(db)

    position = len(active_queue) + 1

    estimated_wait = estimate_wait_time(
        db,
        position,
        service_id
    )

    return add_customer_to_queue(
        db=db,
        customer_id=customer_id,
        service_id=service_id,
        position=position,
        estimated_wait_time=estimated_wait
    )


def leave_queue(
        db: Session,
        customer_id: int
):
    return remove_customer_from_queue(db, customer_id)


def get_queue_status(
        db: Session,
        customer_id: int
):
    return get_queue_entry_by_customer_id(db, customer_id)


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