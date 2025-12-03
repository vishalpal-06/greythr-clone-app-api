import json
from pathlib import Path

BASE_PATH = (
    Path(__file__).resolve().parent.parent.parent / "expected_responses/user/leave/"
)


def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)


# -------------------------------------------------Test User API ---------------------------------------------------
def test_user_get_my_all_leave_success(client, user_A1):
    response = client.get(
        "user/my/leave/", headers={"Authorization": f"Bearer {user_A1}"}
    )
    expected = read_json("get_all_my_leave_userA1.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_my_leave_by_year_success(client, user_A1):
    response = client.get(
        "user/my/leave/year/2025", headers={"Authorization": f"Bearer {user_A1}"}
    )
    expected = read_json("get_my_leave_by_year_userA1.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_my_leave_by_year_not_found(client, user_A1):
    response = client.get(
        "user/my/leave/year/2030", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Leave record not found for employee 4 in year 2030"
    }


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_user_admin_access_get_employee_leave_by_empid_and_years_forbidden(
    client, user_A1
):
    response = client.get(
        "admin/leaves/employee/1/year/2025",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_delete_employee_leave_by_empid_and_years_forbidden(
    client, user_A1
):
    response = client.delete(
        "admin/leaves/employee/1/year/2025",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_get_employee_leaves_by_empid_forbidden(client, user_A1):
    response = client.get(
        "admin/leaves/employee/1", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_create_leave_forbidden(client, user_A1):
    payloads = {
        "assign_year": 2000,
        "casual_leave": 0,
        "plan_leave": 0,
        "probation_leave": 0,
        "sick_leave": 0,
        "total_leave": 0,
        "balance_leave": 0,
        "fk_employee_id": 1,
    }
    response = client.post(
        "admin/leaves/", json=payloads, headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_delete_leave_by_id_forbidden(client, user_A1):
    response = client.delete(
        "admin/leaves/1", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
