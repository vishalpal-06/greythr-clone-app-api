from pydantic import BaseModel


class DepartmentBase(BaseModel):
    department_name: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    department_id: int
    

    class Config:
        from_attributes = True