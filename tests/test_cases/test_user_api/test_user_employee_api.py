import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent / "expected_responses/user/employee/"

def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)

# -------------------------------------------------test user api ---------------------------------------------------
def test_user_get_my_profile_success(client, user_A1):
    response = client.get(
        "/user/my/me/",
        headers={"Authorization": f"Bearer {user_A1}"}
    )
    expected = read_json("juniour_employee_response.json")

    assert response.status_code == 200
    assert response.json() == expected

# -------------------------------------------------test manager api ---------------------------------------------------
def test_user_access_manager_subordinate_by_id_not_under_manager(client, user_A1):
    response = client.get(
        "/manager/subordinates/id/1",
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_user_access_manager_subordinate_by_email_not_under_manager(client, user_A1):
    response = client.get(
        "/manager/subordinates/email/userA2@test.com/",
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_user_access_manager_subordinate_by_email_not_found(client, user_A1):
    response = client.get(
        "/manager/subordinates/email/altufaltu@test.com/",
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


def test_user_access_manager_subordinate_by_id_not_found(client, user_A1):
    response = client.get(
        "/manager/subordinates/id/10",
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


# -------------------------------------------------test admin api ---------------------------------------------------
def test_user_access_admin_get_all_employees_forbidden(client, user_A1):
    response = client.get(
        "/admin/employees/",
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_access_admin_create_employee_forbidden(client, user_A1):
    payload = {
        "first_name": "string",
        "last_name": "string",
        "email": "string@example.com",
        "joining_date": "2025-11-27",
        "address": "string",
        "isadmin": True,
        "fk_department_id": 1,
        "fk_role_id": 1,
        "fk_manager_id": 1,
        "password": "string"
    }

    response = client.post(
        "/admin/employees/",
        json=payload,
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_access_admin_get_employee_by_id_forbidden(client, user_A1):
    response = client.get(
        "/admin/employees/id/1",
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_access_admin_update_employee_by_id_forbidden(client, user_A1):
    payload = {
        "first_name": "string",
        "last_name": "string",
        "joining_date": "2025-11-27",
        "address": "string",
        "isadmin": True,
        "fk_department_id": 1,
        "fk_role_id": 1,
        "fk_manager_id": 1,
        "password": "string"
    }

    response = client.put(
        "/admin/employees/id/1",
        json=payload,
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_access_admin_delete_employee_by_id_forbidden(client, user_A1):
    response = client.delete(
        "/admin/employees/id/1",
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_access_admin_get_employee_by_email_forbidden(client, user_A1):
    response = client.get(
        "/admin/employees/email/admin@test.com",
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_access_admin_update_employee_by_email_forbidden(client, user_A1):
    payload = {
        "first_name": "string",
        "last_name": "string",
        "joining_date": "2025-11-27",
        "address": "string",
        "isadmin": True,
        "fk_department_id": 1,
        "fk_role_id": 1,
        "fk_manager_id": 1,
        "password": "string"
    }

    response = client.put(
        "/admin/employees/email/admin@test.com",
        json=payload,
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_access_admin_delete_employee_by_email_forbidden(client, user_A1):
    response = client.delete(
        "/admin/employees/email/admin@test.com",
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}

