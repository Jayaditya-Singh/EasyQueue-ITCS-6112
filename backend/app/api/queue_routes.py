from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.serializers import queue_entry_to_dict
from app.db.connection import get_db
from app.schemas.queue_schema import ActiveQueueResponse, QueueMetricsResponse
from app.services import queue_service
from app.services.prediction_service import get_queue_metrics

router = APIRouter(prefix="/queue", tags=["Queue"])


@router.get("/active", response_model=ActiveQueueResponse)
def get_active_queue(db: Session = Depends(get_db)):
    queue = queue_service.get_current_queue(db)

    return {"customers": [queue_entry_to_dict(entry) for entry in queue]}


@router.get("/metrics", response_model=QueueMetricsResponse)
def get_metrics(db: Session = Depends(get_db)):
    return get_queue_metrics(db)
