def login(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "organization_id": 1,
            "username": "testuser",
            "password": "correct-horse-battery",
        },
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_liveness(client):
    assert client.get("/health/live").json() == {"status": "alive"}


def test_employee_list_requires_authentication(client):
    assert client.get("/api/v1/employees").status_code == 401


def test_login_rejects_wrong_password(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "organization_id": 1,
            "username": "testuser",
            "password": "incorrect-password",
        },
    )
    assert response.status_code == 401


def test_login_requires_tenant_identifier(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "correct-horse-battery"},
    )
    assert response.status_code == 422


def test_hr_admin_can_list_employees(client):
    response = client.get("/api/v1/employees", headers=login(client))
    assert response.status_code == 200
    assert [item["employee_code"] for item in response.json()] == ["EMP-001"]


def test_hr_admin_can_create_employee(client):
    response = client.post(
        "/api/v1/employees",
        headers=login(client),
        json={
            "employee_code": "EMP-002",
            "first_name": "New",
            "last_name": "Person",
            "email": "new.person@example.com",
            "department": "Engineering",
            "job_title": "Developer",
            "date_joined": "2026-01-01",
        },
    )
    assert response.status_code == 201
    assert response.json()["employee_code"] == "EMP-002"


def test_employee_detail_does_not_leak_other_tenant(client):
    response = client.get("/api/v1/employees/2", headers=login(client))
    assert response.status_code == 404


def test_attendance_checkin_uses_authenticated_employee(client):
    response = client.post("/api/v1/attendance/check-in", headers=login(client))
    assert response.status_code == 200
    assert response.json()["employee_id"] == 1


def test_duplicate_attendance_checkin_is_rejected(client):
    headers = login(client)
    assert client.post("/api/v1/attendance/check-in", headers=headers).status_code == 200
    assert client.post("/api/v1/attendance/check-in", headers=headers).status_code == 409
