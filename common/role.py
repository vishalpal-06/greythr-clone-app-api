# common/role.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from database.models import Role
from typing import Dict, Any
from common.common import _require_admin


def _get_role_by_id(db: Session, role_id: int) -> Role:
    role = db.query(Role).filter(Role.role_id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


def _get_role_by_name(db: Session, role_name: str) -> Role:
    role = db.query(Role).filter(Role.role.ilike(role_name.strip())).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


# === READ ===
def get_all_roles(db: Session):
    return db.query(Role).all()


def get_role_by_id(db: Session, role_id: int):
    return _get_role_by_id(db, role_id)


# === ADMIN: CREATE ===
def create_role(db: Session, role_name: str, user: dict) -> Role:
    _require_admin(user)
    role_name = role_name.strip()
    if db.query(Role).filter(Role.role.ilike(role_name)).first():
        raise HTTPException(status_code=400, detail="Role already exists")

    new_role = Role(role=role_name)
    db.add(new_role)
    db.commit()
    return new_role


# === ADMIN: UPDATE BY ID ===
def update_role_by_id(
    db: Session, role_id: int, new_role_name: str, user: dict
) -> Role:
    _require_admin(user)
    role = _get_role_by_id(db, role_id)

    new_name = new_role_name.strip()

    if (
        db.query(Role)
        .filter(Role.role.ilike(new_name), Role.role_id != role_id)
        .first()
    ):
        raise HTTPException(
            status_code=400, detail="Role with this name already exists"
        )

    role.role = new_name
    db.commit()
    return role


# === ADMIN: UPDATE BY NAME ===
def update_role_by_name(
    db: Session, current_role_name: str, new_role_name: str, user: dict
) -> Role:
    _require_admin(user)
    role = _get_role_by_name(db, current_role_name)

    new_name = new_role_name.strip()

    if db.query(Role).filter(Role.role.ilike(new_name)).first():
        raise HTTPException(
            status_code=400, detail="Role with this name already exists"
        )

    role.role = new_name
    db.commit()
    return role


# === ADMIN: DELETE BY ID ===
def delete_role_by_id(db: Session, role_id: int, user: dict) -> Dict[str, str]:
    _require_admin(user)
    role = _get_role_by_id(db, role_id)
    db.delete(role)
    db.commit()
    return {"detail": "Role deleted successfully"}


# === ADMIN: DELETE BY NAME ===
def delete_role_by_name(db: Session, role_name: str, user: dict) -> Dict[str, str]:
    _require_admin(user)
    role = _get_role_by_name(db, role_name)
    db.delete(role)
    db.commit()
    return {"detail": "Role deleted successfully"}
