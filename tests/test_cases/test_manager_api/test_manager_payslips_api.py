import pytest


# -----------------------------------Test User API -----------------------------------
def test_manager_get_all_my_payslips_success(client, manager_A, read_json):
    response = client.get("/user/my/payslips/", headers={"Authorization": f"Bearer {manager_A}"})
    expected = read_json("expected_responses/manager/payslips/get_all_my_payslips_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_my_payslips_by_year_and_month_success(client, manager_A, read_json):
    response = client.get(
        "/user/my/payslips/month/2025/1",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json(
        "expected_responses/manager/payslips/get_my_payslips_by_year_and_month_manager_A.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_my_payslips_by_year_and_month_fot_found(client, manager_A, read_json):
    response = client.get(
        "/user/my/payslips/month/2025/11",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Payslip not found for this month"}


# ------------------------------Test Admin API -------------------------------
PAYSLIP_PAYLOAD = {
    "basic_amount": 1,
    "hra": 0,
    "special_allowance": 0,
    "internet_allowance": 0,
    "payslip_month": "2025-11-01T00:00:00.000Z",
    "fk_employee_id": 0,
}


@pytest.mark.parametrize(
    ("method", "url", "kwargs"),
    [
        ("post", "/admin/payslips/", {"json": PAYSLIP_PAYLOAD}),
        ("get", "/admin/payslips/employee/1", {}),
        ("get", "/admin/payslips/month/2025/4", {}),
        ("get", "/admin/payslips/employee/1/month/2025/4", {}),
        ("delete", "/admin/payslips/employee/1/month/2025/4", {}),
        ("delete", "/admin/payslips/1", {}),
    ],
)
def test_manager_admin_access_payslips_forbidden(
    client,
    manager_A,
    method,
    url,
    kwargs,
):
    response = getattr(client, method)(
        url,
        headers={"Authorization": f"Bearer {manager_A}"},
        **kwargs,
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
