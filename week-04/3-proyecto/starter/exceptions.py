"""
Task Manager API - Excepciones Personalizadas
Semana 04 - Proyecto

Define excepciones de negocio y handlers para manejo de errores.
"""

from fastapi import Request
from fastapi.responses import JSONResponse


# ============================================
# CUSTOM EXCEPTIONS
# ============================================

class TaskManagerException(Exception):
    """Excepción base para Task Manager."""
    
    def __init__(
        self,
        error_code: str,
        message: str,
        status_code: int = 400,
        details: dict | None = None,
    ):
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class TaskNotFoundError(TaskManagerException):
    """Tarea no encontrada."""
    
    def __init__(self, task_id: int):
        super().__init__(
            error_code="TASK_NOT_FOUND",
            message=f"Tarea con id {task_id} no encontrada",
            status_code=404,
        )


class InvalidStateTransitionError(TaskManagerException):
    """Transición de estado no válida."""
    
    def __init__(self, current_status: str, target_status: str):
        super().__init__(
            error_code="INVALID_STATE_TRANSITION",
            message=f"No se puede transicionar de '{current_status}' a '{target_status}'",
            status_code=400,
        )


class DuplicateTaskCodeError(TaskManagerException):
    """Código de tarea duplicado."""
    
    def __init__(self, code: str):
        super().__init__(
            error_code="DUPLICATE_TASK_CODE",
            message=f"Código de tarea '{code}' ya existe",
            status_code=409,
        )


class ValidationError(TaskManagerException):
    """Error de validación de datos."""
    
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(
            error_code="VALIDATION_ERROR",
            message=message,
            status_code=422,
            details=details,
        )


# ============================================
# EXCEPTION HANDLERS
# ============================================

async def task_manager_exception_handler(request: Request, exc: TaskManagerException):
    """Handler para excepciones de Task Manager."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "status_code": exc.status_code,
            **({"details": exc.details} if exc.details else {}),
        },
    )
    def __init__(self, task_id: int):
        # TODO: Implementar
        super().__init__(
            code="TASK_NOT_FOUND",
            message=f"Task with id {task_id} not found",
            status_code=404
        )


class InvalidStatusTransitionError(TaskManagerException):
    """
    Invalid status transition exception.
    
    TODO: Implementar constructor que:
    - Reciba current_status y target_status
    - code="INVALID_STATUS_TRANSITION"
    - status_code=400
    """
    
    def __init__(self, current_status: str, target_status: str):
        # TODO: Implementar
        pass


class DuplicateTaskError(TaskManagerException):
    """
    Duplicate task exception.
    
    TODO: Implementar constructor que:
    - Reciba title: str
    - code="DUPLICATE_TASK"
    - status_code=409
    """
    
    def __init__(self, title: str):
        # TODO: Implementar
        pass


# ============================================
# EXCEPTION HANDLERS - TODO: Completar
# ============================================

async def task_manager_exception_handler(
    request: Request,
    exc: TaskManagerException
) -> JSONResponse:
    """
    Handler para TaskManagerException.
    
    TODO: Retornar JSONResponse con formato:
    {
        "error": {
            "code": exc.code,
            "message": exc.message,
            "details": exc.details
        }
    }
    """
    # TODO: Implementar
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )
