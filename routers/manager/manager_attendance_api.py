# routers/manager_attendance_api.py
from datetime import date

from fastapi import APIRouter

from common.attendance import (
    get_manager_subordinate_attendance_by_date,
    get_manager_team_attendance_by_date,
)
from routers.auth import db_dependency, user_dependency
from schema.attendance_schema import AttendanceResponse

router = APIRouter(
    prefix="/attendance",
    tags=["Manager - Attendance"],
)


@router.get("/date/{punch_date}", response_model=list[AttendanceResponse])
def get_team_attendance_by_date(
    punch_date: date,
    db: db_dependency,
    user: user_dependency,
):
    return get_manager_team_attendance_by_date(punch_date=punch_date, db=db, user=user)


@router.get("/employee/{employee_id}/date/{punch_date}", response_model=list[AttendanceResponse])
def get_subordinate_attendance_by_date(
    employee_id: int,
    punch_date: date,
    db: db_dependency,
    user: user_dependency,
):
    return get_manager_subordinate_attendance_by_date(
        employee_id=employee_id,
        punch_date=punch_date,
        db=db,
        user=user,
    )
