"""Service-layer tests for queue ordering and status rules."""
import pytest

from app.repositories.customer_repo import create_customer
from app.services import queue_service, staff_service
from app.services.errors import ConflictError, NotFoundError


def _join(db, name, phone, service="License Renewal"):
    customer = create_customer(db, name, phone)
    return queue_service.join_queue(db, customer.customer_id, service_type=service)


def test_positions_close_gaps_when_someone_leaves(db):
    a = _join(db, "A", "7045550001")
    b = _join(db, "B", "7045550002")
    c = _join(db, "C", "7045550003")

    queue_service.leave_queue(db, b.customer_id)

    queue = queue_service.get_current_queue(db)
    assert [(e.customer_id, e.position) for e in queue] == [
        (a.customer_id, 1),
        (c.customer_id, 2),
    ]


def test_completed_customers_do_not_take_up_positions(db):
    a = _join(db, "A", "7045550001")
    staff_service.start_service(db, a.customer_id)
    staff_service.complete_service(db, a.customer_id)

    # Before the fix, new joins were numbered after every entry ever created
    b = _join(db, "B", "7045550002")
    assert b.position == 1


def test_call_next_returns_none_when_nobody_waiting(db):
    assert staff_service.call_next_customer(db) is None


def test_start_service_twice_is_a_conflict(db):
    a = _join(db, "A", "7045550001")
    staff_service.start_service(db, a.customer_id)

    with pytest.raises(ConflictError):
        staff_service.start_service(db, a.customer_id)


def test_leave_when_not_in_queue(db):
    with pytest.raises(NotFoundError):
        queue_service.leave_queue(db, 999)


def test_summary_counts_each_status(db):
    a = _join(db, "A", "7045550001")
    b = _join(db, "B", "7045550002")
    _join(db, "C", "7045550003")
    staff_service.start_service(db, a.customer_id)
    staff_service.call_next_customer(db)  # calls B

    assert staff_service.get_dashboard_summary(db) == {
        "waiting_customers": 1,
        "called_customers": 1,
        "customers_in_service": 1,
        "customers_completed": 0,
    }
    assert queue_service.get_customer_position(db, b.customer_id) == 2
