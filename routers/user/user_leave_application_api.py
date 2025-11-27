# api/user_leave_application_api.py
from fastapi import APIRouter, status
from typing import List
from schema.leave_application_schema import (
    LeaveApplicationCreate, LeaveApplicationResponse, LeaveApplicationStatusUpdate, Status
)
from routers.auth import db_dependency, user_dependency
from common.leave_application import (
    create_leave_application, delete_leave_application,
    get_my_applications_by_status, get_my_application_by_id, get_my_applications_by_month
)

router = APIRouter(prefix="/my/leave-applications", tags=["My - Leave Applications"])


@router.post("/", response_model=LeaveApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_leave_application_endpoint(app_in: LeaveApplicationCreate, db: db_dependency, user: user_dependency):
    return create_leave_application(db=db, app_in=app_in, user=user)


@router.delete("/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leave_using_id(app_id: int, db: db_dependency, user: user_dependency):
    delete_leave_application(db=db, app_id=app_id, user=user)


@router.get("/status/{status}", response_model=List[LeaveApplicationResponse])
def get_application_by_status(status: Status, db: db_dependency, user: user_dependency):
    return get_my_applications_by_status(db=db, user=user, status=status)


@router.get("/{app_id}", response_model=LeaveApplicationResponse)
def get_by_id(app_id: int, db: db_dependency, user: user_dependency):
    return get_my_application_by_id(db=db, app_id=app_id, user=user)


@router.get("/month/{year}/{month}", response_model=List[LeaveApplicationResponse])
def get_all_leave_by_month(year: int, month: int, db: db_dependency, user: user_dependency):
    return get_my_applications_by_month(db=db, year=year, month=month, user=user)