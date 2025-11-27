# schema/expense_claim_schema.py
from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Optional
from datetime import datetime
from enum import Enum


class Status(str, Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"


class ExpenseClaimBase(BaseModel):
    claim_date: datetime = Field(..., description="Date of expense")
    amount: float = Field(..., gt=0)
    description: str = Field(..., min_length=10, max_length=500)


class ExpenseClaimCreate(ExpenseClaimBase):
    pass


class ExpenseClaimStatusUpdate(BaseModel):
    claim_status: Status


class ExpenseClaimResponse(ExpenseClaimBase):
    claim_id: int
    claim_status: Status
    fk_employee_id: int
    fk_manager_id: int

    model_config = ConfigDict(from_attributes=True)