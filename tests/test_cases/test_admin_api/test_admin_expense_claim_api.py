import json
from pathlib import Path

BASE_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "expected_responses/admin/expense_claim"
)


def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)


# -------------------------------------------------Test User API ---------------------------------------------------
def test_admin_create_expense_claim_fail(client, admin_user):
    response = client.post(
        "user/my/expense-claims/",
        json={
            "claim_date": "2025-12-01T10:30:00.000Z",
            "amount": 10000,
            "description": "Mujhe to bas paisa chaiye",
        },
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "No manager assigned"}


def test_admin_delete_my_expense_claim_fail(client, admin_user):
    response = client.delete(
        "user/my/expense-claims/2",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized"}


# -------------------------------------------------Test Manager API ---------------------------------------------------
def test_admin_manager_access_get_subordinate_expense_claim_by_id_success(
    client, admin_user
):
    response = client.get(
        "/manager/expense-claims/1",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_subordinate_expense_by_id_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_manager_access_get_subordinate_expense_claim_by_id_forbidden(
    client, manager_A
):
    response = client.get(
        "/manager/expense-claims/8",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Expense Application not found under your management"
    }


def test_admin_manager_access_get_subordinate_expense_claims_by_year_month_success(
    client, admin_user
):
    response = client.get(
        "manager/expense-claims/month/2025/3",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_subordinate_expense_by_year_and_month_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_manager_access_get_subordinate_expense_claims_by_year_month_empty(
    client, admin_user
):
    response = client.get(
        "manager/expense-claims/month/2025/11",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_admin_manager_access_get_subordinate_expense_claims_by_status_success(
    client, admin_user
):
    response = client.get(
        "manager/expense-claims/status/Pending",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_subordinate_expense_by_status_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_manager_access_get_subordinate_expense_claims_by_empid_year_and_month_success(
    client, manager_A
):
    response = client.get(
        "manager/expense-claims/employee/4/month/2025/4",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("get_subordinate_expense_by_empid_year_and_month_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_manager_access_get_subordinate_expense_claims_by_empid_year_and_month_nonsubordinate(
    client, manager_A
):
    response = client.get(
        "manager/expense-claims/employee/5/month/2025/12",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_admin_manager_access_update_subordinate_expense_claim_status_success(
    client, admin_user
):
    response = client.put(
        "/manager/expense-claims/1/status",
        json={"claim_status": "Approved"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("update_subordinate_expense_by_id_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_manager_access_update_subordinate_expense_claim_status_forbidden(
    client, admin_user
):
    response = client.put(
        "/manager/expense-claims/7/status",
        json={"claim_status": "Approved"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Expense Application not found under your management"
    }


def test_admin_manager_access_update_expense_claim_status_not_found(client, admin_user):
    response = client.put(
        "/manager/expense-claims/20/status",
        json={"claim_status": "Approved"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Expense claim not found"}


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_admin_admin_access_get_expense_claim_by_id_success(client, admin_user):
    response = client.get(
        "admin/expense-claims/5", headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_employee_expense_by_id_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_get_expense_claim_by_id_not_found(client, admin_user):
    response = client.get(
        "admin/expense-claims/30", headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Expense claim not found"}


def test_admin_admin_access_get_expense_claims_by_empid_success(client, admin_user):
    response = client.get(
        "admin/expense-claims/employee/3",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_employee_expense_empid_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_get_expense_claims_by_empid_not_found(client, admin_user):
    response = client.get(
        "admin/expense-claims/employee/100",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No claims found"}


def test_admin_admin_access_get_expense_claims_by_status_success(client, admin_user):
    response = client.get(
        "/admin/expense-claims/status/Pending",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_employee_expense_by_status_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_get_expense_claims_by_status_not_found(client, admin_user):
    response = client.get(
        "/admin/expense-claims/status/Rejected",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No Rejected claims"}


def test_admin_admin_access_get_expense_claims_by_year_month_success(
    client, admin_user
):
    response = client.get(
        "admin/expense-claims/month/2025/2",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_employee_expense_by_year_month_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_get_expense_claims_by_year_month_not_found(
    client, admin_user
):
    response = client.get(
        "admin/expense-claims/month/2025/11",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No claims in this month"}


def test_admin_admin_access_get_expense_claims_by_empid_year_and_month_success(
    client, admin_user
):
    response = client.get(
        "admin/expense-claims/employee/2/month/2025/2",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json(
        "get_employee_expense_claims_by_empid_year_and_month_admin.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_get_expense_claims_by_empid_year_and_month_not_found(
    client, admin_user
):
    response = client.get(
        "admin/expense-claims/employee/1/month/2025/11",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "No expense claims found for this employee and month"
    }


def test_admin_admin_access_update_expense_claim_status_success(client, admin_user):
    response = client.put(
        "admin/expense-claims/1/status",
        json={"claim_status": "Pending"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("update_employee_expense_status_by_id_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_update_expense_claim_status_not_found(client, admin_user):
    response = client.put(
        "admin/expense-claims/30/status",
        json={"claim_status": "Pending"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Expense claim not found"}
