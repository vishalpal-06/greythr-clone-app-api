# routers/admin_attendance_api.py
from fastapi import APIRouter, Query
from typing import List
from schema.attendance_schema import AttendanceResponse
from common.attendance import (
    get_all_attendance,
    get_attendance_by_date_all_employees,
    get_attendance_by_date_one_employee,
    get_all_attendance_of_employee
)
from routers.auth import db_dependency, user_dependency
from datetime import datetime

router = APIRouter(prefix="/admin/attendance", tags=["Admin - Attendance"])


@router.get("/", response_model=List[AttendanceResponse])
def list_all_attendance(db: db_dependency, user: user_dependency):
    return get_all_attendance(db=db, user=user)


@router.get("/date/{date_str}", response_model=List[AttendanceResponse])
def get_all_employees_attendance_on_date(
    punch_date: datetime,
    db: db_dependency,
    user: user_dependency
):
    return get_attendance_by_date_all_employees(db=db, punch_date=punch_date)


@router.get("/employee/{employee_id}/date/{punch_date}", response_model=List[AttendanceResponse])
def get_one_employee_attendance_on_date(
    employee_id: int,
    punch_date: datetime,
    db: db_dependency,
    user: user_dependency
):
    return get_attendance_by_date_one_employee(db=db, employee_id=employee_id, punch_date=punch_date, user=user)


@router.get("/employee/{employee_id}", response_model=List[AttendanceResponse])
def get_all_attendance_of_one_employee(
    employee_id: int,
    db: db_dependency,
    user: user_dependency
):
    return get_all_attendance_of_employee(db=db, employee_id=employee_id, user=user)