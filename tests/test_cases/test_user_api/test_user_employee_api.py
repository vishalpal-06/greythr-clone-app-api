# -------------------------------------------------Test User API ---------------------------------------------------
def test_user_get_my_profile_success(client, user_A1, read_json):
    response = client.get(
        "/user/my/me/", headers={"Authorization": f"Bearer {user_A1}"}
    )
    expected = read_json("expected_responses/user/employee/get_my_profile_userA1.json")
    assert response.status_code == 200
    assert response.json() == expected


# -------------------------------------------------Test Manager API ---------------------------------------------------
def test_user_manager_access_get_subordinate_by_empid_nonsubordinate_forbidden(
    client, user_A1
):
    response = client.get(
        "/manager/subordinates/id/1", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_user_manager_access_get_subordinate_by_email_nonsubordinate_forbidden(
    client, user_A1
):
    response = client.get(
        "/manager/subordinates/email/userA2@test.com/",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_user_manager_access_get_subordinate_by_email_not_found(
    client, user_A1, read_json
):
    response = client.get(
        "/manager/subordinates/email/altufaltu@test.com/",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


def test_user_manager_access_get_subordinate_by_empid_not_found(
    client, user_A1, read_json
):
    response = client.get(
        "/manager/subordinates/id/10", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_user_admin_access_get_all_employees_forbidden(client, user_A1, read_json):
    response = client.get(
        "/admin/employees/", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_create_employee_forbidden(client, user_A1, read_json):
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
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_get_employee_by_empid_forbidden(client, user_A1, read_json):
    response = client.get(
        "/admin/employees/id/1", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_update_employee_by_empid_forbidden(
    client, user_A1, read_json
):
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
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_delete_employee_by_empid_forbidden(
    client, user_A1, read_json
):
    response = client.delete(
        "/admin/employees/id/1", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_get_employee_by_email_forbidden(client, user_A1, read_json):
    response = client.get(
        "/admin/employees/email/admin@test.com",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_update_employee_by_email_forbidden(
    client, user_A1, read_json
):
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
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_delete_employee_by_email_forbidden(
    client, user_A1, read_json
):
    response = client.delete(
        "/admin/employees/email/admin@test.com",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
