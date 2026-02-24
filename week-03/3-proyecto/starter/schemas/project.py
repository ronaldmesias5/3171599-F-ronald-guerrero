from pydantic import BaseModel
from typing import Optional
from datetime import date
from pydantic import ConfigDict


class ProjectBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    team_id: Optional[int] = None
    status: Optional[str] = "planning"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    is_active: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True)


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    team_id: Optional[int] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)
