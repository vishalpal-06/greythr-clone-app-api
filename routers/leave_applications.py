from typing import List, Optional
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from enum import Enum as PyEnum

from routers.auth import db_dependency, user_dependency
from database.models import LeaveApplication, Employee, Leave
from database.models import Status  # assuming you have enum Status in models

router = APIRouter(prefix="/leave-applications", tags=["Leave Applications"])


# ==============================
# Pydantic Schemas
# ==============================
class LeaveApplicationCreate(BaseModel):
    from_date: date  # Use date, not datetime
    end_date: date
    leave_reason: str


class LeaveApplicationUpdate(BaseModel):
    from_date: Optional[date] = None
    end_date: Optional[date] = None
    leave_reason: Optional[str] = None


class LeaveApplicationResponse(BaseModel):
    leave_application_id: int
    from_date: date
    end_date: date
    total_days: int
    leave_status: Status
    leave_reason: str
    fk_employee_id: int
    fk_manager_id: Optional[int]

    class Config:
        from_attributes = True


class LeaveApplicationApprove(BaseModel):
    action: str  # "approve" or "reject"


# Helper: Calculate total leave days (excluding weekends? optional)
def calculate_leave_days(from_date: date, end_date: date) -> int:
    if from_date > end_date:
        raise ValueError("from_date cannot be after end_date")
    return (end_date - from_date).days + 1  # inclusive


# ==============================
# CREATE Leave Application (Employee only)
# ==============================
@router.post("/", response_model=LeaveApplicationResponse, status_code=201)
def apply_for_leave(
    application: LeaveApplicationCreate,
    db: db_dependency,
    user: user_dependency
):
    employee_id = user.get("employee_id") or user.get("id")
    if not employee_id:
        raise HTTPException(status_code=400, detail="Employee ID not found")

    if application.from_date < date.today():
        raise HTTPException(status_code=400, detail="Cannot apply leave for past dates")

    if application.end_date < application.from_date:
        raise HTTPException(status_code=400, detail="End date cannot be before start date")

    total_days = calculate_leave_days(application.from_date, application.end_date)

    # Optional: Check available balance (uncomment if needed)
    year = application.from_date.year
    leave_balance = db.query(Leave).filter(
        Leave.fk_employee_id == employee_id,
        Leave.assign_year == year
    ).first()
    if leave_balance and leave_balance.balance_leave < total_days:
        raise HTTPException(status_code=400, detail="Insufficient leave balance")

    new_app = LeaveApplication(
        from_date=application.from_date,
        end_date=application.end_date,
        total_days=total_days,
        leave_status=Status.Pending,
        leave_reason=application.leave_reason,
        fk_employee_id=employee_id,
        # fk_manager_id will be set by HR or auto-assigned
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)

    # Optional: Auto-assign manager (if employee has reporting manager)
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if employee and employee.fk_manager_id:
        new_app.fk_manager_id = employee.fk_manager_id
        db.commit()
        db.refresh(new_app)

    return new_app


# ==============================
# GET My Leave Applications
# ==============================
@router.get("/me", response_model=List[LeaveApplicationResponse])
def get_my_applications(
    db: db_dependency,
    user: user_dependency,
    status_filter: Optional[Status] = None
):
    employee_id = user.get("employee_id") or user.get("id")

    query = db.query(LeaveApplication).filter(LeaveApplication.fk_employee_id == employee_id)
    if status_filter:
        query = query.filter(LeaveApplication.leave_status == status_filter)

    applications = query.order_by(LeaveApplication.from_date.desc()).all()
    return applications


# ====================================================
# GET Applications to Approve (For Manager)
# ====================================================
@router.get("/to-approve", response_model=List[LeaveApplicationResponse])
def get_applications_to_approve(
    db: db_dependency,
    user: user_dependency
):
    manager_id = user.get("employee_id") or user.get("id")
    if not manager_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    applications = (
        db.query(LeaveApplication)
        .join(Employee, Employee.employee_id == LeaveApplication.fk_employee_id)
        .filter(LeaveApplication.fk_manager_id == manager_id)
        .filter(LeaveApplication.leave_status == Status.Pending)
        .all()
    )

    # Add employee name for convenience
    result = []
    for app in applications:
        data = LeaveApplicationResponse.from_orm(app)
        data.employee_name = app.employee.full_name if app.employee else "Unknown"
        result.append(data)

    return result


# ====================================================
# APPROVE / REJECT (Manager or Admin)
# ====================================================
@router.put("/{app_id}/review", response_model=LeaveApplicationResponse)
def review_leave_application(
    app_id: int,
    review: LeaveApplicationApprove,
    db: db_dependency,
    user: user_dependency
):
    is_admin = user.get("is_admin")
    manager_id = user.get("employee_id") or user.get("id")

    application = db.query(LeaveApplication).filter(LeaveApplication.leave_application_id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if application.leave_status != Status.Pending:
        raise HTTPException(status_code=400, detail="This application has already been processed")

    # Authorization: Manager or Admin
    if not (is_admin or application.fk_manager_id == manager_id):
        raise HTTPException(status_code=403, detail="Not authorized to review this application")

    if review.action not in ["approve", "reject"]:
        raise HTTPException(status_code=400, detail="Action must be 'approve' or 'reject'")

    new_status = Status.Approved if review.action == "approve" else Status.Rejected
    application.leave_status = new_status

    db.commit()
    db.refresh(application)
    return application


# ====================================================
# GET Single Application (Owner/Manager/Admin)
# ====================================================
@router.get("/{app_id}", response_model=LeaveApplicationResponse)
def get_application(
    app_id: int,
    db: db_dependency,
    user: user_dependency
):
    app = db.query(LeaveApplication).filter(LeaveApplication.leave_application_id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Not found")

    user_id = user.get("employee_id") or user.get("id")
    is_admin = user.get("is_admin")

    if is_admin or app.fk_employee_id == user_id or app.fk_manager_id == user_id:
        data = LeaveApplicationResponse.from_orm(app)
        data.employee_name = app.employee.full_name if app.employee else None
        return data

    raise HTTPException(status_code=403, detail="Not authorized")


# ==============================
# (Optional) Cancel Application (Employee only, if Pending)
# ==============================
@router.delete("/{app_id}", status_code=204)
def cancel_application(
    app_id: int,
    db: db_dependency,
    user: user_dependency
):
    app = db.query(LeaveApplication).filter(LeaveApplication.leave_application_id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Not found")

    if app.fk_employee_id != (user.get("employee_id") or user.get("id")):
        raise HTTPException(status_code=403, detail="Can only cancel your own application")

    if app.leave_status != Status.Pending:
        raise HTTPException(status_code=400, detail="Cannot cancel approved/rejected leave")

    db.delete(app)
    db.commit()
    return None