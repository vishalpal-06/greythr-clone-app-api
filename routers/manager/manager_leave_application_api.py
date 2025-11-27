# api/manager_leave_application_api.py
from fastapi import APIRouter
from typing import List
from schema.leave_application_schema import LeaveApplicationResponse, LeaveApplicationStatusUpdate, Status
from routers.auth import db_dependency, user_dependency
from common.leave_application import (
    get_manager_application_by_id, get_manager_applications_by_status,
    get_manager_applications_by_month, get_manager_applications_by_employee,
    manager_update_status
)

router = APIRouter(prefix="/leave-applications", tags=["Manager - Leave Applications"])


@router.put("/{app_id}/status", response_model=LeaveApplicationResponse)
def put_leave_status_where_manager_currentuser(
    app_id: int, update: LeaveApplicationStatusUpdate, db: db_dependency, user: user_dependency
):
    return manager_update_status(db=db, app_id=app_id, update=update, user=user)


@router.get("/status/{status}", response_model=List[LeaveApplicationResponse])
def get_by_status_where_manager_currentuser(status: Status, db: db_dependency, user: user_dependency):
    return get_manager_applications_by_status(db=db, status=status, user=user)


@router.get("/month/{year}/{month}", response_model=List[LeaveApplicationResponse])
def get_by_month_where_manager_currentuser(year: int, month: int, db: db_dependency, user: user_dependency):
    return get_manager_applications_by_month(db=db, year=year, month=month, user=user)


@router.get("/employee/{emp_id}", response_model=List[LeaveApplicationResponse])
def get_by_employeeid_where_manager_currentuser(emp_id: int, db: db_dependency, user: user_dependency):
    return get_manager_applications_by_employee(db=db, emp_id=emp_id, user=user)