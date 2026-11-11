from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.serializers import queue_entry_to_dict
from app.db.connection import get_db
from app.repositories.history_repo import get_recent_actions
from app.schemas.staff_schema import (
    CallNextCustomerResponse,
    StaffActionLog,
    StaffActionResponse,
    StaffQueueSummary,
)
from app.services import staff_service
from app.services.errors import NotFoundError

router = APIRouter(prefix="/staff", tags=["Staff"])


@router.post("/call-next", response_model=CallNextCustomerResponse)
def call_next_customer(db: Session = Depends(get_db)):
    entry = staff_service.call_next_customer(db)

    if not entry:
        raise NotFoundError("No customers are waiting.")

    return queue_entry_to_dict(entry)


@router.post("/start-service/{customer_id}", response_model=StaffActionResponse)
def start_service(customer_id: int, db: Session = Depends(get_db)):
    entry = staff_service.start_service(db, customer_id)

    return {
        "message": f"Service started for customer {customer_id}",
        "customer_id": customer_id,
        "status": entry.status,
    }


@router.post("/complete-service/{customer_id}", response_model=StaffActionResponse)
def complete_service(customer_id: int, db: Session = Depends(get_db)):
    entry = staff_service.complete_service(db, customer_id)

    return {
        "message": f"Service completed for customer {customer_id}",
        "customer_id": customer_id,
        "status": entry.status,
    }


@router.get("/summary", response_model=StaffQueueSummary)
def get_staff_summary(db: Session = Depends(get_db)):
    return staff_service.get_dashboard_summary(db)


@router.get("/history", response_model=list[StaffActionLog])
def get_history(limit: int = 50, db: Session = Depends(get_db)):
    return get_recent_actions(db, limit)
