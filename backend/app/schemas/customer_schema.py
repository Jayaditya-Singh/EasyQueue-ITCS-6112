from pydantic import BaseModel

class CustomerCreate(BaseModel):
    name: str
    phone_number: str

class CustomerResponse(BaseModel):
    customer_id: int
    name: str
    phone_number: str