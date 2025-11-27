# schema/leave_schema.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class LeaveBase(BaseModel):
    assign_year: int = Field(..., ge=2000, le=2100)
    casual_leave: int = Field(..., ge=0)
    plan_leave: int = Field(..., ge=0)
    probation_leave: int = Field(..., ge=0)
    sick_leave: int = Field(..., ge=0)
    total_leave: int = Field(..., ge=0)
    balance_leave: int = Field(..., ge=0)


class LeaveCreate(LeaveBase):
    fk_employee_id: int = Field(..., gt=0)


class LeaveResponse(LeaveBase):
    leave_id: int
    fk_employee_id: int

    model_config = ConfigDict(from_attributes=True)