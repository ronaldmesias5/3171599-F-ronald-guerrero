from __future__ import annotations

from decimal import Decimal
from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from .validators import project_code_validator, budget_validator, validate_date_order


class StatusEnum(str, Enum):
    planned = "planned"
    active = "active"
    paused = "paused"
    finished = "finished"


class ProjectBase(BaseModel):
    """Schema base para Project con configuración común."""

    model_config = ConfigDict(str_strip_whitespace=True)

    project_code: str = Field(..., min_length=5, max_length=12, description="Código único del proyecto")
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    client: str = Field(..., min_length=2, max_length=100)
    start_date: date
    end_date: Optional[date] = None
    budget: Decimal = Field(..., gt=0)
    status: StatusEnum = Field(default=StatusEnum.planned)
    is_active: bool = Field(default=True)

    @field_validator("project_code")
    @classmethod
    def validate_project_code(cls, v: str) -> str:
        return project_code_validator(v)

    @field_validator("budget")
    @classmethod
    def validate_budget(cls, v: Decimal) -> Decimal:
        return budget_validator(v)

    @model_validator(mode="after")
    def check_dates(self) -> "ProjectBase":
        validate_date_order(self.start_date, self.end_date)
        return self


class ProjectCreate(ProjectBase):
    """Schema usado para crear proyectos."""


class ProjectUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)
    project_code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    client: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[Decimal] = None
    status: Optional[StatusEnum] = None
    is_active: Optional[bool] = None

    @model_validator(mode="after")
    def validate_dates(self) -> "ProjectUpdate":
        validate_date_order(self.start_date, self.end_date)
        return self


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
