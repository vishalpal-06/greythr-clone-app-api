import pytest


# -----------------------------------Test User API -----------------------------------
def test_user_get_my_profile_success(client, user_A1, read_json):
    response = client.get("/user/my/me/", headers={"Authorization": f"Bearer {user_A1}"})
    expected = read_json("expected_responses/user/employee/get_my_profile_userA1.json")
    assert response.status_code == 200
    assert response.json() == expected


# -----------------------------------Test Manager API -----------------------------------
def test_user_manager_access_get_subordinate_by_empid_nonsubordinate_forbidden(client, user_A1):
    response = client.get(
        "/manager/subordinates/id/1", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_user_manager_access_get_subordinate_by_email_nonsubordinate_forbidden(client, user_A1):
    response = client.get(
        "/manager/subordinates/email/userA2@test.com/",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_user_manager_access_get_subordinate_by_email_not_found(client, user_A1, read_json):
    response = client.get(
        "/manager/subordinates/email/altufaltu@test.com/",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


def test_user_manager_access_get_subordinate_by_empid_not_found(client, user_A1, read_json):
    response = client.get(
        "/manager/subordinates/id/10", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


# ------------------------------Test Admin API -------------------------------
EMPLOYEE_PAYLOAD = {
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


@pytest.mark.parametrize(
    ("method", "url", "kwargs"),
    [
        ("get", "/admin/employees/", {}),
        ("post", "/admin/employees/", {"json": EMPLOYEE_PAYLOAD}),
        ("get", "/admin/employees/id/1", {}),
        ("put", "/admin/employees/id/1", {"json": EMPLOYEE_PAYLOAD}),
        ("delete", "/admin/employees/id/1", {}),
        ("get", "/admin/employees/email/admin@test.com", {}),
        ("put", "/admin/employees/email/admin@test.com", {"json": EMPLOYEE_PAYLOAD}),
        ("delete", "/admin/employees/email/admin@test.com", {}),
    ],
)
def test_user_admin_access_employee_forbidden(client, user_A1, method, url, kwargs):
    response = getattr(client, method)(
        url,
        headers={"Authorization": f"Bearer {user_A1}"},
        **kwargs,
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
