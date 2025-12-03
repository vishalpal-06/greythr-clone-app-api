# /employee.py
from database.models import Employee
from fastapi import HTTPException, status
from schema.employee_schema import EmployeeCreate, EmployeeUpdate
from typing import List
from routers.auth import db_dependency, user_dependency
from common.common import _require_admin


# === PUBLIC / SHARED ===
def get_current_user_employee(db: db_dependency, user: user_dependency) -> Employee:
    employee = db.query(Employee).filter(Employee.employee_id == user["id"]).first()
    if not employee:
        raise HTTPException(
            status_code=404, detail="Employee profile not found"
        )  # pragma: no cover
    return employee


# === ADMIN ONLY ===
def get_all_employees(db: db_dependency, user: user_dependency) -> List[Employee]:
    if not user.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required"
        )
    return db.query(Employee).all()


def get_employee_by_id(
    employee_id: int, db: db_dependency, user: user_dependency
) -> Employee:
    _require_admin(user)
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


def get_employee_by_email(
    email: str, db: db_dependency, user: user_dependency
) -> Employee:
    _require_admin(user)
    employee = db.query(Employee).filter(Employee.email == email).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


def create_employee(
    employee_data: EmployeeCreate, db: db_dependency, user: user_dependency
) -> Employee:
    _require_admin(user)

    if db.query(Employee).filter(Employee.email == employee_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee with this email already exists",
        )

    new_employee = Employee(**employee_data.model_dump())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


def update_employee_by_id(
    employee_id: int,
    update_data: EmployeeUpdate,
    db: db_dependency,
    user: user_dependency,
) -> Employee:
    _require_admin(user)
    employee = _get_employee_or_404(db, employee_id)

    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)
    return employee


def update_employee_by_email(
    email: str, update_data: EmployeeUpdate, db: db_dependency, user: user_dependency
) -> Employee:
    _require_admin(user)
    employee = db.query(Employee).filter(Employee.email == email).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)
    return employee


def delete_employee_by_id(
    employee_id: int, db: db_dependency, user: user_dependency
) -> dict:
    _require_admin(user)
    employee = _get_employee_or_404(db, employee_id)
    db.delete(employee)
    db.commit()
    return {"detail": "Employee deleted successfully"}


def delete_employee_by_email(
    email: str, db: db_dependency, user: user_dependency
) -> dict:
    _require_admin(user)
    employee = db.query(Employee).filter(Employee.email == email).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return {"detail": "Employee deleted successfully"}


# === MANAGER ONLY ===
def get_subordinate_by_id(
    employee_id: int, db: db_dependency, user: user_dependency
) -> Employee:
    employee = _get_employee_or_404(db, employee_id)
    if employee.fk_manager_id != user["id"]:
        raise HTTPException(
            status_code=404, detail="Employee not found under your management"
        )
    return employee


def get_subordinate_by_email(
    email: str, db: db_dependency, user: user_dependency
) -> Employee:
    employee = db.query(Employee).filter(Employee.email == email).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    if employee.fk_manager_id != user["id"]:
        raise HTTPException(
            status_code=404, detail="Employee not found under your management"
        )
    return employee


# === Helper Functions ===
def _get_employee_or_404(db, employee_id: int) -> Employee:
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
