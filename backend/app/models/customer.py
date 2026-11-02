from sqlalchemy import Column, Integer, String
from app.db.connection import Base

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)

    def __repr__(self):
        return f"<Customer(id={self.customer_id}, name='{self.name}')>"