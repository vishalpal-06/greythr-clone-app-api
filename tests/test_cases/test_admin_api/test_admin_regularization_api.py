import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent / "expected_responses/admin/regularization/"

def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)


# -------------------------------------------------Test Manager API ---------------------------------------------------
def test_admin_access_manager_get_subordinate_regularization_by_status_success(client, admin_user):
    response = client.get(
        "/manager/regularizations/pending",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_subordinate_regularization_by_status_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_manager_get_subordinate_regularization_by_id_success(client, admin_user):
    response = client.get(
        "manager/regularizations/1",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_subordinate_regularization_by_id_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_manager_get_subordinate_regularization_by_id_forbidden(client, admin_user):
    response = client.get(
        "manager/regularizations/4",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Regularization not found under your management"}


def test_admin_access_manager_get_subordinate_regularization_by_id_not_found(client, admin_user):
    response = client.get(
        "manager/regularizations/15",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Regularization request not found"}


def test_admin_access_manager_get_subordinate_regularization_by_empid_success(client, admin_user):
    response = client.get(
        "manager/regularizations/employee/2",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_subordinate_regularization_by_empid_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_manager_get_subordinate_regularization_by_empid_forbidden(client, admin_user):
    response = client.get(
        "manager/regularizations/employee/1",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_admin_access_manager_get_subordinate_regularization_by_empid_not_found(client, admin_user):
    response = client.get(
        "manager/regularizations/employee/10",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


def test_admin_access_manager_update_regularization_status_by_id_success(client, admin_user):
    response = client.put(
        "/manager/regularizations/1/status",
        json={"regularization_status":"Rejected"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("update_subordinate_regularization_status_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_manager_update_regularization_status_by_id_forbidden(client, admin_user):
    response = client.put(
        "/manager/regularizations/6/status",
        json={"regularization_status":"Rejected"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Regularization not found under your management"}


def test_admin_access_manager_update_regularization_status_by_id_not_found(client, admin_user):
    response = client.put(
        "/manager/regularizations/16/status",
        json={"regularization_status":"Rejected"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Regularization request not found"}

# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_admin_access_admin_get_regularization_by_id_success(client, admin_user):
    response = client.get(
        "/admin/regularizations/1",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_employee_regularization_by_id_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_admin_get_regularization_by_id_not_found(client, admin_user):
    response = client.get(
        "/admin/regularizations/100",
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Regularization request not found"}


def test_admin_access_admin_update_regularization_by_id_success(client, admin_user):
    response = client.put(
        "/admin/regularizations/1/status",
        json = {"regularization_status": "Rejected"},
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("update_employee_regularization_by_id_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_admin_update_regularization_by_id_not_found(client, admin_user):
    response = client.put(
        "/admin/regularizations/100/status",
        json = {"regularization_status": "Rejected"},
        headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Regularization request not found"}