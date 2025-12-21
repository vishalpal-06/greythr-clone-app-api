# -------------------------------------------------Test User API ---------------------------------------------------
def test_admin_get_all_departments_success(client, admin_user, read_json):
    response = client.get(
        "/user/my/departments/", headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json(
        "expected_responses/admin/departments/user_get_all_departments.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_get_department_by_id_success(client, admin_user, read_json):
    response = client.get(
        "/user/my/departments/id/4", headers={"Authorization": f"Bearer {admin_user}"}
    )

    expected = read_json(
        "expected_responses/admin/departments/user_get_sales_department.json"
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_admin_get_department_by_id_not_found(client, admin_user, read_json):
    response = client.get(
        "/user/my/departments/id/14", headers={"Authorization": f"Bearer {admin_user}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Department not found"}


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_admin_access_admin_create_department_success(client, admin_user, read_json):
    payload = {"department_name": "string"}
    response = client.post(
        "/admin/departments/",
        json=payload,
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 201
    assert response.json() == {"department_name": "string", "department_id": 6}


def test_admin_access_admin_create_department_conflict(client, admin_user, read_json):
    payload = {"department_name": "Engineering"}
    response = client.post(
        "/admin/departments/",
        json=payload,
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Department already exists"}


def test_admin_access_admin_update_department_by_id_success(
    client, admin_user, read_json
):
    response = client.put(
        "/admin/departments/id/1",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )

    assert response.status_code == 200
    assert response.json() == {"department_name": "HR", "department_id": 1}


def test_admin_access_admin_update_department_by_id_conflict(
    client, admin_user, read_json
):
    response = client.put(
        "/admin/departments/id/1",
        params={"new_name": "Engineering"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Department with this name already exists"}


def test_admin_access_admin_update_department_by_id_not_found(
    client, admin_user, read_json
):
    response = client.put(
        "/admin/departments/id/10",
        params={"new_name": "Altu Jalaltu"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Department not found"}


def test_admin_access_admin_delete_department_by_id_success(
    client, admin_user, read_json
):
    response = client.delete(
        "/admin/departments/id/1", headers={"Authorization": f"Bearer {admin_user}"}
    )

    assert response.status_code == 200
    assert response.json() == {"detail": "Department deleted successfully"}


def test_admin_access_admin_delete_department_by_id_not_found(
    client, admin_user, read_json
):
    response = client.delete(
        "/admin/departments/id/10", headers={"Authorization": f"Bearer {admin_user}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Department not found"}


def test_admin_access_admin_update_department_by_name_success(
    client, admin_user, read_json
):
    response = client.put(
        "/admin/departments/name/Human Resources",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )

    assert response.status_code == 200
    assert response.json() == {"department_name": "HR", "department_id": 2}


def test_admin_access_admin_update_department_by_name_conflict(
    client, admin_user, read_json
):
    response = client.put(
        "/admin/departments/name/Human Resources",
        params={"new_name": "Engineering"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Department with this name already exists"}


def test_admin_access_admin_update_department_by_name_not_found(
    client, admin_user, read_json
):
    response = client.put(
        "/admin/departments/name/Faltu Department",
        params={"new_name": "HR"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Department not found"}


def test_admin_access_admin_delete_department_by_name_success(
    client, admin_user, read_json
):
    response = client.delete(
        "/admin/departments/name/Human Resources",
        headers={"Authorization": f"Bearer {admin_user}"},
    )

    assert response.status_code == 200
    assert response.json() == {"detail": "Department deleted successfully"}


def test_admin_access_admin_delete_department_by_name_forbidden(
    client, admin_user, read_json
):
    response = client.delete(
        "/admin/departments/name/Faltu Department",
        headers={"Authorization": f"Bearer {admin_user}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Department not found"}
