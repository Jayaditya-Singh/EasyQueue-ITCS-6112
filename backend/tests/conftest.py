import os

# Must be set before anything imports app.db.connection. The tests use an
# in-memory SQLite database, so no MySQL server is needed to run them.
os.environ["DATABASE_URL"] = "sqlite://"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.db.connection import Base, SessionLocal, engine  # noqa: E402
from app.db.init_db import init_db  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_database():
    """Every test starts with empty tables plus the default service types."""
    Base.metadata.drop_all(bind=engine)
    init_db()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def check_in(client):
    """Register a customer and put them in line. Returns the join response."""
    def _check_in(name="Test Person", phone="704-555-0100", service="License Renewal"):
        customer = client.post("/customers", json={"name": name, "phone_number": phone})
        assert customer.status_code == 201, customer.text
        joined = client.post(
            "/queue/join",
            json={"customer_id": customer.json()["customer_id"], "service_type": service},
        )
        assert joined.status_code == 201, joined.text
        return joined.json()

    return _check_in
