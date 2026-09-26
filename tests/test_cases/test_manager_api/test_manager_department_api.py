import pytest


# -----------------------------------Test User API -----------------------------------
def test_manager_get_all_departments_success(client, manager_A, read_json):
    response = client.get("/user/my/departments/", headers={"Authorization": f"Bearer {manager_A}"})
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


# ------------------------------Test Admin API -------------------------------
@pytest.mark.parametrize(
    ("method", "url", "kwargs"),
    [
        ("post", "/admin/departments/", {"json": {"department_name": "string"}}),
        ("put", "/admin/departments/id/1", {"params": {"new_name": "HR"}}),
        ("delete", "/admin/departments/id/1", {}),
        (
            "put",
            "/admin/departments/name/Human Resources",
            {"params": {"new_name": "HR"}},
        ),
        ("delete", "/admin/departments/name/Human Resources", {}),
    ],
)
def test_manager_admin_access_department_forbidden(
    client,
    manager_A,
    method,
    url,
    kwargs,
):
    response = getattr(client, method)(
        url,
        headers={"Authorization": f"Bearer {manager_A}"},
        **kwargs,
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
