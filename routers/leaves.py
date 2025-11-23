# routers/leave.py
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from routers.auth import db_dependency, user_dependency
from database.models import Leave, Employee

router = APIRouter(prefix="/leaves", tags=["Leaves"])


# ==============================
# Pydantic Schemas
# ==============================
class LeaveBase(BaseModel):
    assign_year: int
    casual_leave: Optional[int] = None
    plan_leave: Optional[int] = None
    probation_leave: Optional[int] = None
    sick_leave: Optional[int] = None
    total_leave: Optional[int] = None
    balance_leave: Optional[int] = None


class LeaveCreate(LeaveBase):
    fk_employee_id: int


class LeaveUpdate(LeaveBase):
    pass


class LeaveResponse(LeaveBase):
    leave_id: int
    fk_employee_id: int
    total_leave: int
    balance_leave: int

    class Config:
        from_attributes = True


# ==============================
# Helper: Compute total_leave automatically (recommended)
# ==============================
def calculate_total_leave(data: dict) -> int:
    return (
        (data.get("casual_leave") or 0) +
        (data.get("plan_leave") or 0) +
        (data.get("probation_leave") or 0) +
        (data.get("sick_leave") or 0)
    )


# ==============================
# CREATE Leave Balance (Admin Only)
# ==============================
@router.post("/", response_model=LeaveResponse, status_code=status.HTTP_201_CREATED)
def create_leave_balance(
    leave_data: LeaveCreate,
    db: db_dependency,
    user: user_dependency
):
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Only admins can create leave records")

    # Check if employee exists
    employee = db.query(Employee).filter(Employee.employee_id == leave_data.fk_employee_id, Employee.le).first() 
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Prevent duplicate for same employee + year
    existing = db.query(Leave).filter(
        Leave.fk_employee_id == leave_data.fk_employee_id,
        Leave.assign_year == leave_data.assign_year
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Leave record already exists for year {leave_data.assign_year}")

    # Auto-calculate total_leave if not provided
    leave_dict = leave_data.model_dump()
    leave_dict["total_leave"] = calculate_total_leave(leave_dict)
    leave_dict["balance_leave"] = leave_dict["total_leave"]

    new_leave = Leave(**leave_dict)
    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)
    return new_leave


# ==============================
# GET My Leave Balance (Employee + Admin)
# ==============================
@router.get("/me", response_model=List[LeaveResponse])
def get_my_leaves(
    db: db_dependency,
    user: user_dependency,
    year: Optional[int] = None
):
    employee_id = user.get("employee_id") or user.get("id")
    if not employee_id:
        raise HTTPException(status_code=400, detail="Employee ID not found in token")

    query = db.query(Leave).filter(Leave.fk_employee_id == employee_id)
    if year:
        query = query.filter(Leave.assign_year == year)

    leaves = query.order_by(Leave.assign_year.desc()).all()
    return leaves


# ==============================
# GET All Leaves (Admin Only) - Optional
# ==============================
@router.get("/", response_model=List[LeaveResponse])
def get_all_leaves(
    db: db_dependency,
    user: user_dependency,
    skip: int = 0,
    limit: int = 50
):
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Only admins can view all leave records")

    leaves = db.query(Leave).offset(skip).limit(limit).all()
    return leaves


# ==============================
# UPDATE Leave Balance (Admin Only)
# ==============================
@router.put("/{leave_id}", response_model=LeaveResponse)
def update_leave_balance(
    leave_id: int,
    update_data: LeaveUpdate,
    db: db_dependency,
    user: user_dependency
):
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Only admins can update leave records")

    leave = db.query(Leave).filter(Leave.leave_id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave record not found")

    update_dict = update_data.model_dump(exclude_unset=True)

    # Recalculate total_leave if any leave type is updated
    if any(key in update_dict for key in ["casual_leave", "plan_leave", "probation_leave", "sick_leave"]):
        base = {
            "casual_leave": leave.casual_leave,
            "plan_leave": leave.plan_leave,
            "probation_leave": leave.probation_leave,
            "sick_leave": leave.sick_leave,
        }
        base.update({k: v for k, v in update_dict.items() if k in base})
        update_dict["total_leave"] = calculate_total_leave(base)

    # Update fields
    for key, value in update_dict.items():
        setattr(leave, key, value)

    db.commit()
    db.refresh(leave)
    return leave


# ==============================
# DELETE Leave Record (Admin Only)
# ==============================
@router.delete("/{leave_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leave_balance(
    leave_id: int,
    db: db_dependency,
    user: user_dependency
):
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Only admins can delete leave records")

    leave = db.query(Leave).filter(Leave.leave_id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave record not found")

    db.delete(leave)
    db.commit()
    return None