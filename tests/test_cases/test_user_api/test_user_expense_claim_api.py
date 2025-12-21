# -------------------------------------------------Test User API ---------------------------------------------------
def test_user_create_my_expense_claim_success(client, user_A1, read_json):
    response = client.post(
        "user/my/expense-claims/",
        json={
            "claim_date": "2025-12-01T10:30:00.000Z",
            "amount": 10000,
            "description": "Mujhe to bas paisa chaiye",
        },
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    expected = read_json(
        "expected_responses/user/expense_claim/create_expense_userA1.json"
    )
    assert response.status_code == 201
    assert response.json() == expected


def test_user_delete_my_expense_claim_success(client, user_A1, read_json):
    response = client.delete(
        "user/my/expense-claims/6",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 204


def test_user_delete_my_expense_claim_rejected_or_approved_fails(
    client, user_A1, read_json
):
    response = client.delete(
        "user/my/expense-claims/5",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot delete approved/rejected claim"}


def test_user_delete_other_user_expense_claim_forbidden(client, user_A1, read_json):
    response = client.delete(
        "user/my/expense-claims/1",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized"}


def test_user_get_my_expense_claim_by_id_success(client, user_A1, read_json):
    response = client.get(
        "/user/my/expense-claims/5",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    expected = read_json(
        "expected_responses/user/expense_claim/get_my_expense_by_id_userA1.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_other_user_expense_claim_by_id_forbidden(client, user_A1, read_json):
    response = client.get(
        "/user/my/expense-claims/1",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized"}


def test_user_get_expense_claim_by_id_not_found(client, user_A1, read_json):
    response = client.get(
        "/user/my/expense-claims/16",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Expense claim not found"}


def test_user_get_expense_claims_by_status_success(client, user_A1, read_json):
    response = client.get(
        "/user/my/expense-claims/status/Pending",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    expected = read_json(
        "expected_responses/user/expense_claim/get_expense_by_status_userA1.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_my_expense_claims_by_year_month_success(client, user_A1, read_json):
    response = client.get(
        "user/my/expense-claims/month/2025/04",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    expected = read_json(
        "expected_responses/user/expense_claim/get_my_expense_using_year_month_userA1.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_expense_claims_by_year_month_not_found(client, user_A1, read_json):
    response = client.get(
        "user/my/expense-claims/month/2025/06",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 200
    assert response.json() == []


# -------------------------------------------------Test Manager API ---------------------------------------------------
def test_user_manager_access_get_subordinate_expense_claim_by_id_forbidden(
    client, user_A1
):
    response = client.get(
        "/manager/expense-claims/1",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Expense Application not found under your management"
    }


def test_user_manager_access_get_subordinate_expense_claims_by_year_and_month_empty(
    client, user_A1
):
    response = client.get(
        "manager/expense-claims/month/2025/11",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_user_manager_access_get_subordinate_expense_claims_by_status_empty(
    client, user_A1
):
    response = client.get(
        "manager/expense-claims/status/Pending",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_user_manager_access_get_subordinate_expense_claims_by_empid_year_month_nonsubordinate(
    client, user_A1
):
    response = client.get(
        "manager/expense-claims/employee/1/month/2025/12",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_user_update_subordinate_expense_claim_status_nonsubordinate_forbidden(
    client, user_A1
):
    response = client.put(
        "/manager/expense-claims/2/status",
        json={"claim_status": "Approved"},
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Expense Application not found under your management"
    }


def test_user_update_subordinate_expense_claim_status_by_id_not_found(
    client, user_A1, read_json
):
    response = client.put(
        "/manager/expense-claims/20/status",
        json={"claim_status": "Approved"},
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Expense claim not found"}


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_user_admin_access_get_employee_expense_claim_by_id_forbidden(
    client, user_A1, read_json
):
    response = client.get(
        "admin/expense-claims/1", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_get_employee_expense_claims_by_empid_forbidden(
    client, user_A1
):
    response = client.get(
        "admin/expense-claims/employee/100",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_get_employee_expense_claims_by_status_forbidden(
    client, user_A1
):
    response = client.get(
        "/admin/expense-claims/status/Pending",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_get_employee_expense_claims_by_year_month_forbidden(
    client, user_A1
):
    response = client.get(
        "admin/expense-claims/month/2025/11",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_get_employee_expense_claims_by_empid_year_month_forbidden(
    client, user_A1
):
    response = client.get(
        "admin/expense-claims/employee/1/month/2025/11",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_update_employee_expense_claim_status_by_id_forbidden(
    client, user_A1, read_json
):
    response = client.put(
        "admin/expense-claims/1/status",
        json={"claim_status": "Approved"},
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
