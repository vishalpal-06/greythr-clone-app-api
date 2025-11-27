# routers/admin_department_api.py
from fastapi import APIRouter, status
from typing import List
from schema.department_schema import DepartmentResponse, DepartmentCreate
from common.department import (
    create_department,
    update_department_by_id,
    update_department_by_name,
    delete_department_by_id,
    delete_department_by_name,
)
from routers.auth import db_dependency, user_dependency

router = APIRouter(prefix="/departments", tags=["Admin - Departments"])


@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_new_department_endpoint(department_data: DepartmentCreate, db: db_dependency, user: user_dependency):
    return create_department(db=db, department_name=department_data.department_name, user=user)


# Update by ID
@router.put("/id/{department_id}", response_model=DepartmentResponse)
def rename_department_by_id_endpoint(department_id: int, new_name: str, db: db_dependency, user: user_dependency):
    return update_department_by_id(db=db, department_id=department_id, new_department_name=new_name, user=user)


# Update by name
@router.put("/name/{current_name}", response_model=DepartmentResponse)
def rename_department_by_name_endpoint(current_name: str, new_name: str, db: db_dependency, user: user_dependency):
    return update_department_by_name(db=db, current_department_name=current_name, new_department_name=new_name, user=user)


# Delete by ID
@router.delete("/id/{department_id}")
def remove_department_by_id_endpoint(department_id: int, db: db_dependency, user: user_dependency):
    return delete_department_by_id(db=db, department_id=department_id, user=user)


# Delete by name
@router.delete("/name/{department_name}")
def remove_department_by_name_endpoint(department_name: str, db: db_dependency, user: user_dependency):
    return delete_department_by_name(db=db, department_name=department_name, user=user)