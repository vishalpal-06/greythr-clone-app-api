import json
from pathlib import Path

BASE_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "expected_responses/manager/attendance"
)


def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)


# -------------------------------------------------Test User API ---------------------------------------------------
def test_manager_create_my_attendance_success(client, manager_A):
    response = client.post(
        "user/my/attendance/",
        json={"punch_time": "2025-10-10T04:30:00.000Z"},
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("create_attendance_manager_A.json")
    assert response.status_code == 201
    assert response.json() == expected


def test_manager_get_all_my_attendance_success(client, manager_A):
    response = client.get(
        "user/my/attendance/my",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("get_all_my_attendance_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_my_attendance_by_date_success(client, manager_A):
    response = client.get(
        "/user/my/attendance/my/date/2023-01-10",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("get_all_my_attendance_by_date_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_my_attendance_by_date_not_found(client, manager_A):
    response = client.get(
        "/user/my/attendance/my/date/2025-10-12",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 200
    assert response.json() == []


# -------------------------------------------------Test Manager API ---------------------------------------------------


def test_manager_manager_access_get_subordinate_attendance_by_date_success(
    client, manager_A
):
    response = client.get(
        "manager/attendance/date/2023-04-02",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("get_subordinate_attendenace_by_date_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_manager_access_get_subordinate_attendance_by_date_success_empty(
    client, manager_A
):
    response = client.get(
        "manager/attendance/date/2023-04-22",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_manager_manager_access_get_subordinate_attendance_by_empid_and_date_success(
    client, manager_A
):
    response = client.get(
        "manager/attendance/employee/5/date/2023-04-02",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json(
        "get_subordinate_attendance_by_employee_and_date_managerA.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_manager_access_get_subordinate_attendance_by_empid_and_date_nonsubordinate_empty(
    client, manager_A
):
    response = client.get(
        "manager/attendance/employee/4/date/2025-11-25",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_manager_manager_access_get_attendance_by_empid_and_date_nonsubordinate(
    client, manager_A
):
    response = client.get(
        "manager/attendance/employee/6/date/2025-11-25",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


# -------------------------------------------------Test Admin API ---------------------------------------------------


def test_manager_admin_access_get_all_attendance_list_forbidden(client, manager_A):
    response = client.get(
        "/admin/attendance/",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_get_attendance_by_date_forbidden(client, manager_A):
    response = client.get(
        "admin/attendance/date/2025-11-27",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_get_attendance_by_empid_and_date_forbidden(
    client, manager_A
):
    response = client.get(
        "admin/attendance/employee/120/date/2025-11-27",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_get_attendance_by_empid_forbidden(client, manager_A):
    response = client.get(
        "/admin/attendance/employee/3",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
