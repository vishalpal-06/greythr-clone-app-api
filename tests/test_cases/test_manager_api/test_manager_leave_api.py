import pytest


# -----------------------------------Test User API -----------------------------------
def test_manager_get_my_all_leave_success(client, manager_A, read_json):
    response = client.get("user/my/leave/", headers={"Authorization": f"Bearer {manager_A}"})
    expected = read_json("expected_responses/manager/leave/get_all_my_leave_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_my_leave_by_year_success(client, manager_A, read_json):
    response = client.get(
        "user/my/leave/year/2025", headers={"Authorization": f"Bearer {manager_A}"}
    )
    expected = read_json("expected_responses/manager/leave/get_my_leave_by_year_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_my_leave_by_year_not_found(client, manager_A, read_json):
    response = client.get(
        "user/my/leave/year/2030", headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Leave record not found for employee 2 in year 2030"}


# ------------------------------Test Admin API -------------------------------
LEAVE_PAYLOAD = {
    "assign_year": 2000,
    "casual_leave": 0,
    "plan_leave": 0,
    "probation_leave": 0,
    "sick_leave": 0,
    "total_leave": 0,
    "balance_leave": 0,
    "fk_employee_id": 1,
}


@pytest.mark.parametrize(
    ("method", "url", "kwargs"),
    [
        ("get", "admin/leaves/employee/1/year/2025", {}),
        ("delete", "admin/leaves/employee/1/year/2025", {}),
        ("get", "admin/leaves/employee/1", {}),
        ("post", "admin/leaves/", {"json": LEAVE_PAYLOAD}),
        ("delete", "admin/leaves/1", {}),
    ],
)
def test_manager_admin_access_leave_forbidden(
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
