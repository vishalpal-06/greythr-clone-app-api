# api/user_regularization_api.py
from fastapi import APIRouter, status
from typing import List
from schema.regularization_schema import RegularizationCreate, RegularizationResponse
from routers.auth import db_dependency, user_dependency
from common.regularization import (
    create_regularization,
    get_my_regularizations,
    get_my_regularization_by_id,
    get_my_regularizations_by_month,
)

router = APIRouter(prefix="/my/regularizations", tags=["My - Regularizations"])


@router.post(
    "/", response_model=RegularizationResponse, status_code=status.HTTP_201_CREATED
)
def create_regularization_endpoint(
    reg_in: RegularizationCreate, db: db_dependency, user: user_dependency
):
    return create_regularization(db=db, reg_in=reg_in, user=user)


@router.get("/", response_model=List[RegularizationResponse])
def get_all_my_regularizations(db: db_dependency, user: user_dependency):
    return get_my_regularizations(db=db, user=user)


@router.get("/{reg_id}", response_model=RegularizationResponse)
def get_my_regularization_by_id_endpoint(
    reg_id: int, db: db_dependency, user: user_dependency
):
    return get_my_regularization_by_id(reg_id=reg_id, db=db, user=user)


@router.get("/month/{year}/{month}", response_model=List[RegularizationResponse])
def get_by_month(year: int, month: int, db: db_dependency, user: user_dependency):
    return get_my_regularizations_by_month(year=year, month=month, db=db, user=user)
