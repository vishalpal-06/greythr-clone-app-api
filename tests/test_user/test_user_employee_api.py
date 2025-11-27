import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent / "expected_responses/user/employee/"

def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)

# -------------------------------------------------test user api ---------------------------------------------------
def test_user_get_my_details(client, user_token):
    response = client.get(
        "/user/my/me/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    expected = read_json("juniour_employee_response.json")

    assert response.status_code == 200
    assert response.json() == expected

# -------------------------------------------------test manager api ---------------------------------------------------
def test_employee_not_under_manager_by_id(client, user_token):
    response = client.get(
        "/manager/subordinates/id/1",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_employee_not_under_manager_by_email(client, user_token):
    response = client.get(
        "/manager/subordinates/email/manager@test.com/",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_employee_not_under_manager_by_email_not_exist_in_db(client, user_token):
    response = client.get(
        "/manager/subordinates/email/altufaltu@test.com/",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


def test_employee_not_under_manager_by_id_not_exist_in_db(client, user_token):
    response = client.get(
        "/manager/subordinates/id/10",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


# -------------------------------------------------test admin api ---------------------------------------------------
def test_user_get_all_employee(client, user_token):
    response = client.get(
        "/admin/employees/",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_create_employee(client, user_token):
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
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_get_employee_using_id(client, user_token):
    response = client.get(
        "/admin/employees/id/1",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_update_employee_using_id(client, user_token):
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
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_delete_employee_using_id(client, user_token):
    response = client.delete(
        "/admin/employees/id/1",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_get_employee_using_email(client, user_token):
    response = client.get(
        "/admin/employees/email/admin@test.com",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_update_employee_using_email(client, user_token):
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
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_delete_employee_using_email(client, user_token):
    response = client.delete(
        "/admin/employees/email/admin@test.com",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}

