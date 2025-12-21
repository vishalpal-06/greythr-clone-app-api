# -------------------------------------------------Test User API ---------------------------------------------------
def test_user_get_all_my_salary_success(client, user_A1, read_json):
    response = client.get(
        "/user/my/salary/", headers={"Authorization": f"Bearer {user_A1}"}
    )
    expected = read_json("expected_responses/user/salary/get_all_my_salary_userA1.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_my_salary_by_year_success(client, user_A1, read_json):
    response = client.get(
        "/user/my/salary/year/2025", headers={"Authorization": f"Bearer {user_A1}"}
    )
    expected = read_json(
        "expected_responses/user/salary/get_my_salary_by_year_userA1.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_my_salary_by_year_not_found(client, user_A1, read_json):
    response = client.get(
        "/user/my/salary/year/2028", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Salary record not found for employee in year 2028"
    }


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_user_admin_access_get_employee_salary_by_years_forbidden(
    client, user_A1, read_json
):
    response = client.get(
        "admin/salaries/year/2025", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_get_all_employees_forbidden(client, user_A1, read_json):
    response = client.get(
        "admin/salaries/year/2025", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_delete_employee_salary_by_empid_and_year_forbidden(
    client, user_A1
):
    response = client.delete(
        "admin/salaries/employee/1/year/2026",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_get_salary_by_empid_forbidden(client, user_A1, read_json):
    response = client.get(
        "admin/salaries/employee/1/year/2026",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_post_salary_forbidden(client, user_A1, read_json):
    response = client.post(
        "admin/salaries/",
        json={"lpa": 1, "salary_year": 2000, "fk_employee_id": 1},
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_delete_salary_by_salaryid_forbidden(
    client, user_A1, read_json
):
    response = client.delete(
        "admin/salaries/1", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
