# common/department.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from database.models import Department
from typing import Dict, Any
from routers.auth import db_dependency, user_dependency
from common.common import _require_admin


def _get_department_by_id(db: db_dependency, department_id: int) -> Department:
    department = (
        db.query(Department).filter(Department.department_id == department_id).first()
    )
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


def _get_department_by_name(db: db_dependency, department_name: str) -> Department:
    department = (
        db.query(Department)
        .filter(Department.department_name.ilike(department_name.strip()))
        .first()
    )
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


# === READ ===
def get_all_departments(db: db_dependency, user: user_dependency):
    return db.query(Department).all()


def get_department_by_id(db: db_dependency, department_id: int):
    return _get_department_by_id(db, department_id)


# === ADMIN: CREATE ===
def create_department(
    db: db_dependency, department_name: str, user: dict
) -> Department:
    _require_admin(user)
    department_name = department_name.strip()
    if (
        db.query(Department)
        .filter(Department.department_name.ilike(department_name))
        .first()
    ):
        raise HTTPException(status_code=400, detail="Department already exists")

    new_department = Department(department_name=department_name)
    db.add(new_department)
    db.commit()
    return new_department


# === ADMIN: UPDATE BY ID ===
def update_department_by_id(
    db: db_dependency, department_id: int, new_department_name: str, user: dict
) -> Department:
    _require_admin(user)
    department = _get_department_by_id(db, department_id)

    new_name = new_department_name.strip()
    if (
        db.query(Department)
        .filter(
            Department.department_name.ilike(new_name),
            Department.department_id != department_id,
        )
        .first()
    ):
        raise HTTPException(
            status_code=400, detail="Department with this name already exists"
        )

    department.department_name = new_name
    db.commit()
    return department


# === ADMIN: UPDATE BY NAME ===
def update_department_by_name(
    db: db_dependency,
    current_department_name: str,
    new_department_name: str,
    user: dict,
) -> Department:
    _require_admin(user)
    department = _get_department_by_name(db, current_department_name)

    new_name = new_department_name.strip()
    if db.query(Department).filter(Department.department_name.ilike(new_name)).first():
        raise HTTPException(
            status_code=400, detail="Department with this name already exists"
        )

    department.department_name = new_name
    db.commit()
    return department


# === ADMIN: DELETE BY ID ===
def delete_department_by_id(
    db: db_dependency, department_id: int, user: dict
) -> Dict[str, str]:
    _require_admin(user)
    department = _get_department_by_id(db, department_id)
    db.delete(department)
    db.commit()
    return {"detail": "Department deleted successfully"}


# === ADMIN: DELETE BY NAME ===
def delete_department_by_name(
    db: db_dependency, department_name: str, user: dict
) -> Dict[str, str]:
    _require_admin(user)
    department = _get_department_by_name(db, department_name)
    db.delete(department)
    db.commit()
    return {"detail": "Department deleted successfully"}
