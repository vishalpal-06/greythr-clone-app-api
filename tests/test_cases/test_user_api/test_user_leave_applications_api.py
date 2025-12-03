import json
from pathlib import Path

BASE_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "expected_responses/user/leave_applications/"
)


def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)


# -------------------------------------------------Test User API ---------------------------------------------------
def test_user_create_my_leave_application_success(client, user_A1):
    payload = {
        "from_date": "2025-11-30T10:00:00.000Z",
        "end_date": "2025-11-30T19:00:00.000Z",
        "leave_reason": "string",
    }
    response = client.post(
        "/user/my/leave-applications/",
        json=payload,
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    expected = read_json("create_my_leave_application_userA1.json")
    assert response.status_code == 201
    assert response.json() == expected


def test_user_delete_my_leave_application_by_id_success(client, user_A1):
    response = client.delete(
        "/user/my/leave-applications/1", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 204


def test_user_delete_others_leave_application_by_id_forbidden(client, user_A1):
    response = client.delete(
        "/user/my/leave-applications/4", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized"}


def test_user_delete_leave_application_not_exist_by_id_not_found(client, user_A1):
    response = client.delete(
        "/user/my/leave-applications/14", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Leave application not found"}


def test_user_get_my_leave_application_by_id_success(client, user_A1):
    response = client.get(
        "/user/my/leave-applications/1", headers={"Authorization": f"Bearer {user_A1}"}
    )
    expected = read_json("get_my_leave_application_by_id_userA1.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_others_leave_application_by_id_forbidden(client, user_A1):
    response = client.get(
        "/user/my/leave-applications/5", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized"}


def test_user_get_my_leave_application_not_exist_by_id_not_found(client, user_A1):
    response = client.get(
        "/user/my/leave-applications/15", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Leave application not found"}


def test_user_get_my_leave_application_by_status_success(client, user_A1):
    response = client.get(
        "/user/my/leave-applications/status/Pending",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    expected = read_json("get_my_leave_application_by_status_userA1.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_my_leave_application_by_year_and_month_success(client, user_A1):
    response = client.get(
        "/user/my/leave-applications/month/2025/6",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    expected = read_json("get_my_leave_application_by_year_and_month_userA1.json")
    assert response.status_code == 200
    assert response.json() == expected


def test_user_get_my_leave_application_by_year_and_month_not_found(client, user_A1):
    response = client.get(
        "/user/my/leave-applications/month/2025/11",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 200
    assert response.json() == []


# -------------------------------------------------Test Manager API ---------------------------------------------------
def test_user_manager_access_update_leave_application_status_by_id_forbidden(
    client, user_A1
):
    response = client.put(
        "manager/leave-applications/1/status",
        json={"leave_status": "Approved"},
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Leave Application not found under your management"
    }


def test_user_manager_access_update_leave_application_status_not_exist_by_id_not_found(
    client, user_A1
):
    response = client.put(
        "manager/leave-applications/11/status",
        json={"leave_status": "Approved"},
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Leave application not found"}


def test_user_manager_access_get_leave_applications_by_status_success(client, user_A1):
    response = client.get(
        "/manager/leave-applications/status/Pending",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_user_manager_access_get_leave_applications_by_year_and_month_success(
    client, user_A1
):
    response = client.get(
        "/manager/leave-applications/month/2025/11",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_user_manager_access_get_leave_applications_by_empid_nonsubordinate_forbidden(
    client, user_A1
):
    response = client.get(
        "/manager/leave-applications/employee/2",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found under your management"}


def test_user_manager_access_leave_applications_by_empid_not_exist_not_found(
    client, user_A1
):
    response = client.get(
        "/manager/leave-applications/employee/12",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


# -------------------------------------------------Test Admin API ---------------------------------------------------
def test_user_admin_access_get_employee_leave_application_by_id_forbidden(
    client, user_A1
):
    response = client.get(
        "/admin/leave-applications/1", headers={"Authorization": f"Bearer {user_A1}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_get_employee_leave_application_by_empid_forbidden(
    client, user_A1
):
    response = client.get(
        "/admin/leave-applications/employee/1",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_get_employee_leave_application_by_year_and_month_forbidden(
    client, user_A1
):
    response = client.get(
        "/admin/leave-applications/month/2026/11",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_user_admin_access_update_employee_leave_application_status_by_id_forbidden(
    client, user_A1
):
    response = client.put(
        "/admin/leave-applications/1/status",
        json={"leave_status": "Approved"},
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
