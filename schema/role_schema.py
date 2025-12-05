from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    role: str


class RoleCreate(RoleBase):
    pass


class RoleResponse(RoleBase):
    role_id: int

    model_config = ConfigDict(from_attributes=True)
