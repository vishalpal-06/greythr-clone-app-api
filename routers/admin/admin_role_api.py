# routers/admin_role_api.py
from fastapi import APIRouter, status
from typing import List
from schema.role_schema import RoleResponse, RoleCreate
from common.role import (
    create_role,
    update_role_by_id,
    update_role_by_name,
    delete_role_by_id,
    delete_role_by_name,
)
from routers.auth import db_dependency, user_dependency

router = APIRouter(prefix="/roles", tags=["Admin - Roles"])


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_new_role_endpoint(
    role_data: RoleCreate, db: db_dependency, user: user_dependency
):
    return create_role(db=db, role_name=role_data.role, user=user)


# Update by ID
@router.put("/id/{role_id}", response_model=RoleResponse)
def rename_role_by_id_endpoint(
    role_id: int, new_name: str, db: db_dependency, user: user_dependency
):
    return update_role_by_id(db=db, role_id=role_id, new_role_name=new_name, user=user)


# Update by name
@router.put("/name/{current_name}", response_model=RoleResponse)
def rename_role_by_name_endpoint(
    current_name: str, new_name: str, db: db_dependency, user: user_dependency
):
    return update_role_by_name(
        db=db, current_role_name=current_name, new_role_name=new_name, user=user
    )


# Delete by ID
@router.delete("/id/{role_id}")
def remove_role_by_id_endpoint(role_id: int, db: db_dependency, user: user_dependency):
    return delete_role_by_id(db=db, role_id=role_id, user=user)


# Delete by name
@router.delete("/name/{role_name}")
def remove_role_by_name_endpoint(
    role_name: str, db: db_dependency, user: user_dependency
):
    return delete_role_by_name(db=db, role_name=role_name, user=user)
