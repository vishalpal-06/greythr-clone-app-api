# schema/leave_application_schema.py
from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class Status(str, Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"


class LeaveApplicationBase(BaseModel):
    from_date: datetime = Field(..., description="Leave start date & time")
    end_date: datetime = Field(..., description="Leave end date & time")
    leave_reason: str = Field(..., min_length=5, max_length=255)

    @model_validator(mode="after")
    def end_after_start(self):
        if self.end_date <= self.from_date:
            raise ValueError("end_date must be after from_date")  # pragma: no cover
        return self


class LeaveApplicationCreate(LeaveApplicationBase):
    pass


class LeaveApplicationStatusUpdate(BaseModel):
    leave_status: Status


class LeaveApplicationResponse(LeaveApplicationBase):
    leave_application_id: int
    total_days: Optional[int] = None
    leave_status: Status
    fk_employee_id: int
    fk_manager_id: int

    model_config = ConfigDict(from_attributes=True)
