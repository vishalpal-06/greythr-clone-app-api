import pytest


# -----------------------------------Test User API -----------------------------------
def test_user_get_all_my_payslips_success(client, user_A1, read_json):
    response = client.get("/user/my/payslips/", headers={"Authorization": f"Bearer {user_A1}"})
    expected = read_json("expected_responses/user/payslips/get_all_my_payslips_userA1.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_my_payslips_by_year_and_month_success(client, user_A1, read_json):
    response = client.get(
        "/user/my/payslips/month/2025/1", headers={"Authorization": f"Bearer {user_A1}"}
    )
    expected = read_json(
        "expected_responses/user/payslips/get_my_payslips_by_year_and_month_userA1.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_my_payslips_by_year_and_month_fot_found(client, user_A1, read_json):
    response = client.get(
        "/user/my/payslips/month/2025/11",
        headers={"Authorization": f"Bearer {user_A1}"},
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
def test_user_admin_access_payslips_forbidden(
    client,
    user_A1,
    method,
    url,
    kwargs,
):
    response = getattr(client, method)(
        url,
        headers={"Authorization": f"Bearer {user_A1}"},
        **kwargs,
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
