
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import teams, projects

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Catálogo - Sistema de gestión de proyectos colaborativos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(teams.router, prefix="/teams", tags=["teams"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])

@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz"""
    return {
        "message": "API de gestión de proyectos colaborativos",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/healthz")
def health() -> dict:
    return {"status": "ok"}
