from pydantic import BaseModel
from typing import Optional
from datetime import date


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    joining_date: date
    address: Optional[str] = None
    isadmin: bool
    fk_department_id: int
    fk_role_id: int
    fk_manager_id: Optional[int] = None


class EmployeeCreate(EmployeeBase):
    password: str


class EmployeeResponse(EmployeeBase):
    employee_id: int

    class Config:
        from_attributes = True


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    joining_date: Optional[date] = None
    address: Optional[str] = None
    isadmin: Optional[bool] = None
    fk_department_id: Optional[int] = None
    fk_role_id: Optional[int] = None
    fk_manager_id: Optional[int] = None
    password: Optional[str] = None
