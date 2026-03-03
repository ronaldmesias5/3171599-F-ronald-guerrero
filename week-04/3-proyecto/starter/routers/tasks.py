"""
Routers para gestión de tareas.
Endpoints CRUD y transiciones de estado.
"""

from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query

from database import get_db
from models import TaskAssignment, TaskStatus, TaskPriority
from schemas.request import TaskCreateRequest, TaskUpdateRequest
from schemas.response import TaskResponse, TaskDetailResponse, TaskListResponse, ErrorResponse
from exceptions import (
    TaskNotFoundError,
    InvalidStateTransitionError,
    DuplicateTaskCodeError,
    task_manager_exception_handler,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


def generate_task_code(db: Session) -> str:
    """Genera un código único para la tarea."""
    from datetime import datetime as dt
    
    count = db.query(TaskAssignment).count()
    date_part = dt.now().strftime("%Y%m%d")
    return f"TASK-{date_part}-{count + 1:03d}"


def get_task_or_404(db: Session, task_id: int) -> TaskAssignment:
    """Obtiene una tarea o lanza excepción 404."""
    task = db.query(TaskAssignment).filter(TaskAssignment.id == task_id).first()
    if not task:
        raise TaskNotFoundError(task_id)
    return task


# ============================================
# CRUD ENDPOINTS
# ============================================

@router.post("/", response_model=TaskDetailResponse, status_code=201)
async def create_task(
    task_data: TaskCreateRequest,
    db: Session = Depends(get_db),
) -> TaskDetailResponse:
    """
    Crear una nueva tarea.
    
    - **project_name**: Nombre del proyecto
    - **assigned_to**: Miembro asignado
    - **description**: Descripción detallada
    - **priority**: Nivel de prioridad (low, medium, high)
    - **estimated_hours**: Horas estimadas
    
    Retorna: Tarea creada con código único
    """
    # Generar código único
    code = generate_task_code(db)
    
    # Crear tarea
    db_task = TaskAssignment(
        code=code,
        project_name=task_data.project_name,
        assigned_to=task_data.assigned_to,
        description=task_data.description,
        priority=task_data.priority,
        estimated_hours=task_data.estimated_hours,
        status=TaskStatus.PENDING,
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return TaskDetailResponse.model_validate(db_task)


@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    skip: int = Query(0, ge=0, description="Tareas a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Límite de tareas"),
    status: str | None = Query(None, description="Filtrar por estado"),
    db: Session = Depends(get_db),
) -> TaskListResponse:
    """
    Listar todas las tareas con paginación y filtros.
    
    - **skip**: Cantidad de registros a saltar
    - **limit**: Límite de registros a retornar
    - **status**: Filtrar por estado (optional)
    """
    query = db.query(TaskAssignment)
    
    # Filtrar por estado si se proporciona
    if status:
        valid_statuses = [s.value for s in TaskStatus]
        if status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Estado inválido. Válidos: {valid_statuses}",
            )
        query = query.filter(TaskAssignment.status == status)
    
    # Contar total
    total = query.count()
    
    # Aplicar paginación
    tasks = query.offset(skip).limit(limit).all()
    
    return TaskListResponse(
        tasks=[TaskResponse.model_validate(t) for t in tasks],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/{task_id}", response_model=TaskDetailResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> TaskDetailResponse:
    """Obtener detalles completos de una tarea por ID."""
    task = get_task_or_404(db, task_id)
    return TaskDetailResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskDetailResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdateRequest,
    db: Session = Depends(get_db),
) -> TaskDetailResponse:
    """
    Actualizar una tarea existente.
    
    Solo los campos proporcionados serán actualizados.
    """
    task = get_task_or_404(db, task_id)
    
    # Actualizar solo los campos proporcionados
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    task.updated_at = datetime.now()
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return TaskDetailResponse.model_validate(task)


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Eliminar una tarea por ID."""
    task = get_task_or_404(db, task_id)
    
    db.delete(task)
    db.commit()


# ============================================
# STATE TRANSITION ENDPOINTS
# ============================================

@router.post("/{task_id}/start", response_model=TaskDetailResponse, status_code=200)
async def start_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> TaskDetailResponse:
    """
    Cambiar estado de tarea a IN_PROGRESS.
    
    Solo permitido desde PENDING.
    """
    task = get_task_or_404(db, task_id)
    
    # Validar transición
    if task.status != TaskStatus.PENDING:
        raise InvalidStateTransitionError(task.status.value, TaskStatus.IN_PROGRESS.value)
    
    # Cambiar estado
    task.status = TaskStatus.IN_PROGRESS
    task.started_at = datetime.now()
    task.updated_at = datetime.now()
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return TaskDetailResponse.model_validate(task)


@router.post("/{task_id}/complete", response_model=TaskDetailResponse, status_code=200)
async def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> TaskDetailResponse:
    """
    Cambiar estado de tarea a COMPLETED.
    
    Solo permitido desde IN_PROGRESS.
    """
    task = get_task_or_404(db, task_id)
    
    # Validar transición
    if task.status != TaskStatus.IN_PROGRESS:
        raise InvalidStateTransitionError(task.status.value, TaskStatus.COMPLETED.value)
    
    # Cambiar estado
    task.status = TaskStatus.COMPLETED
    task.completed_at = datetime.now()
    task.updated_at = datetime.now()
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return TaskDetailResponse.model_validate(task)


@router.post("/{task_id}/cancel", response_model=TaskDetailResponse, status_code=200)
async def cancel_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> TaskDetailResponse:
    """
    Cambiar estado de tarea a CANCELLED.
    
    Permitido desde PENDING o IN_PROGRESS.
    """
    task = get_task_or_404(db, task_id)
    
    # Validar transición
    if task.status in (TaskStatus.COMPLETED, TaskStatus.CANCELLED):
        raise InvalidStateTransitionError(task.status.value, TaskStatus.CANCELLED.value)
    
    # Cambiar estado
    task.status = TaskStatus.CANCELLED
    task.cancelled_at = datetime.now()
    task.updated_at = datetime.now()
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return TaskDetailResponse.model_validate(task)
