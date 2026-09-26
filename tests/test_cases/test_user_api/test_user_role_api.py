import pytest


# -----------------------------------Test User API -----------------------------------
def test_user_get_all_roles_success(client, user_A1, read_json):
    response = client.get("/user/my/roles/", headers={"Authorization": f"Bearer {user_A1}"})
    expected = read_json("expected_responses/user/roles/get_all_roles_userA1.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_role_by_id_success(client, user_A1, read_json):
    response = client.get("/user/my/roles/id/4", headers={"Authorization": f"Bearer {user_A1}"})
    expected = read_json("expected_responses/user/roles/get_role_by_id_userA1.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_role_by_id_not_found(client, user_A1, read_json):
    response = client.get("/user/my/roles/id/14", headers={"Authorization": f"Bearer {user_A1}"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Role not found"}


# ------------------------------Test Admin API -------------------------------


@pytest.mark.parametrize(
    ("method", "url", "kwargs"),
    [
        ("post", "/admin/roles/", {"json": {"role": "string"}}),
        ("put", "/admin/roles/id/1", {"params": {"new_name": "HR"}}),
        ("delete", "/admin/roles/id/1", {}),
        (
            "put",
            "/admin/roles/name/Human Resources",
            {"params": {"new_name": "HR"}},
        ),
        ("delete", "/admin/roles/name/Human Resources", {}),
    ],
)
def test_user_admin_access_role_forbidden(client, user_A1, method, url, kwargs):
    response = getattr(client, method)(
        url,
        headers={"Authorization": f"Bearer {user_A1}"},
        **kwargs,
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
