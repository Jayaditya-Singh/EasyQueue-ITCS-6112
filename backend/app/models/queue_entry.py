from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.connection import Base
from app.utils.time_utils import utc_now


class QueueEntry(Base):
    __tablename__ = "queue_entries"

    queue_id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)

    service_id = Column(Integer, ForeignKey("service_types.service_id"), nullable=False)

    position = Column(Integer, nullable=False)

    status = Column(String(50), nullable=False, default="WAITING")

    estimated_wait_time = Column(Integer)

    join_time = Column(DateTime, default=utc_now)

    # Python-side links only (no schema change); lets routes read the
    # customer's name and the service name without extra queries
    customer = relationship("Customer")
    service = relationship("ServiceType")

    def __repr__(self):
        return (
            f"<QueueEntry(id={self.queue_id}, "
            f"customer_id={self.customer_id}, "
            f"position={self.position})>"
        )