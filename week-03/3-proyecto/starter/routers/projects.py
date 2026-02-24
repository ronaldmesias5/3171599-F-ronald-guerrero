from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from database import get_db
from models.project import Project
from schemas.project import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter()


@router.post("/", response_model=ProjectRead, status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> Project:
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/", response_model=List[ProjectRead])
def list_projects(
    team: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    min_budget_gte: Optional[float] = Query(None),
    max_budget_lte: Optional[float] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("id"),
    order: str = Query("asc"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Project)
    if team:
        try:
            team_id = int(team)
            query = query.filter(Project.team_id == team_id)
        except ValueError:
            pass
    if status:
        query = query.filter(Project.status == status)
    if min_budget_gte is not None:
        query = query.filter(Project.budget >= min_budget_gte)
    if max_budget_lte is not None:
        query = query.filter(Project.budget <= max_budget_lte)
    if search:
        q = f"%{search}%"
        query = query.filter(or_(Project.name.ilike(q), Project.code.ilike(q)))

    # Ordering
    order_func = asc if order.lower() == "asc" else desc
    if hasattr(Project, sort_by):
        query = query.order_by(order_func(getattr(Project, sort_by)))

    # Pagination
    offset = (page - 1) * per_page
    items = query.offset(offset).limit(per_page).all()
    return items


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(project, k, v)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return None
