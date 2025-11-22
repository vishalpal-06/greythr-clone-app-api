# routers/expense_claim.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.models import ExpenseClaim, Employee
# schemas/expense_claim.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from routers.auth import db_dependency, user_dependency

router = APIRouter(prefix="/expense-claims", tags=["Expense Claims"])


class ExpenseClaimBase(BaseModel):
    claim_date: datetime
    amount: float
    description: str
    claim_status: str

class ExpenseClaimCreate(ExpenseClaimBase):
    pass

class ExpenseClaimUpdate(BaseModel):
    claim_status: str

class ExpenseClaimResponse(ExpenseClaimBase):
    claim_id: int
    fk_employee_id: int
    fk_manager_id: int

    class Config:
        from_attribute: True
    

@router.post("create_expense/", response_model=ExpenseClaimResponse, status_code=status.HTTP_201_CREATED)
def create_expense_claim(
    claim: ExpenseClaimCreate,
    db: db_dependency,
    user: user_dependency
):
    if claim.claim_status not in ['Pending','Approved','Rejected']:
        raise HTTPException(status_code=422,detail="invalid claim status")
    employee_details = db.query(Employee).filter(Employee.employee_id == user['id']).first()

    new_claim = ExpenseClaim(
        claim_date=claim.claim_date,
        amount=claim.amount,
        description=claim.description,
        claim_status=claim.claim_status,
        fk_employee_id=employee_details.employee_id,
        fk_manager_id=employee_details.fk_manager_id
    )

    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)
    return new_claim


@router.delete("delete_expense/", status_code=status.HTTP_200_OK)
def create_expense_claim(
    claim_id: int,
    db: db_dependency,
    user: user_dependency
):
    
    claim = db.query(ExpenseClaim).filter(ExpenseClaim.fk_employee_id == user['id'], ExpenseClaim.claim_id == claim_id).first()

    if not claim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The claim does not exist or you do not have permission to access it.")

    db.delete(claim)
    db.commit()
    db.refresh(claim)
    return "All Good"


#Update expense status
@router.put("/update_expense_status/{expense_id}")
def update_expense_status(expense_id: int, expense_form: ExpenseClaimUpdate, db: db_dependency, user : user_dependency):
    expense_record = db.query(ExpenseClaim).filter(ExpenseClaim.claim_id == expense_id).first()
    if not expense_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ExpenseClaim record not found")
    if expense_record.fk_manager_id == user['id']:
        expense_record.expense_status = expense_form.claim_status
        db.commit()
        db.refresh(expense_record)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")
    return {"message": "ExpenseClaim status updated successfully", "data": expense_record}


@router.get("/get_all_expense", response_model=List[ExpenseClaimResponse])
def get_all_expense(db: db_dependency, user : user_dependency):
    expense_record = db.query(ExpenseClaim).filter(ExpenseClaim.fk_employee_id == user['id']).all()
    return expense_record


@router.get("/get_all_expense_manager", response_model=List[ExpenseClaimResponse])
def get_all_expense(db: db_dependency, user : user_dependency):
    expense_record = db.query(ExpenseClaim).filter(ExpenseClaim.fk_manager_id == user['id']).all()
    return expense_record




