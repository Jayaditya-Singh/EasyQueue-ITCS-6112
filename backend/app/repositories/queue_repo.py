from sqlalchemy.orm import Session

from app.constants.enums import ACTIVE_STATUSES, QueueStatus
from app.models.queue_entry import QueueEntry


def add_customer_to_queue(
        db: Session,
        customer_id: int,
        service_id: int,
        position: int,
        estimated_wait_time: int
):
    queue_entry = QueueEntry(
        customer_id=customer_id,
        service_id=service_id,
        position=position,
        status=QueueStatus.WAITING.value,
        estimated_wait_time=estimated_wait_time
    )

    db.add(queue_entry)
    db.commit()
    db.refresh(queue_entry)

    return queue_entry


def get_queue_entry_by_customer_id(
        db: Session,
        customer_id: int
):
    """The customer's current spot in line, or None if they are not in line.

    A customer can have old COMPLETED/CANCELED entries from earlier visits,
    so only active entries are considered, newest first.
    """
    return (
        db.query(QueueEntry)
        .filter(
            QueueEntry.customer_id == customer_id,
            QueueEntry.status.in_(ACTIVE_STATUSES)
        )
        .order_by(QueueEntry.queue_id.desc())
        .first()
    )


def get_latest_queue_entry_by_customer_id(
        db: Session,
        customer_id: int
):
    """The customer's most recent entry, whatever its status."""
    return (
        db.query(QueueEntry)
        .filter(QueueEntry.customer_id == customer_id)
        .order_by(QueueEntry.queue_id.desc())
        .first()
    )


def get_active_queue(db: Session):
    """Everyone still in line (waiting, called, or being served), in order."""
    return (
        db.query(QueueEntry)
        .filter(QueueEntry.status.in_(ACTIVE_STATUSES))
        .order_by(QueueEntry.position, QueueEntry.queue_id)
        .all()
    )


def get_waiting_queue(db: Session):
    return (
        db.query(QueueEntry)
        .filter(QueueEntry.status == QueueStatus.WAITING.value)
        .order_by(QueueEntry.position, QueueEntry.queue_id)
        .all()
    )


def count_by_status(db: Session, status: str):
    return (
        db.query(QueueEntry)
        .filter(QueueEntry.status == status)
        .count()
    )


def remove_customer_from_queue(
        db: Session,
        customer_id: int
):
    """Take a customer out of line. The row is kept (marked CANCELED) so the
    visit still shows up in history."""
    return update_queue_status(db, customer_id, QueueStatus.CANCELED.value)


def update_queue_position(
        db: Session,
        customer_id: int,
        new_position: int
):
    queue_entry = get_queue_entry_by_customer_id(db, customer_id)

    if queue_entry:
        queue_entry.position = new_position
        db.commit()
        db.refresh(queue_entry)

    return queue_entry


def update_queue_status(
        db: Session,
        customer_id: int,
        new_status: str
):
    queue_entry = get_queue_entry_by_customer_id(db, customer_id)
    if queue_entry:
        queue_entry.status = new_status
        db.commit()
        db.refresh(queue_entry)

    return queue_entry
