"""
Task Manager API - Configuración de Base de Datos
Semana 04 - Proyecto

Configuración de SQLAlchemy con SQLite para desarrollo.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Base URL para SQLite (desarrollo)
DATABASE_URL = "sqlite:///./tasks.db"

# Crear engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Necesario para SQLite
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()


def get_db():
    """
    Dependency para inyectar sesión en endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
            "priority": TaskPriority.low,
        },
    ]
    
    for task_data in sample_tasks:
        task_id = get_next_id()
        now = datetime.now()
        
        tasks_db[task_id] = {
            "id": task_id,
            "title": task_data["title"],
            "description": task_data["description"],
            "status": task_data["status"],
            "priority": task_data["priority"],
            "created_at": now,
            "updated_at": None,
            "completed_at": now if task_data["status"] == TaskStatus.completed else None,
        }


# Initialize with sample data
seed_database()
