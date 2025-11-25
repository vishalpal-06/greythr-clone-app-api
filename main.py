from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine
from database import models
from routers import auth
from routers.admin import admin_employee_api, admin_role_api, admin_department_api, admin_attedence_api
from routers.user import user_employee_api, user_role_api, user_department_api, user_attendence_api
from routers.manager import manager_employee_api,manager_attendance_api

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
app.include_router(admin_role_api.router)
app.include_router(user_role_api.router)
app.include_router(admin_department_api.router)
app.include_router(user_department_api.router)
app.include_router(admin_attedence_api.router)
app.include_router(user_attendence_api.router)
app.include_router(manager_attendance_api.router)

models.Base.metadata.create_all(bind=engine)