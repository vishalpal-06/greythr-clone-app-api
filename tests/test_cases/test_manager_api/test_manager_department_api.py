# -------------------------------------------------Test User API ---------------------------------------------------
def test_manager_get_all_departments_success(client, manager_A, read_json):
    response = client.get(
        "/user/my/departments/", headers={"Authorization": f"Bearer {manager_A}"}
    )
    expected = read_json(
        "expected_responses/manager/departments/get_all_departments_manager_A.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_department_by_id_success(client, manager_A, read_json):
    response = client.get(
        "/user/my/departments/id/4", headers={"Authorization": f"Bearer {manager_A}"}
    )

    expected = read_json(
        "expected_responses/manager/departments/get_department_by_id_manager_A.json"
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_department_by_id_not_found(client, manager_A, read_json):
    response = client.get(
        "/user/my/departments/id/14", headers={"Authorization": f"Bearer {manager_A}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Department not found"}


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_manager_admin_access_create_department_forbidden(client, manager_A, read_json):
    payload = {"department_name": "string"}
    response = client.post(
        "/admin/departments/",
        json=payload,
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_update_department_by_id_forbidden(
    client, manager_A, read_json
):
    response = client.put(
        "/admin/departments/id/1",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {manager_A}"},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_delete_department_by_id_forbidden(
    client, manager_A, read_json
):
    response = client.delete(
        "/admin/departments/id/1", headers={"Authorization": f"Bearer {manager_A}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_update_department_by_name_forbidden(
    client, manager_A, read_json
):
    response = client.put(
        "/admin/departments/name/Human Resources",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {manager_A}"},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_delete_department_by_name_forbidden(
    client, manager_A, read_json
):
    response = client.delete(
        "/admin/departments/name/Human Resources",
        headers={"Authorization": f"Bearer {manager_A}"},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
