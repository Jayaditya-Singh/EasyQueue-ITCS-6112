from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.repositories.service_repo import get_all_services
from app.schemas.service_schema import ServiceTypeResponse

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("", response_model=list[ServiceTypeResponse])
def list_services(db: Session = Depends(get_db)):
    return get_all_services(db)
