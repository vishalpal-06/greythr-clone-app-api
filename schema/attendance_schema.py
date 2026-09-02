# schema/attendance_schema.py
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AttendanceBase(BaseModel):
    punch_time: datetime


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceResponse(AttendanceBase):
    attendance_id: int
    fk_employee_id: int

    model_config = ConfigDict(from_attributes=True)
