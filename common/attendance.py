# common/attendance.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import cast, Date, func
from database.models import Attendance, Employee
from schema.attendance_schema import AttendanceCreate
from typing import List, Dict
from common.common import _require_admin
from datetime import datetime, date, time
from routers.auth import db_dependency, user_dependency


# === Helpers ===
def _get_attendance_or_404(db: Session, attendance_id: int) -> Attendance:
    att = db.query(Attendance).filter(Attendance.attendance_id == attendance_id).first()
    if not att:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return att


# === USER: CREATE ===
def create_attendance(db: Session, punch_time, current_user: dict) -> Attendance:
    new_att = Attendance(
        punch_time=punch_time,
        fk_employee_id=current_user["id"]
    )
    db.add(new_att)
    db.commit()
    return new_att


# === USER: READ OWN ===
def get_my_attendance_all(db: Session, current_user: dict) -> List[Attendance]:
    return db.query(Attendance).filter(Attendance.fk_employee_id == current_user["id"]).all()

    

def get_my_attendance_by_date(
    db: db_dependency,
    user: user_dependency,
    punch_date: date
):
    start_dt = datetime.combine(punch_date, time.min)
    end_dt = datetime.combine(punch_date, time.max)

    return (
        db.query(Attendance)
        .filter(
            Attendance.fk_employee_id == user["id"],
            Attendance.punch_time >= start_dt,
            Attendance.punch_time <= end_dt
        )
        .order_by(Attendance.punch_time)
        .all()
    )




# MANAGER: All direct reports' attendance on a given date
def get_manager_team_attendance_by_date(
    punch_date: date,
    db: Session,
    user: dict,
) -> List[Attendance]:
    # Real check: does ANY employee report to this user?
    has_subordinates = db.query(Employee).filter(
        Employee.fk_manager_id == user["id"]
    ).first()

    if not has_subordinates:
        return []  # No one reports to you → empty list (safe)

    managed_ids = [
        e.employee_id for e in
        db.query(Employee.employee_id)
          .filter(Employee.fk_manager_id == user["id"])
          .all()
    ]

    start_dt = datetime.combine(punch_date, time.min)
    end_dt = datetime.combine(punch_date, time.max)

    return (
        db.query(Attendance)
        .filter(
            Attendance.fk_employee_id.in_(managed_ids),
            Attendance.punch_time.between(start_dt, end_dt)
        )
        .order_by(Attendance.fk_employee_id, Attendance.punch_time)
        .all()
    )


# MANAGER: One specific subordinate's attendance on a date
def get_manager_subordinate_attendance_by_date(
    employee_id: int,
    punch_date: date,
    db: Session,
    user: dict,
) -> List[Attendance]:
    # Security: employee must exist AND report directly to current user
    employee = db.query(Employee).filter(
        Employee.employee_id == employee_id,
        Employee.fk_manager_id == user["id"]
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found under your management"
        )

    start_dt = datetime.combine(punch_date, time.min)
    end_dt = datetime.combine(punch_date, time.max)

    return (
        db.query(Attendance)
        .filter(
            Attendance.fk_employee_id == employee_id,
            Attendance.punch_time.between(start_dt, end_dt)
        )
        .order_by(Attendance.punch_time)
        .all()
    )

# === ADMIN: READ ALL ===
def get_all_attendance(db: Session, user: user_dependency):
    _require_admin(user=user)
    return db.query(Attendance).all()


def get_attendance_by_date_all_employees(db: Session, punch_date: datetime, user: user_dependency):
    _require_admin(user=user)
    start_dt = datetime.combine(punch_date, time.min)
    end_dt = datetime.combine(punch_date, time.max)

    return (
        db.query(Attendance)
        .filter(
            Attendance.punch_time >= start_dt,
            Attendance.punch_time <= end_dt
        )
        .order_by(Attendance.punch_time)
        .all()
    )


def get_attendance_by_date_one_employee(db: Session, employee_id: int, punch_date: datetime, user:user_dependency):
    _require_admin(user=user)
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
    start_dt = datetime.combine(punch_date, time.min)
    end_dt = datetime.combine(punch_date, time.max)

    return (
        db.query(Attendance)
        .filter(
            Attendance.punch_time >= start_dt,
            Attendance.punch_time <= end_dt,
            Attendance.fk_employee_id == employee_id,
        )
        .order_by(Attendance.punch_time)
        .all()
    )


def get_all_attendance_of_employee(db: Session, employee_id: int, user:user_dependency):
    _require_admin(user=user)
    employee = db.query(Employee).filter(Employee.employee_id==employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee Not Founds")
    if user['is_admin'] or employee.fk_manager_id == user['is_admin']:
        records = db.query(Attendance).filter(Attendance.fk_employee_id == employee_id).all()
        return records
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you can not perform this action")



