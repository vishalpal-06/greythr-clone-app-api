import json
from pathlib import Path

BASE_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "expected_responses/user/departments/"
)


def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)


# -------------------------------------------------Test User API ---------------------------------------------------
def test_user_get_all_departments_success(client, user_A2):
    response = client.get(
        "/user/my/departments/", headers={"Authorization": f"Bearer {user_A2}"}
    )
    expected = read_json("get_all_departments_userA2.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_department_by_id_success(client, user_B1):
    response = client.get(
        "/user/my/departments/id/4", headers={"Authorization": f"Bearer {user_B1}"}
    )
    expected = read_json("get_department_by_id_userB1.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_department_by_id_not_found(client, user_B2):
    response = client.get(
        "/user/my/departments/id/14", headers={"Authorization": f"Bearer {user_B2}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Department not found"}


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_user_admin_access_create_department_forbidden(client, user_A1):
    payload = {"department_name": "string"}
    response = client.post(
        "/admin/departments/",
        json=payload,
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_update_department_by_id_forbidden(client, user_A1):
    response = client.put(
        "/admin/departments/id/1",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_update_department_by_name_forbidden(client, user_A1):
    response = client.put(
        "/admin/departments/name/Human Resources",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_delete_department_by_id_forbidden(client, user_A1):
    response = client.delete(
        "/admin/departments/id/1", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_delete_department_by_name_forbidden(client, user_A1):
    response = client.delete(
        "/admin/departments/name/Human Resources",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
