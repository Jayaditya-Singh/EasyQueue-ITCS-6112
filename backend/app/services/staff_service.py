from sqlalchemy.orm import Session

from app.repositories.queue_repo import (
    get_active_queue,
    update_queue_status
)

from app.repositories.customer_repo import (
    get_customer_by_id
)


def call_next_customer(db: Session):
    queue = get_active_queue(db)

    if not queue:
        return None

    next_customer = queue[0]

    update_queue_status(
        db,
        next_customer.customer_id,
        "CALLED"
    )

    return next_customer


def start_service(
        db: Session,
        customer_id: int
):
    customer = get_customer_by_id(db, customer_id)

    if not customer:
        raise ValueError(
            "Customer not found."
        )

    return update_queue_status(
        db,
        customer_id,
        "IN_SERVICE"
    )


def complete_service(
        db: Session,
        customer_id: int
):
    customer = get_customer_by_id(db, customer_id)

    if not customer:
        raise ValueError(
            "Customer not found."
        )

    return update_queue_status(
        db,
        customer_id,
        "COMPLETED"
    )


def get_dashboard_summary(
        db: Session
):
    queue = get_active_queue(db)

    waiting = 0
    called = 0
    in_service = 0
    completed = 0

    for entry in queue:

        if entry.status == "WAITING":
            waiting += 1

        elif entry.status == "CALLED":
            called += 1

        elif entry.status == "IN_SERVICE":
            in_service += 1

        elif entry.status == "COMPLETED":
            completed += 1

    return {
        "waiting_customers": waiting,
        "called_customers": called,
        "customers_in_service": in_service,
        "completed_customers": completed
    }