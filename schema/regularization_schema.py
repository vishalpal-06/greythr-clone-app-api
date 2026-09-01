# schema/regularization_schema.py
from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class Status(str, Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"


class RegularizationBase(BaseModel):
    regularization_start_time: datetime = Field(
        ..., description="Start date & time (e.g. 2025-11-25 09:00:00)"
    )
    regularization_end_time: datetime = Field(
        ..., description="End date & time (e.g. 2025-11-25 18:20:33)"
    )
    regularization_reason: str = Field(..., min_length=5, max_length=255)

    @model_validator(mode="after")
    def end_must_be_after_start(self):
        if self.regularization_end_time <= self.regularization_start_time:
            raise ValueError("end_time must be after start_time")  # pragma: no cover
        return self


class RegularizationCreate(RegularizationBase):
    pass


class RegularizationStatusUpdate(BaseModel):
    regularization_status: Status


class RegularizationResponse(RegularizationBase):
    regularization_id: int
    regularization_status: Status
    fk_employee_id: int
    fk_manager_id: int

    model_config = ConfigDict(from_attributes=True)
