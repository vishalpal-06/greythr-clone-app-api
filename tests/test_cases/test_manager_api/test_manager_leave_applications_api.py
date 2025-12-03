import json
from pathlib import Path

BASE_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "expected_responses/manager/leave_applications/"
)


def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)


# -------------------------------------------------Test User API ---------------------------------------------------
def test_manager_create_leave_application_success(client, manager_A):
    payload = {
        "from_date": "2025-11-30T10:00:00.000Z",
        "end_date": "2025-11-30T19:00:00.000Z",
        "leave_reason": "string",
    }
    response = client.post(
        "/user/my/leave-applications/",
        json=payload,
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("create_leave_application_manager_A.json")
    assert response.status_code == 201
    assert response.json() == expected


def test_manager_delete_my_leave_application_by_id_success(client, manager_B):
    response = client.delete(
        "/user/my/leave-applications/6",
        headers={"Authorization": f"Bearer {manager_B}"},
    )
    assert response.status_code == 204


def test_manager_delete_others_leave_application_by_id_forbidden(client, manager_A):
    response = client.delete(
        "/user/my/leave-applications/4",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized"}


def test_manager_delete_leave_application_not_exist_by_id_not_found(client, manager_A):
    response = client.delete(
        "/user/my/leave-applications/14",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Leave application not found"}


def test_manager_get_my_leave_application_by_id_success(client, manager_B):
    response = client.get(
        "/user/my/leave-applications/6",
        headers={"Authorization": f"Bearer {manager_B}"},
    )
    expected = read_json("get_my_leave_application_by_id_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_others_leave_application_by_id_forbidden(client, manager_A):
    response = client.get(
        "/user/my/leave-applications/5",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized"}


def test_manager_get_leave_application_not_exist_by_id_not_found(client, manager_A):
    response = client.get(
        "/user/my/leave-applications/15",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Leave application not found"}


def test_manager_get_my_leave_application_by_status_success(client, manager_A):
    response = client.get(
        "/user/my/leave-applications/status/Pending",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_manager_get_my_leave_application_by_year_and_month_success(client, manager_B):
    response = client.get(
        "/user/my/leave-applications/month/2025/5",
        headers={"Authorization": f"Bearer {manager_B}"},
    )
    expected = read_json("get_leave_application_by_year_and_month_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_get_my_leave_application_by_year_and_month_not_found(
    client, manager_A
):
    response = client.get(
        "/user/my/leave-applications/month/2025/11",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 200
    assert response.json() == []


# -------------------------------------------------Test Manager API ---------------------------------------------------
def test_manager_manager_access_update_leave_application_status_by_id_success(
    client, manager_A
):
    response = client.put(
        "manager/leave-applications/1/status",
        json={"leave_status": "Rejected"},
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("update_leave_application_status_for_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_manager_access_update_leave_application_status_by_id_forbidden(
    client, manager_A
):
    response = client.put(
        "manager/leave-applications/3/status",
        json={"leave_status": "Approved"},
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Leave Application not found under your management"
    }


def test_manager_manager_access_update_leave_application_not_exist_status_by_id_not_found(
    client, manager_A
):
    response = client.put(
        "manager/leave-applications/11/status",
        json={"leave_status": "Approved"},
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Leave application not found"}


def test_manager_manager_access_get_leave_applications_by_status_success(
    client, manager_A
):
    response = client.get(
        "/manager/leave-applications/status/Pending",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    expected = read_json("get_leave_application_by_status_manager_A.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_manager_access_get_leave_applications_by_year_and_month_success(
    client, manager_B
):
    response = client.get(
        "/manager/leave-applications/month/2025/5",
        headers={"Authorization": f"Bearer {manager_B}"},
    )
    expected = read_json(
        "get_leave_application_of_emp_by_year_and_month_manager_A.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_manager_manager_access_get_leave_applications_by_year_and_month_not_found(
    client, manager_A
):
    response = client.get(
        "/manager/leave-applications/month/2025/11",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_manager_manager_access_leave_applications_by_empid_not_under_manager_forbidden(
    client, manager_A
):
    response = client.get(
        "/manager/leave-applications/employee/2",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_manager_manager_access_leave_applications_by_empid_not_exist_not_found(
    client, manager_A
):
    response = client.get(
        "/manager/leave-applications/employee/12",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_manager_admin_access_get_employee_leave_application_by_id_forbidden(
    client, manager_A
):
    response = client.get(
        "/admin/leave-applications/1", headers={"Authorization": f"Bearer {manager_A}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_get_employee_leave_application_by_empid_forbidden(
    client, manager_A
):
    response = client.get(
        "/admin/leave-applications/employee/1",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_get_employee_leave_application_by_year_and_month_forbidden(
    client, manager_A
):
    response = client.get(
        "/admin/leave-applications/month/2026/11",
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_manager_admin_access_update_employee_leave_application_status_by_id_forbidden(
    client, manager_A
):
    response = client.put(
        "/admin/leave-applications/1/status",
        json={"leave_status": "Approved"},
        headers={"Authorization": f"Bearer {manager_A}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
