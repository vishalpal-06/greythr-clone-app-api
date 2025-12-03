# api/admin_salary_api.py
from fastapi import APIRouter
from typing import List

from common.salary import (
    get_salaries_by_year,
    get_salary_by_employee_and_year,
    get_salaries_by_employee_id,
    create_salary,
    delete_salary,
    delete_salary_by_employee_and_year,
)
import schema.salary_schema as salary_schema
from common.common import _require_admin
from routers.auth import db_dependency, user_dependency

router = APIRouter(prefix="/salaries", tags=["Admin - Salary"])


# Only these lines change — everything else stays same


@router.get("/year/{year}", response_model=List[salary_schema.SalaryResponse])
def get_all_employee_salary_by_year(
    year: int, db: db_dependency, user: user_dependency
):
    _require_admin(user)
    return get_salaries_by_year(db, year=year)  # raises 404 if empty


@router.get(
    "/employee/{employee_id}/year/{year}", response_model=salary_schema.SalaryResponse
)
def get_specific_employee_salary_by_year(
    employee_id: int, year: int, db: db_dependency, user: user_dependency
):
    _require_admin(user)
    return get_salary_by_employee_and_year(db, employee_id=employee_id, year=year)


@router.get(
    "/employee/{employee_id}/salaries",
    response_model=List[salary_schema.SalaryResponse],
)
def get_employee_all_salaries(
    employee_id: int, db: db_dependency, user: user_dependency
):
    _require_admin(user)
    return get_salaries_by_employee_id(db, employee_id=employee_id)


@router.post("/", response_model=salary_schema.SalaryResponse, status_code=201)
def post_salary(
    salary_in: salary_schema.SalaryCreate, db: db_dependency, user: user_dependency
):
    _require_admin(user)
    return create_salary(db=db, salary=salary_in)


@router.delete("/{salary_id}", status_code=204)
def delete_salary_endpoint(salary_id: int, db: db_dependency, user: user_dependency):
    _require_admin(user)
    delete_salary(db=db, salary_id=salary_id)  # raises 404 if not found
    return None


@router.delete("/employee/{employee_id}/year/{year}", status_code=204)
def delete_salary_by_employee_and_year_endpoint(
    employee_id: int,
    year: int,
    db: db_dependency,
    user: user_dependency,
):
    _require_admin(user)
    delete_salary_by_employee_and_year(db=db, employee_id=employee_id, year=year)
