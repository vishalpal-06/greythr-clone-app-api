import json
from pathlib import Path

BASE_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "expected_responses/admin/leave_applications/"
)


def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)


# -------------------------------------------------Test User API ---------------------------------------------------
def test_admin_create_leave_application_fail(client, admin_user):
    payload = {
        "from_date": "2025-11-30T10:00:00.000Z",
        "end_date": "2025-11-30T19:00:00.000Z",
        "leave_reason": "string",
    }
    response = client.post(
        "/user/my/leave-applications/",
        json=payload,
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail":"No manager assigned"}


def test_admin_delete_my_leave_application_by_id_success(client, admin_user):
    response = client.delete(
        "/user/my/leave-applications/7",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 204


def test_admin_delete_my_leave_application_by_id_not_allow(client, admin_user):
    response = client.delete(
        "/user/my/leave-applications/8",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail":"Cannot delete approved/rejected leave"}


def test_admin_delete_others_leave_application_by_id_forbidden(client, admin_user):
    response = client.delete(
        "/user/my/leave-applications/4",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized"}


def test_admin_delete_leave_application_not_exist_by_id_not_found(client, admin_user):
    response = client.delete(
        "/user/my/leave-applications/14",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Leave application not found"}


def test_admin_get_others_leave_application_by_id_forbidden(client, admin_user):
    response = client.get(
        "/user/my/leave-applications/5",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized"}


def test_admin_get_leave_application_not_exist_by_id_not_found(client, admin_user):
    response = client.get(
        "/user/my/leave-applications/15",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Leave application not found"}


# -------------------------------------------------Test Manager API ---------------------------------------------------
def test_admin_manager_access_update_subordinate_leave_application_status_by_id_success(
    client, admin_user
):
    response = client.put(
        "manager/leave-applications/6/status",
        json={"leave_status": "Rejected"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("update_subordinate_leave_application_status_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_manager_access_update_subordinate_leave_application_status_by_id_forbidden(
    client, admin_user
):
    response = client.put(
        "manager/leave-applications/3/status",
        json={"leave_status": "Approved"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Leave Application not found under your management"
    }


def test_admin_manager_access_update_subordinate_leave_application_not_exist_status_by_id_not_found(
    client, admin_user
):
    response = client.put(
        "manager/leave-applications/11/status",
        json={"leave_status": "Approved"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Leave application not found"}


def test_admin_manager_access_get_subordinate_leave_applications_by_status_success(
    client, admin_user
):
    response = client.get(
        "/manager/leave-applications/status/Pending",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_subordinate_leave_application_by_status_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_manager_access_get_leave_applications_by_year_and_month_success(
    client, manager_B
):
    response = client.get(
        "/manager/leave-applications/month/2025/5",
        headers={"Authorization": f"Bearer {manager_B}"},
    )
    expected = read_json(
        "get_subordinate_leave_application_by_year_and_month_admin.json"
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_manager_access_get_leave_applications_by_year_and_month_not_found(
    client, admin_user
):
    response = client.get(
        "/manager/leave-applications/month/2025/11",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_admin_manager_access_get_subordinate_leave_applications_by_empid_success(
    client, admin_user
):
    response = client.get(
        "/manager/leave-applications/employee/3",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_subordinate_leave_application_by_empid_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_manager_access_get_subordinate_leave_applications_by_empid_forbidden(
    client, admin_user
):
    response = client.get(
        "/manager/leave-applications/employee/4",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_admin_manager_access_get_subordinate_leave_applications_by_empid_not_exist(
    client, admin_user
):
    response = client.get(
        "/manager/leave-applications/employee/12",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_admin_admin_access_get_employee_leave_application_by_id_success(
    client, admin_user
):
    response = client.get(
        "/admin/leave-applications/1", headers={"Authorization": f"Bearer {admin_user}"}
    )
    expected = read_json("get_employee_leave_application_by_id_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_get_employee_leave_application_by_id_not_found(
    client, admin_user
):
    response = client.get(
        "/admin/leave-applications/30", headers={"Authorization": f"Bearer {admin_user}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Leave application not found"}


def test_admin_admin_access_get_employee_leave_application_by_empid_success(
    client, admin_user
):
    response = client.get(
        "/admin/leave-applications/employee/4",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_employee_leave_application_by_empid_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_get_employee_leave_application_by_empid_not_found(
    client, admin_user
):
    response = client.get(
        "/admin/leave-applications/employee/10",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No leave applications found"}


def test_admin_admin_access_get_employee_leave_application_by_year_and_month_success(
    client, admin_user
):
    response = client.get(
        "/admin/leave-applications/month/2025/5",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("get_employee_leave_application_by_year_and_month_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_get_employee_leave_application_by_year_and_month_not_found(
    client, admin_user
):
    response = client.get(
        "/admin/leave-applications/month/2026/11",
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No applications in this month"}


def test_admin_admin_access_update_employee_leave_application_status_by_id_success(
    client, admin_user
):
    response = client.put(
        "/admin/leave-applications/1/status",
        json={"leave_status": "Approved"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    expected = read_json("update_employee_leave_application_status_by_id_admin.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_admin_admin_access_update_employee_leave_application_status_by_id_not_found(
    client, admin_user
):
    response = client.put(
        "/admin/leave-applications/10/status",
        json={"leave_status": "Approved"},
        headers={"Authorization": f"Bearer {admin_user}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail":"Leave application not found"}