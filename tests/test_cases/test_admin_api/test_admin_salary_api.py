import json
from pathlib import Path

BASE_PATH = (
    Path(__file__).resolve().parent.parent.parent / "expected_responses/admin/salary/"
)


def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)


# -------------------------------------------------Test User API ---------------------------------------------------
def test_user_get_all_my_salary_success(client, admin_user):
    response = client.get(
        "/user/my/salary/", headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_all_my_salary_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_my_salary_by_year_success(client, admin_user):
    response = client.get(
        "/user/my/salary/year/2025", headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_my_salary_by_year_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_my_salary_by_year_not_found(client, admin_user):
    response = client.get(
        "/user/my/salary/year/2028", headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Salary record not found for employee in year 2028"
    }


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_admin_admin_access_get_employee_salary_by_years_success(client, admin_user):
    response = client.get(
        "admin/salaries/year/2025", headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_employees_salary_by_year_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_get_employee_salary_by_years_not_found(client, admin_user):
    response = client.get(
        "admin/salaries/year/2028", headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No salary records found for year 2028"}


def test_admin_admin_access_get_all_employees_salary_success(client, admin_user):
    response = client.get(
        "admin/salaries/year/2025", headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_all_employees_salary_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_delete_employee_salary_by_empid_and_year_success(
    client, admin_user
):
    response = client.delete(
        "admin/salaries/employee/1/year/2025",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 204


def test_admin_admin_access_delete_employee_salary_by_empid_and_year_not_found(
    client, admin_user
):
    response = client.delete(
        "admin/salaries/employee/1/year/2028",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Salary record not found for employee in year 2028"
    }


def test_admin_admin_access_get_salary_by_empid_and_year_success(client, admin_user):
    response = client.get(
        "admin/salaries/employee/5/year/2025",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_emoloyee_salary_by_empid_and_year_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_get_salary_by_empid_and_year_not_exist(client, admin_user):
    response = client.get(
        "admin/salaries/employee/100/year/2026",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Salary record not found for employee in year 2026"
    }


def test_admin_admin_access_get_salary_by_empid_success(client, admin_user):
    response = client.get(
        "admin/salaries/employee/5/salaries",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_emoloyee_salary_by_empid_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_get_salary_by_empid_not_exist(client, admin_user):
    response = client.get(
        "admin/salaries/employee/100/salaries",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No salary records found for employee 100"}


def test_admin_admin_access_create_salary_success(client, admin_user):
    response = client.post(
        "admin/salaries/",
        json={"lpa": 1, "salary_year": 2000, "fk_employee_id": 1},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("create_salary_admin.json")
    assert response.status_code == 201
    assert response.json() == expected


def test_admin_admin_access_create_salary_conflict(client, admin_user):
    response = client.post(
        "admin/salaries/",
        json={"lpa": 1, "salary_year": 2025, "fk_employee_id": 1},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Salary record already exists for employee 1 in year 2025"
    }


def test_admin_admin_access_delete_salary_by_salaryid_success(client, admin_user):
    response = client.delete(
        "admin/salaries/1", headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 204


def test_admin_admin_access_delete_salary_by_salaryid_not_found(client, admin_user):
    response = client.delete(
        "admin/salaries/100", headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Salary record with ID 100 not found"}
