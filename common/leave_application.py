# common/leave_application.py
from sqlalchemy.orm import Session
from database.models import LeaveApplication, Employee
from schema.leave_application_schema import (
    LeaveApplicationCreate,
    LeaveApplicationStatusUpdate,
    Status,
)
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import List
from sqlalchemy import extract


def _get_leave_app_or_404(db: Session, app_id: int) -> LeaveApplication:
    app = (
        db.query(LeaveApplication)
        .filter(LeaveApplication.leave_application_id == app_id)
        .first()
    )
    if not app:
        raise HTTPException(status_code=404, detail="Leave application not found")
    return app


def create_leave_application(
    db: Session, app_in: LeaveApplicationCreate, user: dict
) -> LeaveApplication:
    emp = db.query(Employee).filter(Employee.employee_id == user["id"]).first()
    if not emp or not emp.fk_manager_id:
        raise HTTPException(status_code=400, detail="No manager assigned")

    total_days = (app_in.end_date.date() - app_in.from_date.date()).days + 1

    app = LeaveApplication(
        **app_in.model_dump(),
        total_days=total_days,
        fk_employee_id=user["id"],
        fk_manager_id=emp.fk_manager_id,
        leave_status=Status.Pending
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


def delete_leave_application(db: Session, app_id: int, user: dict) -> None:
    app = _get_leave_app_or_404(db, app_id)
    if app.fk_employee_id != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    if app.leave_status != Status.Pending:
        raise HTTPException(
            status_code=400, detail="Cannot delete approved/rejected leave"
        )
    db.delete(app)
    db.commit()


def get_my_applications_by_status(
    db: Session, user: dict, status: Status
) -> List[LeaveApplication]:
    return (
        db.query(LeaveApplication)
        .filter(
            LeaveApplication.fk_employee_id == user["id"],
            LeaveApplication.leave_status == status,
        )
        .order_by(LeaveApplication.from_date.desc())
        .all()
    )


def get_my_application_by_id(db: Session, app_id: int, user: dict) -> LeaveApplication:
    app = _get_leave_app_or_404(db, app_id)
    if app.fk_employee_id != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return app


def get_my_applications_by_month(
    db: Session, year: int, month: int, user: dict
) -> List[LeaveApplication]:
    return (
        db.query(LeaveApplication)
        .filter(
            LeaveApplication.fk_employee_id == user["id"],
            extract("year", LeaveApplication.from_date) == year,
            extract("month", LeaveApplication.from_date) == month,
        )
        .order_by(LeaveApplication.from_date)
        .all()
    )


# Admin
def get_application_by_id_admin(db: Session, app_id: int) -> LeaveApplication:
    return _get_leave_app_or_404(db, app_id)


def get_all_by_employee_admin(db: Session, emp_id: int) -> List[LeaveApplication]:
    apps = (
        db.query(LeaveApplication)
        .filter(LeaveApplication.fk_employee_id == emp_id)
        .order_by(LeaveApplication.from_date.desc())
        .all()
    )
    if not apps:
        raise HTTPException(status_code=404, detail="No leave applications found")
    return apps


def get_all_by_month_admin(
    db: Session, year: int, month: int
) -> List[LeaveApplication]:
    apps = (
        db.query(LeaveApplication)
        .filter(
            extract("year", LeaveApplication.from_date) == year,
            extract("month", LeaveApplication.from_date) == month,
        )
        .all()
    )
    if not apps:
        raise HTTPException(status_code=404, detail="No applications in this month")
    return apps


def admin_update_status(
    db: Session, app_id: int, update: LeaveApplicationStatusUpdate
) -> LeaveApplication:
    app = _get_leave_app_or_404(db, app_id)
    app.leave_status = update.leave_status
    app.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(app)
    return app


# Manager
def get_manager_application_by_id(
    db: Session, app_id: int, user: dict
) -> LeaveApplication:
    app = _get_leave_app_or_404(db, app_id)
    if app.fk_manager_id != user["id"]:
        raise HTTPException(
            status_code=403, detail="Leave Application not found under your management"
        )
    return app


def get_manager_applications_by_status(
    db: Session, status: Status, user: dict
) -> List[LeaveApplication]:
    return (
        db.query(LeaveApplication)
        .filter(
            LeaveApplication.fk_manager_id == user["id"],
            LeaveApplication.leave_status == status,
        )
        .order_by(LeaveApplication.from_date)
        .all()
    )


def get_manager_applications_by_month(
    db: Session, year: int, month: int, user: dict
) -> List[LeaveApplication]:
    return (
        db.query(LeaveApplication)
        .filter(
            LeaveApplication.fk_manager_id == user["id"],
            extract("year", LeaveApplication.from_date) == year,
            extract("month", LeaveApplication.from_date) == month,
        )
        .all()
    )


def get_manager_applications_by_employee(
    db: Session, emp_id: int, user: dict
) -> List[LeaveApplication]:
    from common.employee import get_subordinate_by_id

    get_subordinate_by_id(employee_id=emp_id, db=db, user=user)
    return (
        db.query(LeaveApplication)
        .filter(LeaveApplication.fk_employee_id == emp_id)
        .order_by(LeaveApplication.from_date.desc())
        .all()
    )


def manager_update_status(
    db: Session, app_id: int, update: LeaveApplicationStatusUpdate, user: dict
) -> LeaveApplication:
    app = get_manager_application_by_id(db, app_id, user)
    app.leave_status = update.leave_status
    app.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(app)
    return app
