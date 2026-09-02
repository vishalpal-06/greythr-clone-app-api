# schema/leave_application_schema.py
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Status(StrEnum):
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
    total_days: int | None = None
    leave_status: Status
    fk_employee_id: int
    fk_manager_id: int

    model_config = ConfigDict(from_attributes=True)
