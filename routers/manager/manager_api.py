from fastapi import APIRouter

from . import (
    manager_employee_api,
    manager_attendance_api,
    manager_leave_api,
    manager_regularization_api,
    manager_leave_application_api,
    manager_expense_claim_api
)

manager_router = APIRouter(prefix="/manager")

manager_router.include_router(manager_employee_api.router)
manager_router.include_router(manager_attendance_api.router)
manager_router.include_router(manager_leave_api.router)
manager_router.include_router(manager_regularization_api.router)
manager_router.include_router(manager_leave_application_api.router)
manager_router.include_router(manager_expense_claim_api.router)
