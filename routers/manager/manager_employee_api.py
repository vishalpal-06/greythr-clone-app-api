# routers/manager_employee_api.py
from fastapi import APIRouter
from schema.employee_schema import EmployeeResponse
from routers.auth import db_dependency, user_dependency
from common.employee import get_subordinate_by_id, get_subordinate_by_email

router = APIRouter(prefix="/subordinates", tags=["Manager - Subordinates"])


@router.get("/id/{employee_id}", response_model=EmployeeResponse)
def get_subordinate_by_id_endpoint(employee_id: int, db: db_dependency, user: user_dependency):
    return get_subordinate_by_id(employee_id=employee_id, db=db, user=user)


@router.get("/email/{email}", response_model=EmployeeResponse)
def get_subordinate_by_email_endpoint(email: str, db: db_dependency, user: user_dependency):
    return get_subordinate_by_email(email=email, db=db, user=user)