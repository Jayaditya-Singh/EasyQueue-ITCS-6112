from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import DEFAULT_SERVICE_TYPES
from app.models.service_type import ServiceType


def get_all_services(db: Session):
    return db.query(ServiceType).order_by(ServiceType.service_id).all()


def get_service_by_id(db: Session, service_id: int):
    return (
        db.query(ServiceType)
        .filter(ServiceType.service_id == service_id)
        .first()
    )


def get_service_by_name(db: Session, service_name: str):
    """Case-insensitive, so "Real ID" and "real id" match the same row."""
    return (
        db.query(ServiceType)
        .filter(func.lower(ServiceType.service_name) == service_name.strip().lower())
        .first()
    )


def seed_default_services(db: Session):
    """Insert the default DMV services if the table is empty."""
    if db.query(ServiceType).count() > 0:
        return

    for name, duration in DEFAULT_SERVICE_TYPES:
        db.add(ServiceType(service_name=name, estimated_duration=duration))

    db.commit()
