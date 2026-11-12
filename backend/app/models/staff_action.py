from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.db.connection import Base
from app.utils.time_utils import utc_now


class StaffAction(Base):
    __tablename__ = "staff_actions"

    action_id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)

    action_type = Column(String(50), nullable=False)

    timestamp = Column(DateTime, default=utc_now)

    def __repr__(self):
        return (
            f"<StaffAction(id={self.action_id}, "
            f"action='{self.action_type}')>"
        )