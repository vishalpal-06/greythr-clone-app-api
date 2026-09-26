import pytest


# -----------------------------------Test User API -----------------------------------
def test_user_get_all_my_salary_success(client, manager_A, read_json):
    response = client.get("/user/my/salary/", headers={"Authorization": f"Bearer {manager_A}"})
    expected = read_json("expected_responses/manager/salary/get_all_my_salary_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_my_salary_by_year_success(client, manager_A, read_json):
    response = client.get(
        "/user/my/salary/year/2025", headers={"Authorization": f"Bearer {manager_A}"}
    )
    expected = read_json("expected_responses/manager/salary/get_my_salary_by_year_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_my_salary_by_year_not_found(client, manager_A, read_json):
    response = client.get(
        "/user/my/salary/year/2028", headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Salary record not found for employee in year 2028"}


# -----------------------------------Test Manager API -----------------------------------
def test_manager_manager_access_get_employee_salary_by_year_not_found(client, manager_A):
    response = client.get(
        "manager/leaves/employee/1/year/2025",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_manager_manager_access_get_employee_salary_by_empid_not_found(client, manager_A):
    response = client.get(
        "manager/leaves/employee/1", headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


# ------------------------------Test Admin API -------------------------------
@pytest.mark.parametrize(
    ("method", "url", "kwargs"),
    [
        ("get", "admin/salaries/year/2025", {}),
        ("delete", "admin/salaries/employee/1/year/2026", {}),
        ("get", "admin/salaries/employee/1/year/2026", {}),
        (
            "post",
            "admin/salaries/",
            {"json": {"lpa": 1, "salary_year": 2000, "fk_employee_id": 1}},
        ),
        ("delete", "admin/salaries/1", {}),
    ],
)
def test_manager_admin_access_salary_forbidden(
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
