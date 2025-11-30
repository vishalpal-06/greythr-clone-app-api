import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent / "expected_responses/manager/payslips/"

def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)

# -------------------------------------------------test user api ---------------------------------------------------
def test_manager_get_all_my_payslips_success(client, manager_A):
    response = client.get(
        "/user/my/payslips/",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    expected = read_json("get_all_my_payslips_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_my_payslips_by_year_and_month_success(client, manager_A):
    response = client.get(
        "/user/my/payslips/month/2025/1",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    expected = read_json("get_payslips_by_year_and_month_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_my_payslips_by_year_and_month_fot_found(client, manager_A):
    response = client.get(
        "/user/my/payslips/month/2025/11",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Payslip not found for this month"}


# -------------------------------------------------test admin api ---------------------------------------------------
def test_manager_access_admin_create_payslips_forbidden(client, manager_A):
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
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_access_admin_get_payslips_by_id_forbidden(client, manager_A):
    response = client.get(
        "/admin/payslips/employee/1",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_access_admin_get_payslips_by_year_and_month_forbidden(client, manager_A):
    response = client.get(
        "/admin/payslips/month/2025/4",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_access_admin_get_payslips_by_empid_year_and_month_forbidden(client, manager_A):
    response = client.get(
        "/admin/payslips/employee/1/month/2025/4",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_access_admin_delete_payslips_by_empid_year_and_month_forbidden(client, manager_A):
    response = client.delete(
        "/admin/payslips/employee/1/month/2025/4",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_access_admin_delete_payslips_by_id_forbidden(client, manager_A):
    response = client.delete(
        "/admin/payslips/1",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}













