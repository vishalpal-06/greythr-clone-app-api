from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine
from database import models
from routers import auth
from routers.admin import (
    admin_employee_api, 
    admin_role_api, 
    admin_department_api, 
    admin_attedence_api, 
    admin_salary_api,
    admin_leave_api,
    admin_regularization_api,
    admin_payslip_api,
    admin_leave_application_api,
    admin_expense_claim_api
)
from routers.user import (
    user_employee_api, 
    user_role_api, 
    user_department_api, 
    user_attendence_api, 
    user_salary_api, 
    user_leave_api,
    user_regularization_api,
    user_payslip_api,
    user_leave_application_api,
    user_expense_claim_api
)
from routers.manager import (
    manager_employee_api,
    manager_attendance_api,
    manager_leave_api,
    manager_regularization_api,
    manager_leave_application_api,
    manager_expense_claim_api
)

app = FastAPI(
    title="Grethr Clone API",
    description="A simplified version of the Grethr API built with FastAPI.",
    version="1.0.0"
)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin_employee_api.router)
app.include_router(user_employee_api.router)
app.include_router(manager_employee_api.router)
# app.include_router(admin_role_api.router)
# app.include_router(user_role_api.router)
# app.include_router(admin_department_api.router)
# app.include_router(user_department_api.router)
# app.include_router(admin_attedence_api.router)
# app.include_router(user_attendence_api.router)
# app.include_router(manager_attendance_api.router)
# app.include_router(admin_salary_api.router)
# app.include_router(user_salary_api.router)
# app.include_router(admin_leave_api.router)
# app.include_router(user_leave_api.router)
# app.include_router(manager_leave_api.router)
# app.include_router(admin_regularization_api.router)
# app.include_router(user_regularization_api.router)
# app.include_router(manager_regularization_api.router)
# app.include_router(admin_payslip_api.router)
# app.include_router(user_payslip_api.router)
# app.include_router(admin_leave_application_api.router)
# app.include_router(user_leave_application_api.router)
# app.include_router(manager_leave_application_api.router)
app.include_router(admin_expense_claim_api.router)
app.include_router(user_expense_claim_api.router)
app.include_router(manager_expense_claim_api.router)

models.Base.metadata.create_all(bind=engine)