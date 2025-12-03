import json
from pathlib import Path

BASE_PATH = (
    Path(__file__).resolve().parent.parent.parent / "expected_responses/admin/leave/"
)


def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)


# -------------------------------------------------Test User API ---------------------------------------------------
def test_admin_get_my_all_leave_success(client, admin_user):
    response = client.get(
        "user/my/leave/", headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_all_my_leave_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_get_my_leave_by_year_success(client, admin_user):
    response = client.get(
        "user/my/leave/year/2025", headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_my_leave_by_year_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_get_my_leave_by_year_not_found(client, admin_user):
    response = client.get(
        "user/my/leave/year/2030", headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Leave record not found for employee 1 in year 2030"
    }


# ------------------------------------------------- Test Manager API ---------------------------------------------------


def test_admin_manager_access_get_subordinates_leave_by_empid_and_year_success(
    client, admin_user
):
    response = client.get(
        "manager/leaves/employee/2/year/2025",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_subordinates_leave_by_empid_and_year_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_manager_access_get_subordinates_leave_by_empid_and_year_nonsubordinate(
    client, admin_user
):
    response = client.get(
        "manager/leaves/employee/5/year/2025",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_admin_manager_access_get_subordinate_leave_by_empid_success(
    client, admin_user
):
    response = client.get(
        "manager/leaves/employee/2", headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_subordinate_leave_by_empid_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_manager_access_get_subordinate_leave_by_empid_not_found(
    client, admin_user
):
    response = client.get(
        "manager/leaves/employee/6", headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_admin_admin_access_get_employee_leave_by_empid_and_years_success(
    client, admin_user
):
    response = client.get(
        "admin/leaves/employee/1/year/2025",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_employee_leave_by_empid_and_years_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_get_employee_leave_by_empid_and_years_not_found(
    client, admin_user
):
    response = client.get(
        "admin/leaves/employee/1/year/2028",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Leave record not found for employee 1 in year 2028"
    }


def test_admin_admin_access_delete_employee_leave_by_empid_and_years_success(
    client, admin_user
):
    response = client.delete(
        "admin/leaves/employee/1/year/2025",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 204


def test_admin_admin_access_delete_employee_leave_by_empid_and_years_not_found(
    client, admin_user
):
    response = client.delete(
        "admin/leaves/employee/1/year/2028",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Leave record not found for employee 1 in year 2028"
    }


def test_admin_admin_access_get_employee_leaves_by_empid_success(client, admin_user):
    response = client.get(
        "admin/leaves/employee/1", headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_employee_leaves_by_empid_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_get_employee_leaves_by_empid_not_found(client, admin_user):
    response = client.get(
        "admin/leaves/employee/10", headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No leave records found for employee 10"}


def test_admin_admin_access_create_leave_success(client, admin_user):
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
        "admin/leaves/",
        json=payloads,
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("create_leave_admin.json")
    assert response.status_code == 201
    assert response.json() == expected


def test_admin_admin_access_create_duplicate_leave_conflict(client, admin_user):
    payloads = {
        "assign_year": 2023,
        "casual_leave": 5,
        "plan_leave": 15,
        "probation_leave": 6,
        "sick_leave": 5,
        "total_leave": 31,
        "balance_leave": 31,
        "fk_employee_id": 2,
    }
    response = client.post(
        "admin/leaves/",
        json=payloads,
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Leave record already exists for employee 2 in year 2023"
    }


def test_admin_admin_access_delete_leave_by_id_success(client, admin_user):
    response = client.delete(
        "admin/leaves/1", headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 204


def test_admin_admin_access_delete_leave_by_id_not_found(client, admin_user):
    response = client.delete(
        "admin/leaves/100", headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Leave record with ID 100 not found"}
