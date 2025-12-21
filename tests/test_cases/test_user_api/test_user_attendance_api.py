# -------------------------------------------------Test User API ---------------------------------------------------
def test_user_create_my_attendance_success(client, user_A1, read_json):
    response = client.post(
        "user/my/attendance/",
        json={"punch_time": "2025-10-10T04:30:00.000Z"},
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 201
    assert response.json() == {
        "punch_time": "2025-10-10T04:30:00",
        "attendance_id": 29,
        "fk_employee_id": 4,
    }


def test_user_get_all_my_attendance_success(client, user_A1, read_json):
    response = client.get(
        "user/my/attendance/my",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    expected = read_json(
        "expected_responses/user/attendance/get_all_my_attendance_userA1.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_my_attendance_by_date_success(client, user_A1, read_json):
    response = client.get(
        "/user/my/attendance/my/date/2025-10-10",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_user_get_my_attendance_by_date_not_found(client, user_A1, read_json):
    response = client.get(
        "/user/my/attendance/my/date/2025-10-12",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 200
    assert response.json() == []


# -------------------------------------------------Test Manager API ---------------------------------------------------


def test_user_manager_access_get_subordinate_attendance_by_date_success_empty(
    client, user_A1
):
    response = client.get(
        "manager/attendance/date/2025-11-25",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_user_manager_access_get_subordinate_attendance_by_empid_and_date_nonsubordinate_forbidden(
    client, user_A1
):
    response = client.get(
        "manager/attendance/employee/3/date/2025-11-25",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


# -------------------------------------------------Test Admin API ---------------------------------------------------


def test_user_admin_access_get_all_attendance_list_forbidden(
    client, user_A1, read_json
):
    response = client.get(
        "/admin/attendance/",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_get_attendance_by_date_forbidden(client, user_A1, read_json):
    response = client.get(
        "admin/attendance/date/2025-11-27",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_get_attendance_by_empid_and_date_forbidden(
    client, user_A1, read_json
):
    response = client.get(
        "admin/attendance/employee/120/date/2025-11-27",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_get_attendance_by_empid_forbidden(
    client, user_A1, read_json
):
    response = client.get(
        "/admin/attendance/employee/3",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
