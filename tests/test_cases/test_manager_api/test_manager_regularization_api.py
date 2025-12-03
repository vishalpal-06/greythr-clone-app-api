import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent / "expected_responses/manager/regularization/"

def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)

# -------------------------------------------------Test User API ---------------------------------------------------
def test_manager_get_all_my_regularization_success(client, manager_A):
    response = client.get(
        "/user/my/regularizations/",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    expected = read_json("get_all_my_regularization_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_create_my_regularization_success(client, manager_A):
    payload = {"regularization_start_time": "2025-11-30T10:00:00.000Z",
               "regularization_end_time": "2025-11-30T19:00:00.000Z",
               "regularization_reason": "mera man nahi tha kam kerne ka"
    }
    response = client.post(
        "/user/my/regularizations/",
        json = payload,
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    expected = read_json("create_my_regularization_manager_A.json")
    assert response.status_code == 201
    assert response.json() == expected


def test_manager_get_my_regularization_by_id_success(client, manager_A):
    response = client.get(
        "user/my/regularizations/2",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    expected = read_json("get_my_regularization_by_id_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_others_regularization_by_id_forbidden(client, manager_A):
    response = client.get(
        "user/my/regularizations/5",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized"}


def test_manager_get_my_regularization_by_year_and_month_success(client, manager_A):
    response = client.get(
        "/user/my/regularizations/month/2025/1",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    expected = read_json("get_regularization_by_year_month_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_my_regularization_by_year_and_month_not_found(client, manager_A):
    response = client.get(
        "/user/my/regularizations/month/2025/11",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 200
    assert response.json() == []


# -------------------------------------------------Test Manager API ---------------------------------------------------
def test_manager_manager_access_get_subordinate_regularization_by_status_success(client, manager_A):
    response = client.get(
        "/manager/regularizations/pending",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("get_regularization_by_status_for_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_manager_access_get_subordinate_regularization_by_id_success(client, manager_A):
    response = client.get(
        "manager/regularizations/4",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("get_regularization_by_id_for_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_manager_access_get_subordinate_regularization_by_id_forbidden(client, manager_A):
    response = client.get(
        "manager/regularizations/1",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Regularization not found under your management"}


def test_manager_manager_access_get_subordinate_regularization_by_id_not_found(client, manager_A):
    response = client.get(
        "manager/regularizations/15",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Regularization request not found"}


def test_manager_manager_access_get_subordinate_regularization_by_empid_success(client, manager_A):
    response = client.get(
        "manager/regularizations/employee/4",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("get_regularization_by_empid_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_manager_access_get_subordinate_regularization_by_empid_forbidden(client, manager_A):
    response = client.get(
        "manager/regularizations/employee/1",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_manager_manager_access_get_subordinate_regularization_by_empid_not_found(client, manager_A):
    response = client.get(
        "manager/regularizations/employee/10",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


def test_manager_manager_access_update_subordinate_regularization_status_by_id_success(client, manager_A):
    response = client.put(
        "/manager/regularizations/3/status",
        json={"regularization_status":"Rejected"},
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("update_regularization_status_for_Manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_manager_access_update_subordinate_regularization_status_by_id_forbidden(client, manager_A):
    response = client.put(
        "/manager/regularizations/6/status",
        json={"regularization_status":"Rejected"},
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Regularization not found under your management"}


def test_manager_manager_access_update_subordinate_regularization_status_by_id_not_found(client, manager_A):
    response = client.put(
        "/manager/regularizations/16/status",
        json={"regularization_status":"Rejected"},
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Regularization request not found"}

# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_manager_admin_access_get_regularization_by_id_forbidden(client, manager_A):
    response = client.get(
        "/admin/regularizations/1",
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_update_regularization_by_id_forbidden(client, manager_A):
    response = client.put(
        "/admin/regularizations/1/status",
        json = {"regularization_status": "Rejected"},
        headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}




















