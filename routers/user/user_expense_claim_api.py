# api/user_expense_claim_api.py
from fastapi import APIRouter, status
from typing import List
from schema.expense_claim_schema import (
    ExpenseClaimCreate, ExpenseClaimResponse, ExpenseClaimStatusUpdate, Status
)
from routers.auth import db_dependency, user_dependency
from common.expense_claim import (
    create_expense_claim, delete_expense_claim,
    get_my_claims_by_status, get_my_claim_by_id, get_my_claims_by_month
)

router = APIRouter(prefix="/my/expense-claims", tags=["My Expense Claims"])


@router.post("/", response_model=ExpenseClaimResponse, status_code=status.HTTP_201_CREATED)
def create_expense(claim_in: ExpenseClaimCreate, db: db_dependency, user: user_dependency):
    return create_expense_claim(db=db, claim_in=claim_in, user=user)


@router.delete("/{claim_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(claim_id: int, db: db_dependency, user: user_dependency):
    delete_expense_claim(db=db, claim_id=claim_id, user=user)


@router.get("/status/{status}", response_model=List[ExpenseClaimResponse])
def get_exp_by_status(status: Status, db: db_dependency, user: user_dependency):
    return get_my_claims_by_status(db=db, status=status, user=user)


@router.get("/{claim_id}", response_model=ExpenseClaimResponse)
def get_expense_by_id(claim_id: int, db: db_dependency, user: user_dependency):
    return get_my_claim_by_id(db=db, claim_id=claim_id, user=user)


@router.get("/month/{year}/{month}", response_model=List[ExpenseClaimResponse])
def get_all_expense_by_month(year: int, month: int, db: db_dependency, user: user_dependency):
    return get_my_claims_by_month(db=db, year=year, month=month, user=user)