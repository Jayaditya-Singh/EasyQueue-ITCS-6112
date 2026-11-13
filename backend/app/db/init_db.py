from app.db.connection import Base, SessionLocal, engine

# Imported so their tables are registered on Base.metadata
from app.models.customer import Customer  # noqa: F401
from app.models.queue_entry import QueueEntry  # noqa: F401
from app.models.service_type import ServiceType  # noqa: F401
from app.models.staff_action import StaffAction  # noqa: F401

from app.repositories.service_repo import seed_default_services


def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_default_services(db)
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    print("Database tables created and service types seeded.")
