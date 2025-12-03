import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent / "expected_responses/admin/employee/"

def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)

# -------------------------------------------------Test User API ---------------------------------------------------
def test_admin_get_my_profile_success(client, admin_user):
    response = client.get(
        "/user/my/me/",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_my_details_admin.json")

    assert response.status_code == 200
    assert response.json() == expected

# -------------------------------------------------Test Manager API ---------------------------------------------------
def test_admin_access_manager_subordinate_by_id_under_manager(client, admin_user):
    response = client.get(
        "/manager/subordinates/id/2",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_subordinate_employee_details_by_id_admin.json")

    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_manager_subordinate_by_id_not_under_manager(client, admin_user):
    response = client.get(
        "/manager/subordinates/id/6",
        headers={"Authorization": f"Bearer {admin_user}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_admin_access_manager_subordinate_by_id_not_found(client, admin_user):
    response = client.get(
        "/manager/subordinates/id/10",
        headers={"Authorization": f"Bearer {admin_user}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


def test_admin_access_manager_subordinate_by_email_under_manager(client, admin_user):
    response = client.get(
        "/manager/subordinates/email/managerA@test.com/",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_subordinate_employee_details_by_email_admin.json")

    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_manager_subordinate_by_email_not_under_manager(client, admin_user):
    response = client.get(
        "/manager/subordinates/email/userB2@test.com/",
        headers={"Authorization": f"Bearer {admin_user}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_admin_access_manager_subordinate_by_email_not_found(client, admin_user):
    response = client.get(
        "/manager/subordinates/email/altufaltu@test.com/",
        headers={"Authorization": f"Bearer {admin_user}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_admin_access_admin_get_all_employees_success(client, admin_user):
    response = client.get(
        "/admin/employees/",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_all_employee_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_admin_create_employee_success(client, admin_user):
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
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("create_employee_admin.json")

    assert response.status_code == 201
    assert response.json() == expected


def test_admin_access_admin_create_employee_duplicate_email_conflict(client, admin_user):
    payload = {
        "first_name": "string",
        "last_name": "string",
        "email": "userB2@test.com",
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
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 409
    assert response.json() == {"detail":"Employee with this email already exists"}


def test_admin_access_admin_get_employee_by_id_success(client, admin_user):
    response = client.get(
        "/admin/employees/id/1",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_employee_details_by_id.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_admin_get_employee_by_id_not_found(client, admin_user):
    response = client.get(
        "/admin/employees/id/10",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


def test_admin_access_admin_update_employee_by_id_success(client, admin_user):
    payload = {
        "first_name": "string",
        "last_name": "string",
        "joining_date": "2025-11-27",
        "address": "string",
        "isadmin": True,
        "fk_department_id": 1,
        "fk_role_id": 1,
    }

    response = client.put(
        "/admin/employees/id/4",
        json=payload,
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("update_employee_details_by_id.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_admin_update_employee_by_id_not_found(client, admin_user):
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
        "/admin/employees/id/14",
        json=payload,
        headers={"Authorization": f"Bearer {admin_user}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


def test_admin_access_admin_delete_employee_by_id_success(client, admin_user):
    response = client.delete(
        "/admin/employees/id/3",
        headers={"Authorization": f"Bearer {admin_user}"}
    )

    assert response.status_code == 200
    assert response.json() == {"detail": "Employee deleted successfully"}


def test_admin_access_admin_delete_employee_by_id_not_found(client, admin_user):
    response = client.delete(
        "/admin/employees/id/13",
        headers={"Authorization": f"Bearer {admin_user}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


def test_admin_access_admin_get_employee_by_email_success(client, admin_user):
    response = client.get(
        "/admin/employees/email/admin@test.com",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_employee_details_by_email.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_admin_get_employee_by_email_not_found(client, admin_user):
    response = client.get(
        "/admin/employees/email/admin2@test.com",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


def test_admin_access_admin_update_employee_by_email_success(client, admin_user):
    payload = {
        "first_name": "string",
        "last_name": "string",
        "joining_date": "2025-11-27",
        "address": "string",
        "isadmin": True,
        "fk_department_id": 1,
        "fk_role_id": 1,
    }

    response = client.put(
        "/admin/employees/email/userA1@test.com",
        json=payload,
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("update_employee_details_by_email.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_admin_update_employee_by_email_not_found(client, admin_user):
    payload = {
        "first_name": "string",
        "last_name": "string",
        "joining_date": "2025-11-27",
        "address": "string",
        "isadmin": True,
        "fk_department_id": 1,
        "fk_role_id": 1,
    }

    response = client.put(
        "/admin/employees/email/userA3@test.com",
        json=payload,
        headers={"Authorization": f"Bearer {admin_user}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


def test_admin_access_admin_delete_employee_by_email_success(client, admin_user):
    response = client.delete(
        "/admin/employees/email/userA1@test.com",
        headers={"Authorization": f"Bearer {admin_user}"}
    )

    assert response.status_code == 200
    assert response.json() == {"detail": "Employee deleted successfully"}


def test_admin_access_admin_delete_employee_by_email_not_found(client, admin_user):
    response = client.delete(
        "/admin/employees/email/user_A5@test.com",
        headers={"Authorization": f"Bearer {admin_user}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}

