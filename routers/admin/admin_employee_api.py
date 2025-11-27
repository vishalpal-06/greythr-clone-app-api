# routers/admin_employee_api.py
from fastapi import APIRouter, status
from typing import List
from schema.employee_schema import EmployeeResponse, EmployeeCreate, EmployeeUpdate
from routers.auth import db_dependency, user_dependency
from common.employee import (
    get_all_employees,
    get_employee_by_id,
    get_employee_by_email,
    create_employee,
    update_employee_by_id,
    update_employee_by_email,
    delete_employee_by_id,
    delete_employee_by_email,
)

router = APIRouter(prefix="/employees", tags=["Admin - Employees"])


@router.get("/", response_model=List[EmployeeResponse])
def list_all_employees_endpoint(db: db_dependency, user: user_dependency):
    return get_all_employees(db=db, user=user)


@router.get("/id/{employee_id}", response_model=EmployeeResponse)
def retrieve_employee_by_id_endpoint(employee_id: int, db: db_dependency, user: user_dependency):
    return get_employee_by_id(employee_id=employee_id, db=db, user=user)


@router.get("/email/{email}", response_model=EmployeeResponse)
def retrieve_employee_by_email_endpoint(email: str, db: db_dependency, user: user_dependency):
    return get_employee_by_email(email=email, db=db, user=user)


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def register_employee_endpoint(employee: EmployeeCreate, db: db_dependency, user: user_dependency):
    return create_employee(employee_data=employee, db=db, user=user)


@router.put("/id/{employee_id}", response_model=EmployeeResponse)
def update_employee_by_id_endpoint(
    employee_id: int,
    update_data: EmployeeUpdate,
    db: db_dependency,
    user: user_dependency
):
    return update_employee_by_id(employee_id, update_data, db, user)


@router.put("/email/{email}", response_model=EmployeeResponse)
def update_employee_by_email_endpoint(
    email: str,
    update_data: EmployeeUpdate,
    db: db_dependency,
    user: user_dependency
):
    return update_employee_by_email(email, update_data, db, user)


@router.delete("/id/{employee_id}", status_code=status.HTTP_200_OK)
def remove_employee_by_id_endpoint(employee_id: int, db: db_dependency, user: user_dependency):
    return delete_employee_by_id(employee_id, db, user)


@router.delete("/email/{email}", status_code=status.HTTP_200_OK)
def remove_employee_by_email_endpoint(email: str, db: db_dependency, user: user_dependency):
    return delete_employee_by_email(email, db, user)