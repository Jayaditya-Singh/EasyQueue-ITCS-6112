from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CallNextCustomerResponse(BaseModel):
    customer_id: int
    customer_name: str
    service_type: str
    position: int
    status: str


class StaffActionResponse(BaseModel):
    message: str
    customer_id: int
    status: str


class StaffQueueSummary(BaseModel):
    waiting_customers: int
    called_customers: int
    customers_in_service: int
    customers_completed: int


class StaffActionLog(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    action_id: int
    customer_id: int
    action_type: str
    timestamp: datetime
