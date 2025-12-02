import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent / "expected_responses/admin/attendance"

def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)

# -------------------------------------------------test user api ---------------------------------------------------
def test_admin_create_attendance_success(client, admin_user):
    response = client.post(
        "user/my/attendance/",
        json={"punch_time": "2025-10-10T04:30:00.000Z"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 201
    assert response.json() == {'punch_time': '2025-10-10T04:30:00', 'attendance_id': 29, 'fk_employee_id': 1}


def test_admin_get_all_my_attendance_success(client, admin_user):
    response = client.get(
        "user/my/attendance/my",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_all_my_attendance_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_get_my_attendance_by_date_success(client, admin_user):
    response = client.get(
        "/user/my/attendance/my/date/2023-01-01",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_all_my_attendance_by_date_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_get_my_attendance_by_date_not_found(client, admin_user):
    response = client.get(
        "/user/my/attendance/my/date/2025-10-12",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 200
    assert response.json() == []


# -------------------------------------------------test manager api ---------------------------------------------------

def test_admin_access_manager_attendance_by_date_success(client, admin_user):
    response = client.get(
        "manager/attendance/date/2023-01-10",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_all_attendenace_by_date_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_manager_attendance_by_date_success_empty(client, admin_user):
    response = client.get(
        "manager/attendance/date/2023-04-22",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_admin_access_manager_attendance_by_employee_and_date_under_manager_success(client, admin_user):
    response = client.get(
        "manager/attendance/employee/3/date/2023-01-10",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_attendance_by_employee_and_date_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_manager_attendance_by_employee_and_date_not_under_manager_empty(client, admin_user):
    response = client.get(
        "manager/attendance/employee/2/date/2025-11-25",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_admin_access_manager_attendance_by_employee_date_not_under_manager(client, admin_user):
    response = client.get(
        "manager/attendance/employee/6/date/2025-11-25",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail":"Employee not found under your management"}

# -------------------------------------------------test admin api ---------------------------------------------------

def test_admin_access_admin_get_all_attendance_list_success(client, admin_user):
    response = client.get(
        "/admin/attendance/",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_all_attendance_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_admin_attendance_by_date_success(client, admin_user):
    response = client.get(
        "admin/attendance/date/2023-04-01",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_attendance_by_date_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_admin_attendance_by_date_not_found(client, admin_user):
    response = client.get(
        "admin/attendance/date/2023-04-04",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_admin_access_admin_attendance_by_empid_date_success(client, admin_user):
    response = client.get(
        "admin/attendance/employee/1/date/2023-01-01",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_attendance_by_empid_and_date_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_admin_attendance_by_empid_date_not_exist(client, admin_user):
    response = client.get(
        "admin/attendance/employee/10/date/2023-01-07",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


def test_admin_access_admin_attendance_by_empid_date_not_found(client, admin_user):
    response = client.get(
        "admin/attendance/employee/1/date/2023-01-07",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_admin_access_admin_attendance_by_empid_success(client, admin_user):
    response = client.get(
        "/admin/attendance/employee/3",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_attendance_by_empid_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_admin_attendance_by_empid_employee_not_exist(client, admin_user):
    response = client.get(
        "/admin/attendance/employee/13",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail":"Employee Not Founds"}