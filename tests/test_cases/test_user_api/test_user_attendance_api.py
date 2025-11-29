import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent / "expected_responses/user/attendance"

def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)

# -------------------------------------------------test user api ---------------------------------------------------
def test_user_create_attendance(client, user_A1):
    response = client.post(
        "user/my/attendance/",
        json={"punch_time": "2025-10-10T04:30:00.000Z"},
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 201
    assert response.json() == {'punch_time': '2025-10-10T04:30:00', 'attendance_id': 29, 'fk_employee_id': 4}


def test_user_get_all_my_attendance(client, user_A1):
    response = client.get(
        "user/my/attendance/my",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    expected = read_json("get_all_my_attendance_userA1.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_my_attendance_using_date(client, user_A1):
    response = client.get(
        "/user/my/attendance/my/date/2025-10-10",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_user_get_my_attendance_using_date_not_exist(client, user_A1):
    response = client.get(
        "/user/my/attendance/my/date/2025-10-12",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 200
    assert response.json() == []


# -------------------------------------------------test manager api ---------------------------------------------------

def test_user_get_manager_attendence(client, user_A1):
    response = client.get(
        "manager/attendance/date/2025-11-25",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_user_get_manager_attendence_using_id(client, user_A1):
    response = client.get(
        "manager/attendance/employee/3/date/2025-11-25",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail":"Employee not found under your management"}


# -------------------------------------------------test admin api ---------------------------------------------------

def test_user_get_all_attendence_for_Admin(client, user_A1):
    response = client.get(
        "/admin/attendance/",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_get_all_attendence_using_date_for_Admin(client, user_A1):
    response = client.get(
        "admin/attendance/date/2025-11-27",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_get_all_attendence_using_empid_and_date_for_Admin(client, user_A1):
    response = client.get(
        "admin/attendance/employee/120/date/2025-11-27",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_get_all_attendence_using_empid_for_Admin(client, user_A1):
    response = client.get(
        "/admin/attendance/employee/3",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}

