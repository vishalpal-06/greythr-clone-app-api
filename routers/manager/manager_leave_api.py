# api/manager_leave_api.py
from fastapi import APIRouter
from typing import List

from common.leave import (
    get_leave_by_employee_and_year,
    get_all_leaves_by_employee_id,
)
import schema.leave_schema as leave_schema
from routers.auth import db_dependency, user_dependency
from common.employee import get_subordinate_by_id


router = APIRouter(prefix="/leaves", tags=["Manager - Leave"])


@router.get(
    "/employee/{employee_id}/year/{year}",
    response_model=leave_schema.LeaveResponse,
    summary="Get leave record of a subordinate for a specific year",
)
def get_subordinate_leave_by_year_endpoint_endpoint(
    employee_id: int,
    year: int,
    db: db_dependency,
    user: user_dependency,
):
    # This function already checks: is employee_id under current manager?
    # If not → raises 404 or 403 depending on your get_subordinate_by_id logic
    get_subordinate_by_id(employee_id=employee_id, db=db, user=user)

    return get_leave_by_employee_and_year(db=db, employee_id=employee_id, year=year)


@router.get(
    "/employee/{employee_id}",
    response_model=List[leave_schema.LeaveResponse],
    summary="Get all leave records of a subordinate",
)
def get_subordinate_all_leaves_endpoint(
    employee_id: int,
    db: db_dependency,
    user: user_dependency,
):
    # Authorization: confirm this employee reports to current user
    get_subordinate_by_id(employee_id=employee_id, db=db, user=user)

    return get_all_leaves_by_employee_id(db=db, employee_id=employee_id)
