import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent / "expected_responses/manager/salary/"

def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)

# -------------------------------------------------test user api ---------------------------------------------------
def test_manager_get_salary_by_year_success(client, manager_A):
    response = client.get(
        "/user/my/leave/year/2025",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    expected = read_json("get_2025_salary_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_salary_by_year_not_found(client, manager_A):
    response = client.get(
        "/user/my/leave/year/2028",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Leave record not found for employee 2 in year 2028"}


def test_manager_get_all_salary_success(client, manager_A):
    response = client.get(
        "user/my/leave/",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    expected = read_json("get_all_salary_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected
    

# -------------------------------------------------test manager api ---------------------------------------------------
def test_manager_access_manager_get_employee_salary_by_year_not_found(client, manager_A):
    response = client.get(
        "manager/leaves/employee/1/year/2025",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_manager_access_manager_get_employee_salary_by_empid_not_found(client, manager_A):
    response = client.get(
        "manager/leaves/employee/1",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


# -------------------------------------------------test admin api ---------------------------------------------------
def test_manager_access_admin_get_employee_salary_by_years_forbidden(client, manager_A):
    response = client.get(
        "admin/salaries/year/2025",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_access_admin_get_all_employees_forbidden(client, manager_A):
    response = client.get(
        "admin/salaries/year/2025",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_access_admin_delete_employee_salary_by_empid_and_year_forbidden(client, manager_A):
    response = client.delete(
        "admin/salaries/employee/1/year/2026",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_access_admin_get_salary_by_empid_forbidden(client, manager_A):
    response = client.get(
        "admin/salaries/employee/1/year/2026",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_access_admin_post_salary_forbidden(client, manager_A):
    response = client.post(
        "admin/salaries/",
        json={"lpa": 1, "salary_year": 2000, "fk_employee_id": 1},
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_access_admin_delete_salary_by_salaryid_forbidden(client, manager_A):
    response = client.delete(
        "admin/salaries/1",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}






