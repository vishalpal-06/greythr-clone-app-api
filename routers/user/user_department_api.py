# routers/user_role_api.py
from fastapi import APIRouter
from typing import List
from schema.department_schema import DepartmentResponse
from common.department import get_all_departments, get_department_by_id
from routers.auth import db_dependency, user_dependency

router = APIRouter(prefix="/user/departments", tags=["User - Departments"])


@router.get("/", response_model=List[DepartmentResponse])
def get_all_departments_endpoint(db: db_dependency, user: user_dependency):
    return get_all_departments(db=db, user=user)


@router.get("/id/{department_id}", response_model=DepartmentResponse)
def get_department_by_id_endpoint(department_id: int, db: db_dependency, user: user_dependency):
    return get_department_by_id(db=db, department_id=department_id)