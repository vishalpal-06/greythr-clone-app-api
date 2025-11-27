from fastapi import APIRouter

from . import (
    admin_employee_api,
    admin_role_api,
    admin_department_api,
    admin_attendance_api,
    admin_salary_api,
    admin_leave_api,
    admin_regularization_api,
    admin_payslip_api,
    admin_leave_application_api,
    admin_expense_claim_api
)

admin_router = APIRouter(prefix="/admin")

admin_router.include_router(admin_employee_api.router)
admin_router.include_router(admin_role_api.router)
admin_router.include_router(admin_department_api.router)
admin_router.include_router(admin_attendance_api.router)
admin_router.include_router(admin_salary_api.router)
admin_router.include_router(admin_leave_api.router)
admin_router.include_router(admin_regularization_api.router)
admin_router.include_router(admin_payslip_api.router)
admin_router.include_router(admin_leave_application_api.router)
admin_router.include_router(admin_expense_claim_api.router)
