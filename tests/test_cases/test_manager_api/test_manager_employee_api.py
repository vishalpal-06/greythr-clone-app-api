import json
from pathlib import Path

BASE_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "expected_responses/manager/employee/"
)


def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)


# -------------------------------------------------Test User API ---------------------------------------------------
def test_manager_get_my_profile_success(client, manager_A):
    response = client.get(
        "/user/my/me/", headers={"Authorization": f"Bearer {manager_A}"}
    )
    expected = read_json("get_my_details_manager_A.json")

    assert response.status_code == 200
    assert response.json() == expected


# -------------------------------------------------Test Manager API ---------------------------------------------------
def test_manager_manager_access_get_subordinate_by_id_success(client, manager_A):
    response = client.get(
        "/manager/subordinates/id/4", headers={"Authorization": f"Bearer {manager_A}"}
    )
    expected = read_json("get_subordinate_employee_details_by_id_manager_A.json")

    assert response.status_code == 200
    assert response.json() == expected


def test_manager_manager_access_get_subordinate_by_id_nonsubordinate(client, manager_A):
    response = client.get(
        "/manager/subordinates/id/6", headers={"Authorization": f"Bearer {manager_A}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_manager_manager_access_get_subordinate_by_email_success(client, manager_A):
    response = client.get(
        "/manager/subordinates/email/userA2@test.com/",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("get_subordinate_employee_details_by_email_manager_A.json")

    assert response.status_code == 200
    assert response.json() == expected


def test_manager_manager_access_get_subordinate_by_email_nonsubordinate(
    client, manager_A
):
    response = client.get(
        "/manager/subordinates/email/userB2@test.com/",
        headers={"Authorization": f"Bearer {manager_A}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_manager_manager_access_get_subordinate_by_email_not_found(client, manager_A):
    response = client.get(
        "/manager/subordinates/email/altufaltu@test.com/",
        headers={"Authorization": f"Bearer {manager_A}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


def test_manager_manager_access_get_subordinate_by_id_not_found(client, manager_A):
    response = client.get(
        "/manager/subordinates/id/10", headers={"Authorization": f"Bearer {manager_A}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_manager_admin_access_get_all_employees_forbidden(client, manager_A):
    response = client.get(
        "/admin/employees/", headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_create_employee_forbidden(client, manager_A):
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
        "password": "string",
    }
    response = client.post(
        "/admin/employees/",
        json=payload,
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_get_employee_by_id_forbidden(client, manager_A):
    response = client.get(
        "/admin/employees/id/1", headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_update_employee_by_id_forbidden(client, manager_A):
    payload = {
        "first_name": "string",
        "last_name": "string",
        "joining_date": "2025-11-27",
        "address": "string",
        "isadmin": True,
        "fk_department_id": 1,
        "fk_role_id": 1,
        "fk_manager_id": 1,
        "password": "string",
    }
    response = client.put(
        "/admin/employees/id/1",
        json=payload,
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_delete_employee_by_id_forbidden(client, manager_A):
    response = client.delete(
        "/admin/employees/id/1", headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_get_employee_by_email_forbidden(client, manager_A):
    response = client.get(
        "/admin/employees/email/admin@test.com",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_update_employee_by_email_forbidden(client, manager_A):
    payload = {
        "first_name": "string",
        "last_name": "string",
        "joining_date": "2025-11-27",
        "address": "string",
        "isadmin": True,
        "fk_department_id": 1,
        "fk_role_id": 1,
        "fk_manager_id": 1,
        "password": "string",
    }
    response = client.put(
        "/admin/employees/email/admin@test.com",
        json=payload,
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_delete_employee_by_email_forbidden(client, manager_A):
    response = client.delete(
        "/admin/employees/email/admin@test.com",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
