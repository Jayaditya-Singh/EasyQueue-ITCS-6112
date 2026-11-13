from sqlalchemy.orm import Session
from app.models.customer import Customer

def create_customer(db: Session, name: str, phone_number: str):
    customer = Customer(
        name=name,
        phone_number=phone_number
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer

def get_customer_by_id(db: Session, customer_id: int):
    return (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )

def get_all_customers(db: Session):
    return db.query(Customer).all()

def delete_customer(db: Session, customer_id: int):
    customer = get_customer_by_id(db, customer_id)

    if customer:
        db.delete(customer)
        db.commit()

    return customer