# api/user_leave_api.py

from fastapi import APIRouter

import schema.leave_schema as leave_schema
from common.leave import get_all_leaves_by_employee_id, get_leave_by_employee_and_year
from routers.auth import db_dependency, user_dependency

router = APIRouter(prefix="/my/leave", tags=["My - Leave"])


@router.get("/year/{year}", response_model=leave_schema.LeaveResponse)
def get_my_leave_by_year_endpoint(year: int, db: db_dependency, user: user_dependency):
    emp_id = user["id"]
    return get_leave_by_employee_and_year(db, emp_id, year)


@router.get("/", response_model=list[leave_schema.LeaveResponse])
def get_my_all_leaves_endpoint(db: db_dependency, user: user_dependency):
    emp_id = user["id"]
    return get_all_leaves_by_employee_id(db, emp_id)
