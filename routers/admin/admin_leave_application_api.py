# api/admin_leave_application_api.py
from fastapi import APIRouter
from typing import List
from schema.leave_application_schema import (
    LeaveApplicationResponse,
    LeaveApplicationStatusUpdate,
)
from routers.auth import db_dependency, user_dependency
from common.common import _require_admin
from common.leave_application import (
    get_application_by_id_admin,
    get_all_by_employee_admin,
    get_all_by_month_admin,
    admin_update_status,
)

router = APIRouter(prefix="/leave-applications", tags=["Admin - Leave Applications"])


@router.get("/{app_id}", response_model=LeaveApplicationResponse)
def get_application_by_id(app_id: int, db: db_dependency, user: user_dependency):
    _require_admin(user)
    return get_application_by_id_admin(db=db, app_id=app_id)


@router.get("/employee/{emp_id}", response_model=List[LeaveApplicationResponse])
def get_all_leave_by_employeeid(emp_id: int, db: db_dependency, user: user_dependency):
    _require_admin(user)
    return get_all_by_employee_admin(db=db, emp_id=emp_id)


@router.get("/month/{year}/{month}", response_model=List[LeaveApplicationResponse])
def get_all_leave_by_month(
    year: int, month: int, db: db_dependency, user: user_dependency
):
    _require_admin(user)
    return get_all_by_month_admin(db=db, year=year, month=month)


@router.put("/{app_id}/status", response_model=LeaveApplicationResponse)
def put_leave_status(
    app_id: int,
    update: LeaveApplicationStatusUpdate,
    db: db_dependency,
    user: user_dependency,
):
    _require_admin(user)
    return admin_update_status(db=db, app_id=app_id, update=update)
