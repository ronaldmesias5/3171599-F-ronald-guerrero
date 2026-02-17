from __future__ import annotations

from fastapi import FastAPI, HTTPException, status, Query
from fastapi.responses import JSONResponse, Response

from .models import ProjectCreate, ProjectResponse, ProjectUpdate
from .database import db

app = FastAPI(title="Projects API - Starter")


@app.post("/projects/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate):
    # Uniqueness check for project_code
    existing = db.get_by_code(payload.project_code)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="project_code already exists")
    created = db.create(payload)
    return created


@app.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int):
    p = db.get(project_id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project not found")
    return p


@app.get("/projects/", response_model=list[ProjectResponse])
def list_projects(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), status: str | None = None, client: str | None = None):
    filters = {}
    if status:
        filters["status"] = status
    if client:
        filters["client"] = client
    items = db.list(skip=skip, limit=limit, **filters)
    return items


@app.get("/projects/by-code/{code}", response_model=ProjectResponse)
def get_by_code(code: str):
    p = db.get_by_code(code)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project not found")
    return p


@app.patch("/projects/{project_id}", response_model=ProjectResponse)
def patch_project(project_id: int, payload: ProjectUpdate):
    # If payload contains project_code and it's duplicated, reject
    payload_data = payload.model_dump()
    new_code = payload_data.get("project_code")
    if new_code:
        existing = db.get_by_code(new_code)
        if existing and existing.id != project_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="project_code already exists")
    updated = db.update(project_id, payload)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project not found")
    return updated


@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int):
    ok = db.delete(project_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": "Projects API"}
