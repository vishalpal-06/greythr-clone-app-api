from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine
from database import models
from routers.auth import auth_router
from routers.admin.admin_api import admin_router
from routers.manager.manager_api import manager_router
from routers.user.user_api import user_router

app = FastAPI(
    title="Grethr Clone API",
    description="A simplified version of the Grethr API built with FastAPI.",
    version="1.2.0",
)

origins = ["http://localhost:3000"]


@app.get("/")
def health_check():
    return {"status": "pass"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(manager_router)
app.include_router(user_router)

models.Base.metadata.create_all(bind=engine)
