import pytest


# -----------------------------------Test User API -----------------------------------
def test_user_get_all_departments_success(client, user_A2, read_json):
    response = client.get("/user/my/departments/", headers={"Authorization": f"Bearer {user_A2}"})
    expected = read_json("expected_responses/user/departments/get_all_departments_userA2.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_department_by_id_success(client, user_B1, read_json):
    response = client.get(
        "/user/my/departments/id/4", headers={"Authorization": f"Bearer {user_B1}"}
    )
    expected = read_json("expected_responses/user/departments/get_department_by_id_userB1.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_department_by_id_not_found(client, user_B2):
    response = client.get(
        "/user/my/departments/id/14", headers={"Authorization": f"Bearer {user_B2}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Department not found"}


# ------------------------------Test Admin API -------------------------------
@pytest.mark.parametrize(
    ("method", "url", "kwargs"),
    [
        ("post", "/admin/departments/", {"json": {"department_name": "string"}}),
        ("put", "/admin/departments/id/1", {"params": {"new_name": "HR"}}),
        (
            "put",
            "/admin/departments/name/Human Resources",
            {"params": {"new_name": "HR"}},
        ),
        ("delete", "/admin/departments/id/1", {}),
        ("delete", "/admin/departments/name/Human Resources", {}),
    ],
)
def test_user_admin_access_department_forbidden(client, user_A1, method, url, kwargs):
    response = getattr(client, method)(
        url,
        headers={"Authorization": f"Bearer {user_A1}"},
        **kwargs,
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
