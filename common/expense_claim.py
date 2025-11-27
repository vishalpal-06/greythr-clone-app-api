# common/expense_claim.py
from sqlalchemy.orm import Session
from database.models import ExpenseClaim, Employee
from schema.expense_claim_schema import ExpenseClaimCreate, ExpenseClaimStatusUpdate, Status
from fastapi import HTTPException, status
from datetime import datetime
from typing import List
from sqlalchemy import extract


def _get_claim_or_404(db: Session, claim_id: int) -> ExpenseClaim:
    claim = db.query(ExpenseClaim).filter(ExpenseClaim.claim_id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Expense claim not found")
    return claim


# USER
def create_expense_claim(db: Session, claim_in: ExpenseClaimCreate, user: dict) -> ExpenseClaim:
    emp = db.query(Employee).filter(Employee.employee_id == user["id"]).first()
    if not emp or not emp.fk_manager_id:
        raise HTTPException(status_code=400, detail="No manager assigned")

    claim = ExpenseClaim(
        **claim_in.model_dump(),
        fk_employee_id=user["id"],
        fk_manager_id=emp.fk_manager_id,
        claim_status=Status.Pending
    )
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return claim


def delete_expense_claim(db: Session, claim_id: int, user: dict) -> None:
    claim = _get_claim_or_404(db, claim_id)
    if claim.fk_employee_id != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    if claim.claim_status != Status.Pending:
        raise HTTPException(status_code=400, detail="Cannot delete approved/rejected claim")
    db.delete(claim)
    db.commit()


def get_my_claims_by_status(db: Session, status: Status, user: dict) -> List[ExpenseClaim]:
    return db.query(ExpenseClaim)\
           .filter(ExpenseClaim.fk_employee_id == user["id"],
                   ExpenseClaim.claim_status == status)\
           .order_by(ExpenseClaim.claim_date.desc())\
           .all()


def get_my_claim_by_id(db: Session, claim_id: int, user: dict) -> ExpenseClaim:
    claim = _get_claim_or_404(db, claim_id)
    if claim.fk_employee_id != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return claim


def get_my_claims_by_month(db: Session, year: int, month: int, user: dict) -> List[ExpenseClaim]:
    return db.query(ExpenseClaim)\
           .filter(
               ExpenseClaim.fk_employee_id == user["id"],
               extract('year', ExpenseClaim.claim_date) == year,
               extract('month', ExpenseClaim.claim_date) == month
           )\
           .order_by(ExpenseClaim.claim_date.desc())\
           .all()


# ADMIN
def get_claim_by_id_admin(db: Session, claim_id: int) -> ExpenseClaim:
    return _get_claim_or_404(db, claim_id)


def get_all_claims_by_employee_admin(db: Session, emp_id: int) -> List[ExpenseClaim]:
    claims = db.query(ExpenseClaim)\
           .filter(ExpenseClaim.fk_employee_id == emp_id)\
           .order_by(ExpenseClaim.claim_date.desc())\
           .all()
    if not claims:
        raise HTTPException(status_code=404, detail="No claims found")
    return claims


def get_claims_by_status_admin(db: Session, status: Status) -> List[ExpenseClaim]:
    claims = db.query(ExpenseClaim).filter(ExpenseClaim.claim_status == status).all()
    if not claims:
        raise HTTPException(status_code=404, detail=f"No {status.value} claims")
    return claims


def get_claims_by_month_admin(db: Session, year: int, month: int) -> List[ExpenseClaim]:
    claims = db.query(ExpenseClaim)\
           .filter(
               extract('year', ExpenseClaim.claim_date) == year,
               extract('month', ExpenseClaim.claim_date) == month
           ).all()
    if not claims:
        raise HTTPException(status_code=404, detail="No claims in this month")
    return claims


def get_claims_by_employee_and_month_any(db: Session, emp_id: int, year: int, month: int) -> List[ExpenseClaim]:
    from sqlalchemy import extract
    claims = db.query(ExpenseClaim)\
           .filter(
               ExpenseClaim.fk_employee_id == emp_id,
               extract('year', ExpenseClaim.claim_date) == year,
               extract('month', ExpenseClaim.claim_date) == month
           )\
           .order_by(ExpenseClaim.claim_date.desc())\
           .all()
    if not claims:
        raise HTTPException(status_code=404, detail="No expense claims found for this employee and month")
    return claims


def admin_update_status(db: Session, claim_id: int, update: ExpenseClaimStatusUpdate) -> ExpenseClaim:
    claim = _get_claim_or_404(db, claim_id)
    claim.claim_status = update.claim_status
    claim.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(claim)
    return claim


# MANAGER
def get_manager_claim_by_id(db: Session, claim_id: int, user: dict) -> ExpenseClaim:
    claim = _get_claim_or_404(db, claim_id)
    if claim.fk_manager_id != user["id"]:
        raise HTTPException(status_code=403, detail="Expense Application not found under your management")
    return claim


def get_manager_claims_by_status(db: Session, status: Status, user: dict) -> List[ExpenseClaim]:
    return db.query(ExpenseClaim)\
           .filter(ExpenseClaim.fk_manager_id == user["id"],
                   ExpenseClaim.claim_status == status)\
           .order_by(ExpenseClaim.claim_date.desc())\
           .all()


def get_manager_claims_by_month(db: Session, year: int, month: int, user: dict) -> List[ExpenseClaim]:
    return db.query(ExpenseClaim)\
           .filter(
               ExpenseClaim.fk_manager_id == user["id"],
               extract('year', ExpenseClaim.claim_date) == year,
               extract('month', ExpenseClaim.claim_date) == month
           )\
           .order_by(ExpenseClaim.claim_date.desc())\
           .all()


def get_manager_claims_by_employee_and_month(db: Session, emp_id: int, year: int, month: int, user: dict) -> List[ExpenseClaim]:
    from common.employee import get_subordinate_by_id
    get_subordinate_by_id(employee_id=emp_id, db=db, user=user)
    return db.query(ExpenseClaim)\
           .filter(
               ExpenseClaim.fk_employee_id == emp_id,
               extract('year', ExpenseClaim.claim_date) == year,
               extract('month', ExpenseClaim.claim_date) == month
           )\
           .order_by(ExpenseClaim.claim_date.desc())\
           .all()


def manager_update_status(db: Session, claim_id: int, update: ExpenseClaimStatusUpdate, user: dict) -> ExpenseClaim:
    claim = get_manager_claim_by_id(db, claim_id, user)
    claim.claim_status = update.claim_status
    claim.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(claim)
    return claim