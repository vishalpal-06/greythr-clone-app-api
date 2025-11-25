# routers/user_attendance_api.py
from fastapi import APIRouter, Query
from typing import List
from schema.attendance_schema import AttendanceCreate, AttendanceResponse
from common.attendance import (
    create_attendance,
    get_my_attendance_all,
    get_my_attendance_by_date
)
from routers.auth import db_dependency, user_dependency
from datetime import datetime

router = APIRouter(prefix="/user/attendance", tags=["User - Attendance"])


@router.post("/", response_model=AttendanceResponse, status_code=201)
def punch_in(att_data: AttendanceCreate, db: db_dependency, user: user_dependency):
    return create_attendance(db=db, punch_time=att_data.punch_time, current_user=user)


@router.get("/my", response_model=List[AttendanceResponse])
def get_my_all_attendance(db: db_dependency, user: user_dependency):
    return get_my_attendance_all(db=db, current_user=user)


@router.get("/my/date/{date_str}", response_model=List[AttendanceResponse])
def get_my_attendance_by_date_endpoint(db: db_dependency, date_str: datetime, user: user_dependency):
    return get_my_attendance_by_date(db=db, punch_date = date_str, user=user)