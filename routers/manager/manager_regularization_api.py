# api/manager_regularization_api.py
from fastapi import APIRouter
from typing import List
from schema.regularization_schema import (
    RegularizationResponse,
    RegularizationStatusUpdate,
)
from routers.auth import db_dependency, user_dependency
from common.regularization import (
    get_manager_regularization_by_id,
    get_manager_regularizations_for_employee,
    get_manager_pending_regularizations,
    manager_update_regularization_status,
)

router = APIRouter(prefix="/regularizations", tags=["Manager - Regularization"])


@router.get("/pending", response_model=List[RegularizationResponse])
def get_pending(db: db_dependency, user: user_dependency):
    return get_manager_pending_regularizations(db=db, user=user)


@router.get("/{reg_id}", response_model=RegularizationResponse)
def get_by_id(reg_id: int, db: db_dependency, user: user_dependency):
    return get_manager_regularization_by_id(reg_id=reg_id, db=db, user=user)


@router.get("/employee/{employee_id}", response_model=List[RegularizationResponse])
def get_by_employee(employee_id: int, db: db_dependency, user: user_dependency):
    return get_manager_regularizations_for_employee(
        employee_id=employee_id, db=db, user=user
    )


@router.put("/{reg_id}/status", response_model=RegularizationResponse)
def update_status(
    reg_id: int,
    status_update: RegularizationStatusUpdate,
    db: db_dependency,
    user: user_dependency,
):
    return manager_update_regularization_status(
        reg_id=reg_id, status_update=status_update, db=db, user=user
    )
