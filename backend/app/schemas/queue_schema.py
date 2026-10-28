from pydantic import BaseModel

class QueueJoinRequest(BaseModel):
    customer_id: int
    service_type: str

class QueueStatusResponse(BaseModel):
    customer_id: int
    position: int
    estimated_wait_time: int
    status: str

class ActiveQueueEntry(BaseModel):
    customer_id: int
    customer_name: str
    service_type: str
    position: int
    status: str

class ActiveQueueResponse(BaseModel):
    customers: list[ActiveQueueEntry]