# schema/payslip_schema.py
from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Optional
from datetime import datetime


class PayslipBase(BaseModel):
    basic_amount: float = Field(..., gt=0)
    hra: float = Field(0.0, ge=0)
    special_allowance: float = Field(0.0, ge=0)
    internet_allowance: float = Field(0.0, ge=0)
    payslip_month: datetime = Field(..., description="Must be first day of month: YYYY-MM-01")

    @validator("payslip_month")
    def must_be_first_day(cls, v):
        if v.day != 1 or v.hour != 0 or v.minute != 0 or v.second != 0:
            raise ValueError("payslip_month must be the 1st day of the month at 00:00:00") # pragma: no cover
        return v


class PayslipCreate(PayslipBase):
    fk_employee_id: int


class PayslipResponse(PayslipBase):
    payslip_id: int
    fk_employee_id: int

    model_config = ConfigDict(from_attributes=True)