"""Task Manager API - main minimal para arrancar la app de forma segura.

Esta versión ligera elimina secciones incompletas y deja endpoints
de health para poder levantar el servidor y continuar el desarrollo.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Task Manager API (minimal)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"])
async def root():
    return {"message": "Task Manager API (minimal) is running", "version": "1.0.0"}


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "service": "task-manager-api", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
