from fastapi import APIRouter
from app.schemas.staff_schema import (
    CallNextCustomerResponse,
    StaffQueueSummary
)

router = APIRouter(prefix="/staff", tags=["Staff"])

@router.post("/call-next")
def call_next_customer():
    return CallNextCustomerResponse(
        customer_id=1,
        customer_name="John Smith",
        service_type="License Renewal"
    )

@router.post("/start-service/{customer_id}")
def start_service(customer_id: int):
    return {
        "message": f"Service started for customer {customer_id}"
    }

@router.post("/complete-service/{customer_id}")
def complete_service(customer_id: int):
    return {
        "message": f"Service completed for customer {customer_id}"
    }

@router.get("/summary")
def get_staff_summary():
    return StaffQueueSummary(
        waiting_customers=12,
        customers_in_service=2,
        customers_completed=34
    )