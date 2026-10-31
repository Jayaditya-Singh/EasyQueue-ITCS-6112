from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from datetime import datetime

from app.db.connection import Base


class QueueEntry(Base):
    __tablename__ = "queue_entries"

    queue_id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)

    service_id = Column(Integer, ForeignKey("service_types.service_id"), nullable=False)

    position = Column(Integer, nullable=False)

    status = Column(String(50), nullable=False, default="WAITING")

    estimated_wait_time = Column(Integer)

    join_time = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (
            f"<QueueEntry(id={self.queue_id}, "
            f"customer_id={self.customer_id}, "
            f"position={self.position})>"
        )