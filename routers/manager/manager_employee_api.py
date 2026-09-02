# routers/manager_employee_api.py
from fastapi import APIRouter

from common.employee import get_subordinate_by_email, get_subordinate_by_id
from routers.auth import db_dependency, user_dependency
from schema.employee_schema import EmployeeResponse

router = APIRouter(prefix="/subordinates", tags=["Manager - Subordinates"])


@router.get("/id/{employee_id}", response_model=EmployeeResponse)
def get_subordinate_by_id_endpoint(employee_id: int, db: db_dependency, user: user_dependency):
    return get_subordinate_by_id(employee_id=employee_id, db=db, user=user)


@router.get("/email/{email}", response_model=EmployeeResponse)
def get_subordinate_by_email_endpoint(email: str, db: db_dependency, user: user_dependency):
    return get_subordinate_by_email(email=email, db=db, user=user)
