from pydantic import BaseModel, ConfigDict


class ServiceTypeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    service_id: int
    service_name: str
    estimated_duration: int
