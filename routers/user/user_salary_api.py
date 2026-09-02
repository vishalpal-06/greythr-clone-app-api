# api/user_salary_api.py

from fastapi import APIRouter

import schema.salary_schema as salary_schema
from common.salary import (
    get_salaries_by_employee_id,
    get_salary_by_employee_and_year,
)
from routers.auth import db_dependency, user_dependency

router = APIRouter(prefix="/my/salary", tags=["My - Salary"])


@router.get("/year/{year}", response_model=salary_schema.SalaryResponse)
def get_my_salary_by_year_endpoint(year: int, db: db_dependency, user: user_dependency):
    emp_id = user["id"]
    return get_salary_by_employee_and_year(db=db, employee_id=emp_id, year=year)


@router.get("/", response_model=list[salary_schema.SalaryResponse])
def get_my_all_salaries_endpoint(db: db_dependency, user: user_dependency):
    emp_id = user["id"]
    return get_salaries_by_employee_id(db=db, employee_id=emp_id)
