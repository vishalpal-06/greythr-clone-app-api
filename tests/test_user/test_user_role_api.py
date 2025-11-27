import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent / "expected_responses/user/roles/"

def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)

# -------------------------------------------------test user api ---------------------------------------------------
def test_user_get_all_roles(client, user_token):
    response = client.get(
        "/user/my/roles/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    expected = read_json("user_get_all_roles.json")

    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_Sales_roles(client, user_token):
    response = client.get(
        "/user/my/roles/id/4",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    expected = read_json("user_get_sales_role.json")

    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_roles_not_found(client, user_token):
    response = client.get(
        "/user/my/roles/id/14",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 404
    assert response.json() == {'detail': 'Role not found'}


# -------------------------------------------------test admin api ---------------------------------------------------
def test_user_create_role(client, user_token):
    payload = {
        "role": "string"
    }

    response = client.post(
        "/admin/roles/",
        json=payload,
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_update_role_using_id(client, user_token):
    response = client.put(
        "/admin/roles/id/1",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_delete_roles_using_id(client, user_token):
    response = client.delete(
        "/admin/roles/id/1",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_update_role_using_name(client, user_token):
    response = client.put(
        "/admin/roles/name/Human Resources",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_delete_roles_using_name(client, user_token):
    response = client.delete(
        "/admin/roles/name/Human Resources",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
