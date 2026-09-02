from datetime import date

from pydantic import BaseModel, ConfigDict


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    joining_date: date
    address: str | None = None
    isadmin: bool
    fk_department_id: int
    fk_role_id: int
    fk_manager_id: int | None = None


class EmployeeCreate(EmployeeBase):
    password: str


class EmployeeResponse(EmployeeBase):
    employee_id: int

    model_config = ConfigDict(from_attributes=True)


class EmployeeUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    joining_date: date | None = None
    address: str | None = None
    isadmin: bool | None = None
    fk_department_id: int | None = None
    fk_role_id: int | None = None
    fk_manager_id: int | None = None
    password: str | None = None
