from app.repositories.queue_repo import get_active_queue
from app.models.service_type import ServiceType
from sqlalchemy.orm import Session
from app.config import DEFAULT_SERVICE_DURATION


def get_average_service_duration(
        db: Session,
        service_id : int
):
    service = (
        db.query(ServiceType)
        .filter(ServiceType.service_id == service_id)
        .first()
    )

    if service:
        return service.estimated_duration

    return DEFAULT_SERVICE_DURATION

def estimate_wait_time(
        db: Session,
        position: int,
        service_id: int
):
    avg_duration = get_average_service_duration(db, service_id)

    people_ahead = max(position - 1, 0)

    return people_ahead * avg_duration

def estimate_service_start_time(
        db: Session,
        position: int,
        service_id: int
):
    return estimate_wait_time(db, position, service_id)

def get_queue_metrics(db: Session):
    queue = get_active_queue(db)

    total_customers = len(queue)

    average_wait = 0

    if total_customers > 0:
        wait_times =[
            entry.estimated_wait_time or 0
            for entry in queue
        ]

        average_wait = sum(wait_times) / total_customers

    return {
        "Total customers": total_customers,
        "Average wait time": average_wait
    }