# -------------------------------------------------Test User API ---------------------------------------------------
def test_admin_get_all_roles_success(client, admin_user, read_json):
    response = client.get(
        "/user/my/roles/", headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("expected_responses/admin/roles/user_get_all_roles.json")

    assert response.status_code == 200
    assert response.json() == expected


def test_admin_get_role_by_id_success(client, admin_user, read_json):
    response = client.get(
        "/user/my/roles/id/4", headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("expected_responses/admin/roles/user_get_sales_role.json")

    assert response.status_code == 200
    assert response.json() == expected


def test_admin_get_role_by_id_not_found(client, admin_user, read_json):
    response = client.get(
        "/user/my/roles/id/14", headers={"Authorization": f"Bearer {admin_user}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Role not found"}


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_admin_access_admin_create_role_success(client, admin_user, read_json):
    payload = {"role": "string"}
    response = client.post(
        "/admin/roles/", json=payload, headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 201
    assert response.json() == {"role": "string", "role_id": 6}


def test_admin_access_admin_create_role_conflict(client, admin_user, read_json):
    payload = {"role": "Accountant"}
    response = client.post(
        "/admin/roles/", json=payload, headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Role already exists"}


def test_admin_access_admin_update_role_by_id_success(client, admin_user, read_json):
    response = client.put(
        "/admin/roles/id/1",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 200
    assert response.json() == {"role": "HR", "role_id": 1}


def test_admin_access_admin_update_role_by_id_conflict(client, admin_user, read_json):
    response = client.put(
        "/admin/roles/id/1",
        params={"new_name": "Developer"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Role with this name already exists"}


def test_admin_access_admin_update_role_by_id_not_found(client, admin_user, read_json):
    response = client.put(
        "/admin/roles/id/10",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Role not found"}


def test_admin_access_admin_delete_role_by_id_success(client, admin_user, read_json):
    response = client.delete(
        "/admin/roles/id/1", headers={"Authorization": f"Bearer {admin_user}"}
    )

    assert response.status_code == 200
    assert response.json() == {"detail": "Role deleted successfully"}


def test_admin_access_admin_delete_role_by_id_not_found(client, admin_user, read_json):
    response = client.delete(
        "/admin/roles/id/10", headers={"Authorization": f"Bearer {admin_user}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Role not found"}


def test_admin_access_admin_update_role_by_name_success(client, admin_user, read_json):
    response = client.put(
        "/admin/roles/name/Accountant",
        params={"new_name": "Majdur"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 200
    assert response.json() == {"role": "Majdur", "role_id": 4}


def test_admin_access_admin_update_role_by_name_conflict(client, admin_user, read_json):
    response = client.put(
        "/admin/roles/name/Accountant",
        params={"new_name": "Developer"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Role with this name already exists"}


def test_admin_access_admin_update_role_by_name_not_found(
    client, admin_user, read_json
):
    response = client.put(
        "/admin/roles/name/Altu Jalaltu",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Role not found"}


def test_admin_access_admin_delete_role_by_name_success(client, admin_user, read_json):
    response = client.delete(
        "/admin/roles/name/HR Executive",
        headers={"Authorization": f"Bearer {admin_user}"},
    )

    assert response.status_code == 200
    assert response.json() == {"detail": "Role deleted successfully"}


def test_admin_access_admin_delete_role_by_name_not_found(
    client, admin_user, read_json
):
    response = client.delete(
        "/admin/roles/name/Human Resources",
        headers={"Authorization": f"Bearer {admin_user}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Role not found"}
