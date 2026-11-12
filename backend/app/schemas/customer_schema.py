from pydantic import BaseModel, ConfigDict, field_validator

from app.utils.validators import clean_name, normalize_phone_number


class CustomerCreate(BaseModel):
    name: str
    phone_number: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return clean_name(value)

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        return normalize_phone_number(value)


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int
    name: str
    phone_number: str
