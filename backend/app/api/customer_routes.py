from fastapi import APIRouter
from app.schemas.queue_schema import (
    QueueJoinRequest,
    QueueStatusResponse
)

router = APIRouter(prefix="/queue", tags=["Customer"])

@router.post("/join")
def join_queue(request: QueueJoinRequest):
    return {
        "message": "Customer added to queue",
        "customer_id": request.customer_id,
        "service_type": request.service_type
    }

@router.get("/status/{customer_id}")
def get_queue_status(customer_id: int):
    return QueueStatusResponse(
        customer_id=customer_id,
        position=3,
        estimated_wait_time=25,
        status="WAITING"
    )

@router.delete("/leave/{customer_id}")
def leave_queue(customer_id: int):
    return {
        "message": f"Customer {customer_id} removed from queue"
    }