# api/admin_expense_claim_api.py
from fastapi import APIRouter
from typing import List
from schema.expense_claim_schema import ExpenseClaimResponse, ExpenseClaimStatusUpdate, Status
from routers.auth import db_dependency, user_dependency
from common.common import _require_admin
from common.expense_claim import (
    get_claim_by_id_admin, get_all_claims_by_employee_admin,
    get_claims_by_status_admin, get_claims_by_month_admin,
    admin_update_status, get_claims_by_employee_and_month_any
)

router = APIRouter(prefix="/admin/expense-claims", tags=["Admin - Expense Claims"])


@router.get("/{claim_id}", response_model=ExpenseClaimResponse)
def get_exp_by_id(claim_id: int, db: db_dependency, user: user_dependency):
    _require_admin(user)
    return get_claim_by_id_admin(db=db, claim_id=claim_id)


@router.get("/employee/{emp_id}", response_model=List[ExpenseClaimResponse])
def get_all_exp_by_emp(emp_id: int, db: db_dependency, user: user_dependency):
    _require_admin(user)
    return get_all_claims_by_employee_admin(db=db, emp_id=emp_id)


@router.get("/status/{status}", response_model=List[ExpenseClaimResponse])
def get_exp_by_status(status: Status, db: db_dependency, user: user_dependency):
    _require_admin(user)
    return get_claims_by_status_admin(db=db, status=status)


@router.get("/month/{year}/{month}", response_model=List[ExpenseClaimResponse])
def get_exp_by_month(year: int, month: int, db: db_dependency, user: user_dependency):
    _require_admin(user)
    return get_claims_by_month_admin(db=db, year=year, month=month)


@router.get("/employee/{emp_id}/month/{year}/{month}", response_model=List[ExpenseClaimResponse])
def get_exp_by_employeeid_and_month(emp_id: int, year: int, month: int, db: db_dependency, user: user_dependency):
    _require_admin(user)
    return get_claims_by_employee_and_month_any(db=db, emp_id=emp_id, year=year, month=month)


@router.put("/{claim_id}/status", response_model=ExpenseClaimResponse)
def update_exp_status(claim_id: int, update: ExpenseClaimStatusUpdate, db: db_dependency, user: user_dependency):
    _require_admin(user)
    return admin_update_status(db=db, claim_id=claim_id, update=update)