import json
from pathlib import Path

BASE_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "expected_responses/user/regularization/"
)


def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)


# -------------------------------------------------Test User API ---------------------------------------------------
def test_user_get_all_my_regularization_success(client, user_A1):
    response = client.get(
        "/user/my/regularizations/", headers={"Authorization": f"Bearer {user_A1}"}
    )
    expected = read_json("get_all_my_regularization_userA1.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_create_my_regularization_success(client, user_A1):
    payload = {
        "regularization_start_time": "2025-11-30T10:00:00.000Z",
        "regularization_end_time": "2025-11-30T19:00:00.000Z",
        "regularization_reason": "mera man nahi tha kam kerne ka",
    }
    response = client.post(
        "/user/my/regularizations/",
        json=payload,
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    expected = read_json("create_regularization_userA1.json")
    assert response.status_code == 201
    assert response.json() == expected


def test_user_get_my_regularization_by_id_success(client, user_A1):
    response = client.get(
        "user/my/regularizations/3", headers={"Authorization": f"Bearer {user_A1}"}
    )
    expected = read_json("get_my_regularization_by_id_userA1.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_others_regularization_by_id_forbidden(client, user_A1):
    response = client.get(
        "user/my/regularizations/1", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized"}


def test_user_get_my_regularization_by_year_and_month_success(client, user_A1):
    response = client.get(
        "/user/my/regularizations/month/2025/4",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    expected = read_json("get_regularization_by_year_month_userA1.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_my_regularization_by_year_and_month_not_found(client, user_A1):
    response = client.get(
        "/user/my/regularizations/month/2025/1",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 200
    assert response.json() == []


# -------------------------------------------------Test Manager API ---------------------------------------------------
def test_user_manager_access_get_subordinate_regularization_by_status_success(
    client, user_A1
):
    response = client.get(
        "/manager/regularizations/pending",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_user_manager_access_get_subordinate_regularization_by_id_forbidden(
    client, user_A1
):
    response = client.get(
        "manager/regularizations/1",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Regularization not found under your management"
    }


def test_user_manager_access_get_subordinate_regularization_by_empid_forbidden(
    client, user_A1
):
    response = client.get(
        "manager/regularizations/employee/1",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_user_manager_access_update_subordinate_regularization_by_id_not_allowed(
    client, user_A1
):
    response = client.get(
        "/manager/regularizations/1/status",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_user_admin_access_get_employee_regularization_by_id_forbidden(client, user_A1):
    response = client.get(
        "/admin/regularizations/1", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_update_employee_regularization_by_id_forbidden(
    client, user_A1
):
    response = client.put(
        "/admin/regularizations/1/status",
        json={"regularization_status": "Rejected"},
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
