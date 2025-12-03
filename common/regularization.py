# common/regularization.py
from sqlalchemy.orm import Session
from database.models import Regularization, Employee
from schema.regularization_schema import (
    RegularizationCreate,
    RegularizationStatusUpdate,
    Status,
)
from fastapi import HTTPException, status
from datetime import datetime
from typing import List
from sqlalchemy import extract


def _get_regularization_or_404(db: Session, reg_id: int) -> Regularization:
    reg = (
        db.query(Regularization)
        .filter(Regularization.regularization_id == reg_id)
        .first()
    )
    if not reg:
        raise HTTPException(status_code=404, detail="Regularization request not found")
    return reg


# ─── USER ───
def create_regularization(
    db: Session, reg_in: RegularizationCreate, user: dict
) -> Regularization:
    emp = db.query(Employee).filter(Employee.employee_id == user["id"]).first()
    if not emp or not emp.fk_manager_id:
        raise HTTPException(status_code=400, detail="You have no manager assigned")

    reg = Regularization(
        **reg_in.model_dump(),
        fk_employee_id=user["id"],
        fk_manager_id=emp.fk_manager_id,
        regularization_status=Status.Pending
    )
    db.add(reg)
    db.commit()
    db.refresh(reg)
    return reg


def get_my_regularizations(db: Session, user: dict) -> List[Regularization]:
    return (
        db.query(Regularization)
        .filter(Regularization.fk_employee_id == user["id"])
        .order_by(Regularization.regularization_start_time.desc())
        .all()
    )


def get_my_regularization_by_id(reg_id: int, db: Session, user: dict) -> Regularization:
    reg = _get_regularization_or_404(db, reg_id)
    if reg.fk_employee_id != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return reg


def get_my_regularizations_by_month(
    year: int, month: int, db: Session, user: dict
) -> List[Regularization]:
    return (
        db.query(Regularization)
        .filter(
            Regularization.fk_employee_id == user["id"],
            extract("year", Regularization.regularization_start_time) == year,
            extract("month", Regularization.regularization_start_time) == month,
        )
        .order_by(Regularization.regularization_start_time)
        .all()
    )


# ─── ADMIN ───
def get_regularization_by_id_admin(reg_id: int, db: Session) -> Regularization:
    return _get_regularization_or_404(db, reg_id)


def admin_update_status(
    reg_id: int, status_update: RegularizationStatusUpdate, db: Session
) -> Regularization:
    reg = _get_regularization_or_404(db, reg_id)
    reg.regularization_status = status_update.regularization_status
    reg.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(reg)
    return reg


# ─── MANAGER ───
def get_manager_regularization_by_id(
    reg_id: int, db: Session, user: dict
) -> Regularization:
    reg = _get_regularization_or_404(db, reg_id)
    if reg.fk_manager_id != user["id"]:
        raise HTTPException(
            status_code=403, detail="Regularization not found under your management"
        )
    return reg


def get_manager_regularizations_for_employee(
    employee_id: int, db: Session, user: dict
) -> List[Regularization]:
    from common.employee import get_subordinate_by_id

    get_subordinate_by_id(employee_id=employee_id, db=db, user=user)
    return (
        db.query(Regularization)
        .filter(Regularization.fk_employee_id == employee_id)
        .order_by(Regularization.regularization_start_time.desc())
        .all()
    )


def get_manager_pending_regularizations(
    db: Session, user: dict
) -> List[Regularization]:
    return (
        db.query(Regularization)
        .filter(
            Regularization.fk_manager_id == user["id"],
            Regularization.regularization_status == Status.Pending,
        )
        .order_by(Regularization.regularization_start_time)
        .all()
    )


def manager_update_regularization_status(
    reg_id: int, status_update: RegularizationStatusUpdate, db: Session, user: dict
) -> Regularization:
    reg = get_manager_regularization_by_id(reg_id, db=db, user=user)
    reg.regularization_status = status_update.regularization_status
    reg.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(reg)
    return reg
