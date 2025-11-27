# api/admin_regularization_api.py
from fastapi import APIRouter
from schema.regularization_schema import RegularizationResponse, RegularizationStatusUpdate
from routers.auth import db_dependency, user_dependency
from common.common import _require_admin
from common.regularization import get_regularization_by_id_admin, admin_update_status

router = APIRouter(prefix="/regularizations", tags=["Admin - Regularization"])


@router.get("/{reg_id}", response_model=RegularizationResponse)
def get_regularization_by_id(reg_id: int, db: db_dependency, user: user_dependency):
    _require_admin(user)
    return get_regularization_by_id_admin(reg_id=reg_id, db=db)


@router.put("/{reg_id}/status", response_model=RegularizationResponse)
def update_status(reg_id: int, status_update: RegularizationStatusUpdate, db: db_dependency, user: user_dependency):
    _require_admin(user)
    return admin_update_status(reg_id=reg_id, status_update=status_update, db=db)