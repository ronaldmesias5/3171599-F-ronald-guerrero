from pydantic import BaseModel
from typing import Optional
from pydantic import ConfigDict


class TeamBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True)


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)
