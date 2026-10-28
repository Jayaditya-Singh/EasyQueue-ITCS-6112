from fastapi import APIRouter
from app.schemas.queue_schema import (
    ActiveQueueResponse,
    ActiveQueueEntry
)

router = APIRouter(prefix="/queue", tags=["Queue"])

@router.get("/active")
def get_active_queue():
    customers = [
        ActiveQueueEntry(
            customer_id=1,
            customer_name="John Smith",
            service_type="License Renewal",
            position=1,
            status="WAITING"
        ),
        ActiveQueueEntry(
            customer_id=2,
            customer_name="Jane Doe",
            service_type="Real ID",
            position=2,
            status="WAITING"
        )
    ]

    return ActiveQueueResponse(customers=customers)