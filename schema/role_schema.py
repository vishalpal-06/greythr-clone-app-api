from pydantic import BaseModel

class RoleBase(BaseModel):
    role: str

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    role_id: int

    class Config:
        from_attributes = True