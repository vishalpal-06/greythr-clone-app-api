import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent / "expected_responses/user/departments/"

def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)

# -------------------------------------------------test user api ---------------------------------------------------
def test_user_get_all_departments(client, user_A1):
    response = client.get(
        "/user/my/departments/",
        headers={"Authorization": f"Bearer {user_A1}"}
    )
    expected = read_json("user_get_all_departments.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_Sales_departments(client, user_A1):
    response = client.get(
        "/user/my/departments/id/4",
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    expected = read_json("user_get_sales_department.json")

    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_departments_not_found(client, user_A1):
    response = client.get(
        "/user/my/departments/id/14",
        headers={"Authorization": f"Bearer {user_A1}"}
    )
    
    assert response.status_code == 404
    assert response.json() == {'detail': 'Department not found'}


# -------------------------------------------------test admin api ---------------------------------------------------
def test_user_create_department(client, user_A1):
    payload = {
        "department_name": "string"
    }

    response = client.post(
        "/admin/departments/",
        json=payload,
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_update_department_using_id(client, user_A1):
    response = client.put(
        "/admin/departments/id/1",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_delete_departments_using_id(client, user_A1):
    response = client.delete(
        "/admin/departments/id/1",
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_update_department_using_name(client, user_A1):
    response = client.put(
        "/admin/departments/name/Human Resources",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_delete_departments_using_name(client, user_A1):
    response = client.delete(
        "/admin/departments/name/Human Resources",
        headers={"Authorization": f"Bearer {user_A1}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
