# routers/user_role_api.py
from fastapi import APIRouter
from typing import List
from schema.role_schema import RoleResponse
from common.role import get_all_roles, get_role_by_id
from routers.auth import db_dependency, user_dependency

router = APIRouter(prefix="/my/roles", tags=["My - Roles"])


@router.get("/", response_model=List[RoleResponse])
def list_all_roles_endpoint(db: db_dependency, user: user_dependency):
    return get_all_roles(db=db)


@router.get("/id/{role_id}", response_model=RoleResponse)
def get_role_endpoint(role_id: int, db: db_dependency, user: user_dependency):
    return get_role_by_id(db=db, role_id=role_id)