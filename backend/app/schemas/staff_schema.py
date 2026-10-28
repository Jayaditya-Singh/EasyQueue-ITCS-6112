from pydantic import BaseModel

class CallNextCustomerResponse(BaseModel):
    customer_id: int
    customer_name: str
    service_type: str

class StartServiceRequest(BaseModel):
    customer_id: int

class CompleteServiceRequest(BaseModel):
    customer_id: int

class StaffQueueSummary(BaseModel):
    waiting_customers: int
    customers_in_service: int
    customers_completed: int