import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent / "expected_responses/manager/expense_claim"

def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)

# -------------------------------------------------test user api ---------------------------------------------------
def test_manager_create_expense_claim_success(client, manager_A):
    response = client.post(
        "user/my/expense-claims/",
        json={"claim_date": "2025-12-01T10:30:00.000Z", "amount": 10000, "description": "Mujhe to bas paisa chaiye"},
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("create_expense_manager_A.json")
    assert response.status_code == 201
    assert response.json() == expected


def test_manager_delete_own_expense_claim_success(client, manager_A):
    response = client.delete(
        "user/my/expense-claims/2",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 204


def test_manager_delete_own_expense_claim_rejected_or_approved_fails(client, manager_A):
    response = client.delete(
        "user/my/expense-claims/1",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Cannot delete approved/rejected claim'}


def test_manager_delete_other_user_expense_claim_forbidden(client, manager_A):
    response = client.delete(
        "user/my/expense-claims/6",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authorized'}


def test_manager_get_own_expense_claim_by_id_success(client, manager_A):
    response = client.get(
        "/user/my/expense-claims/1",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("get_my_expense_by_id_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected
    

def test_manager_get_other_user_expense_claim_by_id_forbidden(client, manager_A):
    response = client.get(
        "/user/my/expense-claims/6",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authorized'}


def test_manager_get_expense_claim_by_id_not_found(client, manager_A):
    response = client.get(
        "/user/my/expense-claims/16",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Expense claim not found'}


def test_manager_get_expense_claims_by_status_success(client, manager_A):
    response = client.get(
        "/user/my/expense-claims/status/Pending",
        headers={"Authorization": f"Bearer {manager_A}"},
    )

    expected = read_json("get_expense_by_status_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_expense_claims_by_year_month_success(client, manager_A):
    response = client.get(
        "user/my/expense-claims/month/2025/2",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("get_expense_using_year_month_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_expense_claims_by_year_month_not_found(client, manager_A):
    response = client.get(
        "user/my/expense-claims/month/2025/06",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 200
    assert response.json() == []


# -------------------------------------------------test manager api ---------------------------------------------------
def test_manager_access_manager_expense_claim_by_id_success(client, manager_A):
    response = client.get(
        "/manager/expense-claims/5",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("get_expense_by_id_for_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_access_manager_expense_claim_by_id_forbidden(client, manager_A):
    response = client.get(
        "/manager/expense-claims/1",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Expense Application not found under your management"}


def test_manager_access_manager_expense_claims_by_year_month_empty(client, manager_A):
    response = client.get(
        "manager/expense-claims/month/2025/11",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_manager_access_manager_expense_claims_by_status_empty(client, manager_A):
    response = client.get(
        "manager/expense-claims/status/Pending",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("get_employee_expense_by_status_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_access_manager_expense_claims_by_empid_year_month_employee_under_manager(client, manager_A):
    response = client.get(
        "manager/expense-claims/employee/4/month/2025/4",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("get_expense_by_empid_year_and_month_for_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_access_manager_expense_claims_by_empid_year_month_employee_not_under_manager(client, manager_A):
    response = client.get(
        "manager/expense-claims/employee/1/month/2025/12",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_manager_update_expense_claim_status_manager_scope_success(client, manager_A):
    response = client.put(
        "/manager/expense-claims/6/status",
        json={"claim_status": "Approved"},
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("update_expense_by_id_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_update_expense_claim_status_manager_scope_forbidden(client, manager_A):
    response = client.put(
        "/manager/expense-claims/2/status",
        json={"claim_status": "Approved"},
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Expense Application not found under your management"}


def test_manager_update_expense_claim_status_manager_not_found(client, manager_A):
    response = client.put(
        "/manager/expense-claims/20/status",
        json={"claim_status": "Approved"},
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Expense claim not found"}


# -------------------------------------------------test admin api ---------------------------------------------------
def test_manager_access_admin_expense_claim_by_id_forbidden(client, manager_A):
    response = client.get(
        "admin/expense-claims/1",
        headers={"Authorization": f"Bearer {manager_A}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_access_admin_expense_claims_by_empid_forbidden(client, manager_A):
    response = client.get(
        "admin/expense-claims/employee/100",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_access_admin_expense_claims_by_status_forbidden(client, manager_A):
    response = client.get(
        "/admin/expense-claims/status/Pending",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_access_admin_expense_claims_by_year_month_forbidden(client, manager_A):
    response = client.get(
        "admin/expense-claims/month/2025/11",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_access_admin_expense_claims_by_empid_year_month_forbidden(client, manager_A):
    response = client.get(
        "admin/expense-claims/employee/1/month/2025/11",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_update_expense_claim_status_admin_forbidden(client, manager_A):
    response = client.put(
        "admin/expense-claims/1/status",
        json={"claim_status": "Approved"},
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}









