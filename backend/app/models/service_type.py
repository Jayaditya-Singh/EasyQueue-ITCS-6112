from sqlalchemy import Column, Integer, String

from app.db.connection import Base

class ServiceType(Base):
    __tablename__ = ("service_types")

    service_id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(100), nullable=False, unique=True)
    estimated_duration = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<ServiceType(id={self.service_id}, service='{self.service_name}')>"
