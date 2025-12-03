import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent / "expected_responses/admin/payslips/"

def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)

# -------------------------------------------------Test User API ---------------------------------------------------
def test_admin_get_all_my_payslips_success(client, admin_user):
    response = client.get(
        "/user/my/payslips/",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_all_my_payslips_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_get_my_payslips_by_year_and_month_success(client, admin_user):
    response = client.get(
        "/user/my/payslips/month/2025/1",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_my_payslips_by_year_and_month_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_get_my_payslips_by_year_and_month_not_found(client, admin_user):
    response = client.get(
        "/user/my/payslips/month/2025/11",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Payslip not found for this month"}


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_admin_admin_access_create_payslips_success(client, admin_user):
    payload = {
                "basic_amount": 1,
                "hra": 0,
                "special_allowance": 0,
                "internet_allowance": 0,
                "payslip_month": "2025-11-01T00:00:00.000Z",
                "fk_employee_id": 0
            }
    response = client.post(
        "/admin/payslips/",
        json=payload,
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("create_payslip_admin.json")
    assert response.status_code == 201
    assert response.json() == expected


def test_admin_admin_access_create_payslips_conflict(client, admin_user):
    payload = {
        "basic_amount": 80000,
        "hra": 40000,
        "special_allowance": 10000,
        "internet_allowance": 1500,
        "payslip_month": "2025-02-01T00:00:00Z",
        "fk_employee_id": 1
    }
    response = client.post(
        "/admin/payslips/",
        json=payload,
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 409
    assert response.json() == {"detail":"Payslip already exists for employee 1 in February 2025"}

def test_admin_admin_access_get_payslips_by_id_success(client, admin_user):
    response = client.get(
        "/admin/payslips/employee/1",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_payslip_by_id_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_get_payslips_by_id_not_found(client, admin_user):
    response = client.get(
        "/admin/payslips/employee/100",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No payslips found for this employee"}


def test_admin_admin_access_get_payslips_by_year_and_month_success(client, admin_user):
    response = client.get(
        "/admin/payslips/month/2025/2",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_payslips_by_year_and_month_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_get_payslips_by_year_and_month_not_found(client, admin_user):
    response = client.get(
        "/admin/payslips/month/2025/4",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No payslips found for 2025-04"}


def test_admin_admin_access_get_payslips_by_empid_year_and_month_success(client, admin_user):
    response = client.get(
        "/admin/payslips/employee/2/month/2025/3",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_payslips_by_empid_year_and_month_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_get_payslips_by_empid_year_and_month_not_found(client, admin_user):
    response = client.get(
        "/admin/payslips/employee/2/month/2025/4",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail" : "Payslip not found for this month"}


def test_admin_admin_access_delete_payslips_by_empid_year_and_month_success(client, admin_user):
    response = client.delete(
        "/admin/payslips/employee/1/month/2025/3",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 204

def test_admin_admin_access_delete_payslips_by_empid_year_and_month_emp_not_found(client, admin_user):
    response = client.delete(
        "/admin/payslips/employee/12/month/2025/4",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail" : "Payslip not found for this month"}


def test_admin_admin_access_delete_payslips_by_id_success(client, admin_user):
    response = client.delete(
        "/admin/payslips/1",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 204


def test_admin_admin_access_delete_payslips_by_id_not_found(client, admin_user):
    response = client.delete(
        "/admin/payslips/100",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Payslip not found"}

