# 🚀 Proyecto Semana 04: Task Manager API


**Dominio**: Sistema de gestión de proyectos colaborativos | Servicios Profesionales

Construir una API de gestión de tareas para equipos de servicios profesionales, permitiendo asignar tareas, cambiar estados y manejar errores de forma robusta.

---

## 🎯 Objetivo

Construir una **API REST completa** aplicando responses, status codes, manejo de errores y documentación OpenAPI.

---

## 📦 Requisitos Funcionales

### TaskAssignment: Entidad Principal (10+ campos)

```python
from enum import Enum
from datetime import datetime
from pydantic import BaseModel

class TaskStatus(str, Enum):
    PENDING = "pending"              # Tarea creada, sin iniciar
    IN_PROGRESS = "in_progress"      # En ejecución
    COMPLETED = "completed"          # Finalizada
    CANCELLED = "cancelled"          # Cancelada

class TaskAssignment(BaseModel):
    id: int
    code: str                         # Unique: TASK-YYYYMMDD-XXX (auto-generated)
    project_name: str                 # Nombre del proyecto
    assigned_to: str                  # Miembro del equipo asignado
    description: str                  # Descripción de la tarea
    status: TaskStatus                # Estado actual
    priority: str                      # high, medium, low
    estimated_hours: float            # Horas estimadas
    created_at: datetime              # Creación
    started_at: datetime | None       # Inicio real
    completed_at: datetime | None     # Finalización
    cancelled_at: datetime | None     # Cancelación
```

### State Transitions (Máquina de Estados)

```
pending → in_progress  (endpoint: POST /tasks/{id}/start)
in_progress → completed  (endpoint: POST /tasks/{id}/complete)
pending/in_progress → cancelled  (endpoint: POST /tasks/{id}/cancel)
```

### Response Models

```python
# Para listados y cálculos (sin datos internos)
class TaskResponse(BaseModel):
    id: int
    code: str
    project_name: str
    assigned_to: str
    status: TaskStatus
    priority: str
    estimated_hours: float
    created_at: datetime

# Completo (para detalles)
class TaskDetailResponse(TaskResponse):
    description: str
    started_at: datetime | None
    completed_at: datetime | None
    cancelled_at: datetime | None
```

### Error Handling

```python
class TaskNotFoundError(HTTPException):
    def __init__(self, task_id: int):
        super().__init__(
            status_code=404,
            detail=f"Tarea {task_id} no encontrada"
        )

class InvalidStateTransitionError(HTTPException):
    def __init__(self, current: str, target: str):
        super().__init__(
            status_code=400,
            detail=f"No se puede transicionar de '{current}' a '{target}'"
        )

class DuplicateTaskCodeError(HTTPException):
    def __init__(self, code: str):
        super().__init__(
            status_code=409,
            detail=f"Código de tarea '{code}' ya existe"
        )
```

---

## 🗂️ Estructura del Proyecto

```
starter/
├── main.py                   # FastAPI app, routers
├── models.py                 # SQLAlchemy models
├── database.py               # Engine, SessionLocal, get_db
├── exceptions.py             # HTTPExceptions personalizadas
├── schemas/
│   ├── __init__.py
│   ├── request.py            # TaskCreate, TaskUpdate
│   └── response.py           # TaskResponse, TaskDetailResponse
├── routers/
│   ├── __init__.py
│   └── tasks.py              # Endpoints CRUD + transiciones
├── pyproject.toml            # Dependencias
├── Dockerfile                # Containerización
├── docker-compose.yml        # Orquestación
└── .dockerignore
```

---

## 🎯 Endpoints Requeridos

| Método | Ruta | Código | Descripción |
|--------|------|--------|-------------|
| GET | `/tasks/` | 200 | Listar todas las tareas |
| GET | `/tasks/{id}` | 200, 404 | Obtener tarea por ID |
| POST | `/tasks/` | 201 | Crear nueva tarea |
| PUT | `/tasks/{id}` | 200, 404 | Actualizar tarea |
| DELETE | `/tasks/{id}` | 204, 404 | Eliminar tarea |
| POST | `/tasks/{id}/start` | 200, 400, 404 | Cambiar a in_progress |
| POST | `/tasks/{id}/complete` | 200, 400, 404 | Cambiar a completed |
| POST | `/tasks/{id}/cancel` | 200, 400, 404 | Cambiar a cancelled |

---

## 📚 Recursos

- [FastAPI Response Models](https://fastapi.tiangolo.com/tutorial/response-model/)
- [HTTP Status Codes](https://fastapi.tiangolo.com/tutorial/status-codes/)
- [Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [OpenAPI Documentation](https://fastapi.tiangolo.com/tutorial/response-model/#response-model-encoding)

