# -------------------------------------------------Test User API ---------------------------------------------------
def test_manager_get_all_roles_success(client, manager_A, read_json):
    response = client.get(
        "/user/my/roles/", headers={"Authorization": f"Bearer {manager_A}"}
    )
    expected = read_json(
        "expected_responses/manager/roles/get_all_roles_manager_A.json"
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_role_by_id_success(client, manager_A, read_json):
    response = client.get(
        "/user/my/roles/id/4", headers={"Authorization": f"Bearer {manager_A}"}
    )
    expected = read_json(
        "expected_responses/manager/roles/get_role_by_id_manager_A.json"
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_role_by_id_not_found(client, manager_A, read_json):
    response = client.get(
        "/user/my/roles/id/14", headers={"Authorization": f"Bearer {manager_A}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Role not found"}


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_manager_admin_access_create_role_forbidden(client, manager_A, read_json):
    payload = {"role": "string"}
    response = client.post(
        "/admin/roles/", json=payload, headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_update_role_by_id_forbidden(client, manager_A, read_json):
    response = client.put(
        "/admin/roles/id/1",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_delete_role_by_id_forbidden(client, manager_A, read_json):
    response = client.delete(
        "/admin/roles/id/1", headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_update_role_by_name_forbidden(
    client, manager_A, read_json
):
    response = client.put(
        "/admin/roles/name/Human Resources",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_delete_role_by_name_forbidden(
    client, manager_A, read_json
):
    response = client.delete(
        "/admin/roles/name/Human Resources",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
