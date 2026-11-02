from app.db.connection import Base, engine

from app.models.customer import Customer
from app.models.queue_entry import QueueEntry
from app.models.service_type import ServiceType
from app.models.staff_action import StaffAction


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")