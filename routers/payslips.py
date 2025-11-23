from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from routers.auth import db_dependency, user_dependency
from database.models import Payslip, Employee

router = APIRouter(prefix="/payslips", tags=["Payslips"])


# Pydantic schemas
class PayslipCreate(BaseModel):
    basic_amount: float
    hra: Optional[float] = None
    special_allowance: Optional[float] = None
    internet_allowance: Optional[float] = None
    payslip_month: datetime
    fk_employee_id: int


class PayslipUpdate(BaseModel):
    basic_amount: Optional[float] = None
    hra: Optional[float] = None
    special_allowance: Optional[float] = None
    internet_allowance: Optional[float] = None
    payslip_month: Optional[datetime] = None

    class Config:
        from_attributes = True


class PayslipResponse(BaseModel):
    payslip_id: int
    basic_amount: float
    hra: Optional[float]
    special_allowance: Optional[float]
    internet_allowance: Optional[float]
    payslip_month: datetime
    fk_employee_id: int

    class Config:
        from_attributes = True


# === CREATE (Admin only) ===
@router.post("/", response_model=PayslipResponse, status_code=status.HTTP_201_CREATED)
def create_payslip(payslip: PayslipCreate, db: db_dependency, user: user_dependency):
    if not user.get('is_admin'):
        raise HTTPException(status_code=403, detail="Only administrators can create payslips.")

    employee = db.query(Employee).filter(Employee.employee_id == payslip.fk_employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    existing = db.query(Payslip).filter(
        Payslip.fk_employee_id == payslip.fk_employee_id,
        Payslip.payslip_month == payslip.payslip_month
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Payslip already exists for this month")

    new_payslip = Payslip(**payslip.model_dump())
    db.add(new_payslip)
    db.commit()
    db.refresh(new_payslip)
    return new_payslip


# === GET MY PAYSLIPS ===
@router.get("/", response_model=list[PayslipResponse])
def get_my_payslips(db: db_dependency, user: user_dependency):
    employee_id = user.get('employee_id') or user.get('id')  # flexible key
    if not employee_id:
        raise HTTPException(status_code=400, detail="Employee ID not found in user context")

    payslips = db.query(Payslip).filter(Payslip.fk_employee_id == employee_id).all()
    return payslips


# === GET SINGLE PAYSLIP (Owner or Admin) ===
@router.get("/{payslip_id}", response_model=PayslipResponse)
def get_payslip(payslip_id: int, db: db_dependency, user: user_dependency):
    if not user.get('is_admin'):
        payslip = db.query(Payslip).filter(Payslip.payslip_id == payslip_id,Payslip.fk_employee_id == user['id']).first()
    else:
        payslip = db.query(Payslip).filter(Payslip.payslip_id == payslip_id).first()
    if not payslip:
        raise HTTPException(status_code=404, detail="Payslip not found")

    employee_id = user.get('employee_id') or user.get('id')
    if user.get('is_admin') or payslip.fk_employee_id == employee_id:
        return payslip

    raise HTTPException(status_code=403, detail="Not authorized to view this payslip")


# === UPDATE PAYSLIP (Admin only) ===
@router.put("/{payslip_id}", response_model=PayslipResponse)
def update_payslip(
    payslip_id: int,
    update_data: PayslipUpdate,
    db: db_dependency,
    user: user_dependency
):
    if not user.get('is_admin'):
        raise HTTPException(status_code=403, detail="Only administrators can update payslips.")

    payslip = db.query(Payslip).filter(Payslip.payslip_id == payslip_id).first()
    if not payslip:
        raise HTTPException(status_code=404, detail="Payslip not found")

    # Update only provided fields
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(payslip, key, value)

    db.commit()
    db.refresh(payslip)
    return payslip


# === DELETE PAYSLIP (Admin only) ===
@router.delete("/{payslip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payslip(
    payslip_id: int,
    db: db_dependency,
    user: user_dependency
):
    if not user.get('is_admin'):
        raise HTTPException(status_code=403, detail="Only admins can delete payslips.")

    payslip = db.query(Payslip).filter(Payslip.payslip_id == payslip_id).first()
    if not payslip:
        raise HTTPException(status_code=404, detail="Payslip not found")

    db.delete(payslip)
    db.commit()
    return None  # 204 returns no content