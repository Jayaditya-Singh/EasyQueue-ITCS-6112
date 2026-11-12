"""Wait-time estimate tests."""
from app.config import DEFAULT_SERVICE_DURATION
from app.repositories.customer_repo import create_customer
from app.services import queue_service, staff_service
from app.services.prediction_service import (
    get_average_service_duration,
    get_queue_metrics,
)
from app.repositories.service_repo import get_service_by_name


def _join(db, name, phone, service):
    customer = create_customer(db, name, phone)
    return queue_service.join_queue(db, customer.customer_id, service_type=service)


def test_service_duration_comes_from_service_type(db):
    real_id = get_service_by_name(db, "Real ID")
    assert get_average_service_duration(db, real_id.service_id) == 20


def test_unknown_service_uses_default_duration(db):
    assert get_average_service_duration(db, 999) == DEFAULT_SERVICE_DURATION


def test_wait_is_sum_of_service_times_ahead(db):
    _join(db, "A", "7045550001", "Driving Test")     # 30 min
    _join(db, "B", "7045550002", "License Renewal")  # 10 min
    c = _join(db, "C", "7045550003", "Real ID")

    assert queue_service.get_estimated_wait_time(db, c.customer_id) == 40


def test_waits_shrink_when_people_ahead_finish(db):
    a = _join(db, "A", "7045550001", "Driving Test")
    b = _join(db, "B", "7045550002", "License Renewal")

    assert queue_service.get_estimated_wait_time(db, b.customer_id) == 30

    staff_service.start_service(db, a.customer_id)
    staff_service.complete_service(db, a.customer_id)

    assert queue_service.get_estimated_wait_time(db, b.customer_id) == 0


def test_called_customers_have_zero_wait(db):
    a = _join(db, "A", "7045550001", "Real ID")
    staff_service.call_next_customer(db)

    assert queue_service.get_estimated_wait_time(db, a.customer_id) == 0


def test_metrics_on_empty_queue(db):
    assert get_queue_metrics(db) == {
        "total_customers": 0,
        "waiting_customers": 0,
        "average_wait_time": 0.0,
        "longest_wait_time": 0,
    }
