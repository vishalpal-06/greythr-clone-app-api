from schema.employee_schema import EmployeeResponse
from routers.auth import db_dependency, user_dependency
from fastapi import APIRouter
from common.employee import (
    get_employee_by_id_for_manager_common,
    get_employee_by_email_for_manager_common
)


router = APIRouter(
    prefix='/manager',
    tags=['Manager => Employee']
)


@router.get("/get_employee_by_id/", response_model=EmployeeResponse)
def get_employee_by_id_manager(employee_id:int ,db: db_dependency, user : user_dependency):
    return get_employee_by_id_for_manager_common(employee_id=employee_id, db=db, user=user)



@router.get("/get_employee_by_email/", response_model=EmployeeResponse)
def get_employee_by_email_manager(email:str, db: db_dependency, user : user_dependency):
    return get_employee_by_email_for_manager_common(employee_email=email, db=db, user=user)

