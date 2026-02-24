from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from models.team import Team
from schemas.team import TeamCreate, TeamRead, TeamUpdate

router = APIRouter()


@router.post("/", response_model=TeamRead, status_code=201)
def create_team(team_in: TeamCreate, db: Session = Depends(get_db)) -> Team:
    team = Team(code=team_in.code, name=team_in.name, description=team_in.description, is_active=team_in.is_active)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


@router.get("/", response_model=List[TeamRead])
def list_teams(q: str | None = Query(None), limit: int = Query(20, ge=1), db: Session = Depends(get_db)):
    query = db.query(Team)
    if q:
        query = query.filter(Team.name.ilike(f"%{q}%") | Team.code.ilike(f"%{q}%"))
    return query.limit(limit).all()


@router.get("/{team_id}", response_model=TeamRead)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.put("/{team_id}", response_model=TeamRead)
def update_team(team_id: int, payload: TeamUpdate, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(team, k, v)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


@router.delete("/{team_id}", status_code=204)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    db.delete(team)
    db.commit()
    return None
