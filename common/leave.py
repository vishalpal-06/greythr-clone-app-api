# common/leave.py
from sqlalchemy.orm import Session
from database.models import Leave, Employee
from schema.leave_schema import LeaveCreate
from typing import List
from fastapi import HTTPException, status


def _get_leave_or_404(db: Session, employee_id: int, year: int) -> Leave:
    leave = db.query(Leave).filter(
        Leave.fk_employee_id == employee_id,
        Leave.assign_year == year
    ).first()
    if not leave:
        raise HTTPException(
            status_code=404,
            detail=f"Leave record not found for employee {employee_id} in year {year}"
        )
    return leave


def get_leave_by_employee_and_year(db: Session, employee_id: int, year: int) -> Leave:
    return _get_leave_or_404(db, employee_id, year)


def get_all_leaves_by_employee_id(db: Session, employee_id: int) -> List[Leave]:
    leaves = db.query(Leave).filter(Leave.fk_employee_id == employee_id).order_by(Leave.assign_year).all()
    if not leaves:
        raise HTTPException(status_code=404, detail=f"No leave records found for employee {employee_id}")
    return leaves


def get_leave_years_by_employee(db: Session, employee_id: int) -> List[int]:
    years = [row[0] for row in db.query(Leave.assign_year)
             .filter(Leave.fk_employee_id == employee_id)
             .distinct()
             .order_by(Leave.assign_year)
             .all()]
    if not years:
        raise HTTPException(status_code=404, detail=f"No leave records found for employee {employee_id}")
    return years


def create_leave(db: Session, leave_in: LeaveCreate) -> Leave:
    # Prevent duplicate year per employee
    exists = db.query(Leave).filter(
        Leave.fk_employee_id == leave_in.fk_employee_id,
        Leave.assign_year == leave_in.assign_year
    ).first()
    if exists:
        raise HTTPException(
            status_code=409,
            detail=f"Leave record already exists for employee {leave_in.fk_employee_id} in year {leave_in.assign_year}"
        )

    db_leave = Leave(**leave_in.model_dump())
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave


def delete_leave(db: Session, leave_id: int) -> None:
    leave = db.query(Leave).filter(Leave.leave_id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail=f"Leave record with ID {leave_id} not found")
    db.delete(leave)
    db.commit()


def delete_leave_by_employee_and_year(db: Session, employee_id: int, year: int) -> None:
    leave = _get_leave_or_404(db, employee_id, year)
    db.delete(leave)
    db.commit()