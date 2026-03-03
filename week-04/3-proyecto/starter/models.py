"""
Task Manager API - Modelos SQLAlchemy
Semana 04 - Proyecto

Define los modelos de base de datos para tareas.
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Integer, String, Enum as SQLEnum
from sqlalchemy.sql import func

from database import Base


class TaskStatus(str, Enum):
    """Estados posibles de una tarea colaborativa"""
    PENDING = "pending"              # Tarea creada, sin iniciar
    IN_PROGRESS = "in_progress"      # En ejecución
    COMPLETED = "completed"          # Finalizada
    CANCELLED = "cancelled"          # Cancelada


class TaskPriority(str, Enum):
    """Niveles de prioridad"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskAssignment(Base):
    """
    Modelo de asignación de tarea en el sistema colaborativo.
    
    Representa una tarea asignada a un miembro del equipo de servicios profesionales.
    """
    __tablename__ = "task_assignments"
    
    # Identificadores
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    
    # Información del proyecto y asignación
    project_name = Column(String(255), nullable=False, index=True)
    assigned_to = Column(String(150), nullable=False, index=True)
    description = Column(String(1000), nullable=False)
    
    # Estado y prioridad
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False, index=True)
    priority = Column(SQLEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    
    # Horas estimadas
    estimated_hours = Column(Integer, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<TaskAssignment(id={self.id}, code={self.code}, status={self.status})>"
