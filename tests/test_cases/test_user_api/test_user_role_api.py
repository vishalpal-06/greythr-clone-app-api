import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent / "expected_responses/user/roles/"

def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)

# -------------------------------------------------test user api ---------------------------------------------------
def test_user_get_all_roles_success(client, user_A1):
    response = client.get(
        "/user/my/roles/",
        headers={"Authorization": f"Bearer {user_A1}"}
    )
    expected = read_json("get_all_roles_userA1.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_role_by_id_success(client, user_A1):
    response = client.get(
        "/user/my/roles/id/4",
        headers={"Authorization": f"Bearer {user_A1}"}
    )
    expected = read_json("get_role_by_id_userA1.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_role_by_id_not_found(client, user_A1):
    response = client.get(
        "/user/my/roles/id/14",
        headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Role not found'}


# -------------------------------------------------test admin api ---------------------------------------------------
def test_user_admin_access_create_role_forbidden(client, user_A1):
    payload = {
        "role": "string"
    }
    response = client.post(
        "/admin/roles/",
        json=payload,
        headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_update_role_by_id_forbidden(client, user_A1):
    response = client.put(
        "/admin/roles/id/1",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_delete_role_by_id_forbidden(client, user_A1):
    response = client.delete(
        "/admin/roles/id/1",
        headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_update_role_by_name_forbidden(client, user_A1):
    response = client.put(
        "/admin/roles/name/Human Resources",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_delete_role_by_name_forbidden(client, user_A1):
    response = client.delete(
        "/admin/roles/name/Human Resources",
        headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
