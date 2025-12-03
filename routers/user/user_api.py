from fastapi import APIRouter

from . import (
    user_employee_api,
    user_role_api,
    user_department_api,
    user_attendance_api,
    user_salary_api,
    user_leave_api,
    user_regularization_api,
    user_payslip_api,
    user_leave_application_api,
    user_expense_claim_api,
)

user_router = APIRouter(prefix="/user")

user_router.include_router(user_employee_api.router)
user_router.include_router(user_role_api.router)
user_router.include_router(user_department_api.router)
user_router.include_router(user_attendance_api.router)
user_router.include_router(user_salary_api.router)
user_router.include_router(user_leave_api.router)
user_router.include_router(user_regularization_api.router)
user_router.include_router(user_payslip_api.router)
user_router.include_router(user_leave_application_api.router)
user_router.include_router(user_expense_claim_api.router)
