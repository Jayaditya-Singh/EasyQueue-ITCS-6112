from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.serializers import queue_entry_to_dict
from app.db.connection import get_db
from app.repositories.customer_repo import create_customer, get_customer_by_id
from app.schemas.customer_schema import CustomerCreate, CustomerResponse
from app.schemas.queue_schema import (
    QueueJoinRequest,
    QueueJoinResponse,
    QueueStatusResponse,
)
from app.services import queue_service
from app.services.errors import NotFoundError

router = APIRouter(tags=["Customer"])


@router.post("/customers", response_model=CustomerResponse, status_code=201)
def register_customer(request: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, request.name, request.phone_number)


@router.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer_by_id(db, customer_id)

    if not customer:
        raise NotFoundError("Customer does not exist.")

    return customer


@router.post("/queue/join", response_model=QueueJoinResponse, status_code=201)
def join_queue(request: QueueJoinRequest, db: Session = Depends(get_db)):
    entry = queue_service.join_queue(
        db,
        customer_id=request.customer_id,
        service_id=request.service_id,
        service_type=request.service_type,
    )

    data = queue_entry_to_dict(entry)
    return {
        **data,
        "message": f"You're #{data['position']} in line. "
                   f"Estimated wait: {data['estimated_wait_time']} min.",
    }


@router.get("/queue/status/{customer_id}", response_model=QueueStatusResponse)
def get_queue_status(customer_id: int, db: Session = Depends(get_db)):
    return queue_entry_to_dict(queue_service.get_queue_status(db, customer_id))


@router.delete("/queue/leave/{customer_id}")
def leave_queue(customer_id: int, db: Session = Depends(get_db)):
    queue_service.leave_queue(db, customer_id)

    return {
        "message": f"Customer {customer_id} removed from queue"
    }
