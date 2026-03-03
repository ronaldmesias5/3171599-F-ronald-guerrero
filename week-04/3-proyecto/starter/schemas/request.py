"""
Esquemas Pydantic para REQUEST (entrada de datos).
Validación de datos enviados por el cliente.
"""

from pydantic import BaseModel, Field


class TaskCreateRequest(BaseModel):
    """Schema para crear una nueva tarea."""
    
    project_name: str = Field(..., min_length=3, max_length=255, description="Nombre del proyecto")
    assigned_to: str = Field(..., min_length=2, max_length=150, description="Miembro asignado")
    description: str = Field(..., min_length=10, max_length=1000, description="Descripción detallada")
    priority: str = Field(default="medium", pattern="^(low|medium|high)$", description="Prioridad")
    estimated_hours: int = Field(..., gt=0, le=480, description="Horas estimadas (1-480)")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "project_name": "Desarrollo de API REST",
                "assigned_to": "Juan Pérez",
                "description": "Implementar endpoints de autenticación y autorización",
                "priority": "high",
                "estimated_hours": 16,
            }
        }
    }


class TaskUpdateRequest(BaseModel):
    """Schema para actualizar una tarea existente."""
    
    project_name: str | None = Field(None, min_length=3, max_length=255)
    assigned_to: str | None = Field(None, min_length=2, max_length=150)
    description: str | None = Field(None, min_length=10, max_length=1000)
    priority: str | None = Field(None, pattern="^(low|medium|high)$")
    estimated_hours: int | None = Field(None, gt=0, le=480)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "priority": "low",
                "estimated_hours": 8,
            }
        }
    }
