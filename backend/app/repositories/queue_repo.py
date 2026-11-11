from sqlalchemy.orm import Session
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
    return (
        db.query(QueueEntry)
        .filter(
            QueueEntry.customer_id == customer_id)
        .first()
    )

def get_active_queue(db: Session):
    return (
        db.query(QueueEntry)
        .order_by(QueueEntry.position)
        .all()
    )

def remove_customer_from_queue(
        db: Session,
        customer_id: int
):
    queue_entry = get_queue_entry_by_customer_id(db, customer_id)
    if queue_entry:
        db.delete(queue_entry)
        db.commit()

    return queue_entry

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