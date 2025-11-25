from schema.employee_schema import EmployeeResponse
from routers.auth import db_dependency, user_dependency
from fastapi import APIRouter
from common.employee import (
    get_my_details_common
)


router = APIRouter(
    prefix='/user',
    tags=['User => Employee']
)


@router.get("/get_my_details/", response_model=EmployeeResponse)
def get_my_details(db: db_dependency, user : user_dependency):
    return get_my_details_common(db=db, user=user)


