from pydantic import BaseModel, ConfigDict


class DepartmentBase(BaseModel):
    department_name: str


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    department_id: int

    model_config = ConfigDict(from_attributes=True)
