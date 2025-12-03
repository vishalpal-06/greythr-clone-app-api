# api/manager_expense_claim_api.py
from fastapi import APIRouter
from typing import List
from schema.expense_claim_schema import (
    ExpenseClaimResponse,
    ExpenseClaimStatusUpdate,
    Status,
)
from routers.auth import db_dependency, user_dependency
from common.expense_claim import (
    get_manager_claim_by_id,
    get_manager_claims_by_status,
    get_manager_claims_by_month,
    get_manager_claims_by_employee_and_month,
    manager_update_status,
)

router = APIRouter(prefix="/expense-claims", tags=["Manager - Expense Claims"])


@router.get("/{claim_id}", response_model=ExpenseClaimResponse)
def get_by_id_where_manager_current_user(
    claim_id: int, db: db_dependency, user: user_dependency
):
    return get_manager_claim_by_id(db=db, claim_id=claim_id, user=user)


@router.get("/month/{year}/{month}", response_model=List[ExpenseClaimResponse])
def get_all_expense_by_month_where_manager_current_user(
    year: int, month: int, db: db_dependency, user: user_dependency
):
    return get_manager_claims_by_month(db=db, year=year, month=month, user=user)


@router.get("/status/{status}", response_model=List[ExpenseClaimResponse])
def get_all_expense_by_status_where_manager_current_user(
    status: Status, db: db_dependency, user: user_dependency
):
    return get_manager_claims_by_status(db=db, status=status, user=user)


@router.get(
    "/employee/{emp_id}/month/{year}/{month}", response_model=List[ExpenseClaimResponse]
)
def get_expense_by_employeeid_and_month_where_manager_currentuser(
    emp_id: int, year: int, month: int, db: db_dependency, user: user_dependency
):
    return get_manager_claims_by_employee_and_month(
        db=db, emp_id=emp_id, year=year, month=month, user=user
    )


@router.put("/{claim_id}/status", response_model=ExpenseClaimResponse)
def update_exp_status_where_manager_currentuser(
    claim_id: int,
    update: ExpenseClaimStatusUpdate,
    db: db_dependency,
    user: user_dependency,
):
    return manager_update_status(db=db, claim_id=claim_id, update=update, user=user)
