"""End-to-end tests of the HTTP endpoints the frontend calls."""


def test_root(client):
    assert client.get("/").json() == {"message": "EasyQueue API Running"}


def test_services_are_seeded(client):
    response = client.get("/services")

    assert response.status_code == 200
    names = [s["service_name"] for s in response.json()]
    assert "License Renewal" in names
    assert "Real ID" in names


def test_create_and_get_customer(client):
    response = client.post(
        "/customers", json={"name": "  Jane   Doe ", "phone_number": "(704) 555-1234"}
    )

    assert response.status_code == 201
    customer = response.json()
    assert customer["name"] == "Jane Doe"
    assert customer["phone_number"] == "7045551234"

    fetched = client.get(f"/customers/{customer['customer_id']}")
    assert fetched.json() == customer


def test_create_customer_rejects_bad_phone(client):
    response = client.post("/customers", json={"name": "Jane", "phone_number": "12345"})
    assert response.status_code == 422


def test_create_customer_rejects_blank_name(client):
    response = client.post("/customers", json={"name": "   ", "phone_number": "7045551234"})
    assert response.status_code == 422


def test_get_missing_customer_is_404(client):
    assert client.get("/customers/999").status_code == 404


def test_join_queue_returns_position_and_wait(check_in):
    first = check_in(name="First", service="Driving Test")
    second = check_in(name="Second", phone="7045550101", service="Real ID")

    assert first["position"] == 1
    assert first["estimated_wait_time"] == 0
    assert first["customer_name"] == "First"
    assert first["service_type"] == "Driving Test"
    assert "message" in first

    assert second["position"] == 2
    assert second["people_ahead"] == 1
    # Waits behind one 30-minute Driving Test
    assert second["estimated_wait_time"] == 30


def test_join_queue_service_name_is_case_insensitive(client):
    customer = client.post(
        "/customers", json={"name": "A", "phone_number": "7045550100"}
    ).json()
    response = client.post(
        "/queue/join",
        json={"customer_id": customer["customer_id"], "service_type": "real id"},
    )

    assert response.status_code == 201
    assert response.json()["service_type"] == "Real ID"


def test_join_queue_unknown_customer_is_404(client):
    response = client.post(
        "/queue/join", json={"customer_id": 999, "service_type": "Real ID"}
    )
    assert response.status_code == 404


def test_join_queue_unknown_service_is_404(client):
    customer = client.post(
        "/customers", json={"name": "A", "phone_number": "7045550100"}
    ).json()
    response = client.post(
        "/queue/join",
        json={"customer_id": customer["customer_id"], "service_type": "Fishing License"},
    )
    assert response.status_code == 404


def test_join_queue_requires_a_service(client):
    response = client.post("/queue/join", json={"customer_id": 1})
    assert response.status_code == 422


def test_cannot_join_twice(client, check_in):
    entry = check_in()
    response = client.post(
        "/queue/join",
        json={"customer_id": entry["customer_id"], "service_type": "Real ID"},
    )
    assert response.status_code == 409


def test_queue_status(client, check_in):
    entry = check_in()
    response = client.get(f"/queue/status/{entry['customer_id']}")

    assert response.status_code == 200
    assert response.json()["status"] == "WAITING"
    assert response.json()["position"] == 1


def test_queue_status_unknown_customer_is_404(client):
    assert client.get("/queue/status/999").status_code == 404


def test_leave_queue(client, check_in):
    entry = check_in()

    response = client.delete(f"/queue/leave/{entry['customer_id']}")
    assert response.status_code == 200

    assert client.get("/queue/active").json()["customers"] == []
    assert client.get(f"/queue/status/{entry['customer_id']}").json()["status"] == "CANCELED"
    # Leaving twice is an error, not a silent success
    assert client.delete(f"/queue/leave/{entry['customer_id']}").status_code == 404


def test_active_queue_lists_people_in_order(client, check_in):
    check_in(name="Alice", phone="7045550001")
    check_in(name="Bob", phone="7045550002", service="Real ID")

    customers = client.get("/queue/active").json()["customers"]

    assert [c["customer_name"] for c in customers] == ["Alice", "Bob"]
    assert [c["position"] for c in customers] == [1, 2]
    assert customers[1]["service_type"] == "Real ID"
    assert customers[0]["join_time"].endswith(("Z", "+00:00"))


def test_full_staff_workflow(client, check_in):
    alice = check_in(name="Alice", phone="7045550001")
    bob = check_in(name="Bob", phone="7045550002")

    called = client.post("/staff/call-next")
    assert called.status_code == 200
    assert called.json()["customer_id"] == alice["customer_id"]
    assert called.json()["status"] == "CALLED"

    # Call-next skips Alice, who was already called
    assert client.post("/staff/call-next").json()["customer_id"] == bob["customer_id"]

    started = client.post(f"/staff/start-service/{alice['customer_id']}")
    assert started.status_code == 200
    assert started.json()["status"] == "IN_SERVICE"

    completed = client.post(f"/staff/complete-service/{alice['customer_id']}")
    assert completed.status_code == 200
    assert completed.json()["status"] == "COMPLETED"

    summary = client.get("/staff/summary").json()
    assert summary == {
        "waiting_customers": 0,
        "called_customers": 1,
        "customers_in_service": 0,
        "customers_completed": 1,
    }

    # Alice is gone from the active queue and Bob moved up
    active = client.get("/queue/active").json()["customers"]
    assert [(c["customer_name"], c["position"]) for c in active] == [("Bob", 1)]

    history = client.get("/staff/history").json()
    assert {h["action_type"] for h in history} == {"CALLED", "STARTED_SERVICE", "COMPLETED_SERVICE"}


def test_call_next_with_empty_queue_is_404(client):
    assert client.post("/staff/call-next").status_code == 404


def test_cannot_complete_someone_still_waiting(client, check_in):
    entry = check_in()
    response = client.post(f"/staff/complete-service/{entry['customer_id']}")
    assert response.status_code == 409


def test_staff_actions_on_unknown_customer_are_404(client):
    assert client.post("/staff/start-service/999").status_code == 404
    assert client.post("/staff/complete-service/999").status_code == 404


def test_returning_customer_can_rejoin(client, check_in):
    entry = check_in()
    cid = entry["customer_id"]
    client.post(f"/staff/start-service/{cid}")
    client.post(f"/staff/complete-service/{cid}")

    rejoin = client.post("/queue/join", json={"customer_id": cid, "service_type": "Real ID"})

    assert rejoin.status_code == 201
    status = client.get(f"/queue/status/{cid}").json()
    assert status["status"] == "WAITING"
    assert status["service_type"] == "Real ID"


def test_queue_metrics(client, check_in):
    check_in(name="A", phone="7045550001", service="Driving Test")  # waits 0
    check_in(name="B", phone="7045550002", service="Real ID")       # waits 30

    metrics = client.get("/queue/metrics").json()

    assert metrics["total_customers"] == 2
    assert metrics["waiting_customers"] == 2
    assert metrics["average_wait_time"] == 15.0
    assert metrics["longest_wait_time"] == 30
