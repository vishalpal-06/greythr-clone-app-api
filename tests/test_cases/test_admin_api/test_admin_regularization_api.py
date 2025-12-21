# -------------------------------------------------Test Manager API ---------------------------------------------------
def test_admin_create_my_regularization_fail(client, admin_user, read_json):
    payload = {
        "regularization_start_time": "2025-11-30T10:00:00.000Z",
        "regularization_end_time": "2025-11-30T19:00:00.000Z",
        "regularization_reason": "mera man nahi tha kam kerne ka",
    }
    response = client.post(
        "/user/my/regularizations/",
        json=payload,
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "You have no manager assigned"}


# -------------------------------------------------Test Manager API ---------------------------------------------------
def test_admin_access_manager_get_subordinate_regularization_by_status_success(
    client, admin_user, read_json
):
    response = client.get(
        "/manager/regularizations/pending",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json(
        "expected_responses/admin/regularization/get_subordinate_regularization_by_status_admin.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_manager_get_subordinate_regularization_by_id_success(
    client, admin_user, read_json
):
    response = client.get(
        "manager/regularizations/1",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json(
        "expected_responses/admin/regularization/get_subordinate_regularization_by_id_admin.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_manager_get_subordinate_regularization_by_id_forbidden(
    client, admin_user, read_json
):
    response = client.get(
        "manager/regularizations/4",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Regularization not found under your management"
    }


def test_admin_access_manager_get_subordinate_regularization_by_id_not_found(
    client, admin_user, read_json
):
    response = client.get(
        "manager/regularizations/15",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Regularization request not found"}


def test_admin_access_manager_get_subordinate_regularization_by_empid_success(
    client, admin_user, read_json
):
    response = client.get(
        "manager/regularizations/employee/2",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json(
        "expected_responses/admin/regularization/get_subordinate_regularization_by_empid_admin.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_manager_get_subordinate_regularization_by_empid_forbidden(
    client, admin_user, read_json
):
    response = client.get(
        "manager/regularizations/employee/1",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_admin_access_manager_get_subordinate_regularization_by_empid_not_found(
    client, admin_user, read_json
):
    response = client.get(
        "manager/regularizations/employee/10",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


def test_admin_access_manager_update_regularization_status_by_id_success(
    client, admin_user, read_json
):
    response = client.put(
        "/manager/regularizations/1/status",
        json={"regularization_status": "Rejected"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json(
        "expected_responses/admin/regularization/update_subordinate_regularization_status_admin.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_manager_update_regularization_status_by_id_forbidden(
    client, admin_user, read_json
):
    response = client.put(
        "/manager/regularizations/6/status",
        json={"regularization_status": "Rejected"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Regularization not found under your management"
    }


def test_admin_access_manager_update_regularization_status_by_id_not_found(
    client, admin_user, read_json
):
    response = client.put(
        "/manager/regularizations/16/status",
        json={"regularization_status": "Rejected"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Regularization request not found"}


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_admin_access_admin_get_regularization_by_id_success(
    client, admin_user, read_json
):
    response = client.get(
        "/admin/regularizations/1", headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json(
        "expected_responses/admin/regularization/get_employee_regularization_by_id_admin.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_admin_get_regularization_by_id_not_found(
    client, admin_user, read_json
):
    response = client.get(
        "/admin/regularizations/100", headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Regularization request not found"}


def test_admin_access_admin_update_regularization_by_id_success(
    client, admin_user, read_json
):
    response = client.put(
        "/admin/regularizations/1/status",
        json={"regularization_status": "Rejected"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json(
        "expected_responses/admin/regularization/update_employee_regularization_by_id_admin.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_access_admin_update_regularization_by_id_not_found(
    client, admin_user, read_json
):
    response = client.put(
        "/admin/regularizations/100/status",
        json={"regularization_status": "Rejected"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Regularization request not found"}
