"""
Esquemas Pydantic para RESPONSE (salida de datos).
Serialización de datos devueltos por la API.
"""

from datetime import datetime
from pydantic import BaseModel, Field


class TaskResponse(BaseModel):
    """Response estándar para una tarea (sin datos sensibles)."""
    
    id: int
    code: str = Field(..., description="Identificador único: TASK-YYYYMMDD-XXX")
    project_name: str
    assigned_to: str
    status: str
    priority: str
    estimated_hours: int
    created_at: datetime
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "code": "TASK-20260228-001",
                "project_name": "Desarrollo de API REST",
                "assigned_to": "Juan Pérez",
                "status": "pending",
                "priority": "high",
                "estimated_hours": 16,
                "created_at": "2026-02-28T10:30:00",
            }
        }
    }


class TaskDetailResponse(TaskResponse):
    """Response completo para una tarea (con detalles adicionales)."""
    
    description: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    cancelled_at: datetime | None = None
    updated_at: datetime | None = None
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "code": "TASK-20260228-001",
                "project_name": "Desarrollo de API REST",
                "assigned_to": "Juan Pérez",
                "description": "Implementar endpoints de autenticación y autorización",
                "status": "in_progress",
                "priority": "high",
                "estimated_hours": 16,
                "created_at": "2026-02-28T10:30:00",
                "started_at": "2026-02-28T11:00:00",
                "completed_at": None,
                "cancelled_at": None,
                "updated_at": "2026-02-28T14:30:00",
            }
        }
    }


class TaskListResponse(BaseModel):
    """Response para listado paginado de tareas."""
    
    tasks: list[TaskResponse]
    total: int = Field(..., description="Total de tareas")
    skip: int = Field(..., description="Tareas saltadas")
    limit: int = Field(..., description="Límite de tareas")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "tasks": [
                    {
                        "id": 1,
                        "code": "TASK-20260228-001",
                        "project_name": "Proyecto A",
                        "assigned_to": "Juan",
                        "status": "in_progress",
                        "priority": "high",
                        "estimated_hours": 16,
                        "created_at": "2026-02-28T10:30:00",
                    }
                ],
                "total": 10,
                "skip": 0,
                "limit": 1,
            }
        }
    }


class ErrorResponse(BaseModel):
    """Response de error estándar."""
    
    error: str = Field(..., description="Código de error")
    message: str = Field(..., description="Mensaje descriptivo")
    status_code: int = Field(..., description="Código HTTP")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "error": "TASK_NOT_FOUND",
                "message": "Tarea con id 99 no encontrada",
                "status_code": 404,
            }
        }
    }
