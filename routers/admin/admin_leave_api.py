# api/admin_leave_api.py
from fastapi import APIRouter, HTTPException, status
from typing import Annotated, List
from common.leave import (
    get_leave_by_employee_and_year,
    get_all_leaves_by_employee_id,
    get_leave_years_by_employee,
    create_leave,
    delete_leave,
    delete_leave_by_employee_and_year,
)
import schema.leave_schema as leave_schema
from routers.auth import db_dependency, user_dependency
from common.common import _require_admin

router = APIRouter(prefix="/leaves", tags=["Admin - Leave"])


@router.get("/employee/{employee_id}/year/{year}", response_model=leave_schema.LeaveResponse)
def get_employee_leave_by_year_endpoint(employee_id: int, year: int, db: db_dependency, user: user_dependency):
    _require_admin(user)
    return get_leave_by_employee_and_year(db, employee_id, year)


@router.get("/employee/{employee_id}", response_model=List[leave_schema.LeaveResponse])
def get_all_leave_by_empid_endpoint(employee_id: int, db: db_dependency, user: user_dependency):
    _require_admin(user)
    return get_all_leaves_by_employee_id(db, employee_id)


@router.get("/employee/{employee_id}/years", response_model=List[int])
def get_leave_years_endpoint(employee_id: int, db: db_dependency, user: user_dependency):
    _require_admin(user)
    return get_leave_years_by_employee(db, employee_id)


@router.post("/", response_model=leave_schema.LeaveResponse, status_code=201)
def post_leave_endpoint(leave_in: leave_schema.LeaveCreate, db: db_dependency, user: user_dependency):
    _require_admin(user)
    return create_leave(db, leave_in)


@router.delete("/{leave_id}", status_code=204)
def delete_leave_endpoint(leave_id: int, db: db_dependency, user: user_dependency):
    _require_admin(user)
    delete_leave(db, leave_id)


@router.delete("/employee/{employee_id}/year/{year}", status_code=204)
def delete_by_employee_and_year_endpoint(employee_id: int, year: int, db: db_dependency, user: user_dependency):
    _require_admin(user)
    delete_leave_by_employee_and_year(db, employee_id, year)