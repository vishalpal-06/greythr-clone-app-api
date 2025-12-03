# schema/salary_schema.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class SalaryBase(BaseModel):
    lpa: float = Field(..., gt=0, description="Salary in Lakhs Per Annum")
    salary_year: int = Field(
        ..., ge=2000, le=2100, description="Year of the salary record"
    )


class SalaryCreate(SalaryBase):
    fk_employee_id: int = Field(..., gt=0)


class SalaryResponse(SalaryBase):
    salary_id: int
    fk_employee_id: int

    model_config = ConfigDict(from_attributes=True)
