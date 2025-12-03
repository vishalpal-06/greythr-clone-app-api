# routers/user_employee_api.py
from fastapi import APIRouter
from schema.employee_schema import EmployeeResponse
from routers.auth import db_dependency, user_dependency
from common.employee import get_current_user_employee

router = APIRouter(prefix="/my", tags=["My - Employee"])


@router.get(
    "/me/",
    response_model=EmployeeResponse,
    summary="Get logged-in employee's own profile",
)
def get_my_profile_endpoint(db: db_dependency, user: user_dependency):
    return get_current_user_employee(db=db, user=user)
