from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine
from database import models
from routers import auth,employee

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
app.include_router(employee.router)

models.Base.metadata.create_all(bind=engine)