from datetime import datetime

from pydantic import BaseModel, model_validator


class QueueJoinRequest(BaseModel):
    customer_id: int
    # Send either the service name (what the check-in page uses) or its id
    service_type: str | None = None
    service_id: int | None = None

    @model_validator(mode="after")
    def require_service(self):
        if self.service_id is None and not (self.service_type and self.service_type.strip()):
            raise ValueError("Provide service_type or service_id.")
        return self


class QueueStatusResponse(BaseModel):
    queue_id: int
    customer_id: int
    customer_name: str
    service_type: str
    position: int
    people_ahead: int
    estimated_wait_time: int
    status: str
    join_time: datetime | None = None


class QueueJoinResponse(QueueStatusResponse):
    message: str


class ActiveQueueEntry(BaseModel):
    queue_id: int
    customer_id: int
    customer_name: str
    service_type: str
    position: int
    status: str
    estimated_wait_time: int
    join_time: datetime | None = None


class ActiveQueueResponse(BaseModel):
    customers: list[ActiveQueueEntry]


class QueueMetricsResponse(BaseModel):
    total_customers: int
    waiting_customers: int
    average_wait_time: float
    longest_wait_time: int
