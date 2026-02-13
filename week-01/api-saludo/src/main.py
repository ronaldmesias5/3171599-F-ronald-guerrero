# ============================================
# PROYECTO: API DE SALUDO
# ============================================
# Semana 01 - Bootcamp FastAPI Zero to Hero
#
# En este proyecto implementarás una API de saludos
# que demuestra el uso de:
# - FastAPI
# - Type hints
# - Path parameters
# - Query parameters
# - Documentación automática
# ============================================

from fastapi import FastAPI

# ============================================
# DATOS DE CONFIGURACIÓN
# ============================================

# Diccionario de saludos por idioma (para colaboradores)
GREETINGS: dict[str, str] = {
    "es": "¡Bienvenido al equipo, {name}!",
    "en": "Welcome to the team, {name}!",
    "fr": "Bienvenue dans l'équipe, {name}!",
    "de": "Willkommen im Team, {name}!",
    "it": "Benvenuto nel team, {name}!",
    "pt": "Bem-vindo à equipe, {name}!",
}

# Idiomas soportados (para documentación)
SUPPORTED_LANGUAGES = list(GREETINGS.keys())


# ============================================
# TODO 1: CREAR LA INSTANCIA DE FASTAPI
# ============================================
# Crea una instancia de FastAPI con la siguiente configuración:
# - title: "Greeting API"
# - description: "API de saludos multiidioma"
# - version: "1.0.0"
#
# Ejemplo:
#   app = FastAPI(title="...", description="...", version="...")

app = FastAPI(
    title="Project Management API",
    description="API de gestión de proyectos colaborativos - Servicios Profesionales",
    version="1.0.0",
    contact={
        "name": "Development Team",
        "email": "dev@projectmanagement.com",
    },
)


# ============================================
# TODO 2: ENDPOINT RAÍZ
# ============================================
# Implementa el endpoint GET /
#
# Debe retornar:
# {
#     "name": "Greeting API",
#     "version": "1.0.0",
#     "docs": "/docs",
#     "languages": ["es", "en", "fr", "de", "it", "pt"]
# }
#
# Recuerda:
# - Usar el decorador @app.get("/")
# - Definir la función como async
# - Agregar docstring para la documentación

@app.get("/")
async def root() -> dict[str, str | list[str]]:
    """Información de la API de gestión de proyectos."""
    return {
        "name": "Project Management API",
        "version": "1.0.0",
        "domain": "collaborative-project-management",
        "docs": "/docs",
        "languages": SUPPORTED_LANGUAGES,
    }


# ============================================
# TODO 3: SALUDO PERSONALIZADO
# ============================================
# Implementa el endpoint GET /greet/{name}
#
# Parámetros:
# - name (path): Nombre de la persona a saludar
# - language (query, default="es"): Idioma del saludo
#
# Debe retornar:
# {
#     "greeting": "¡Hola, Carlos!",
#     "language": "es",
#     "name": "Carlos"
# }
#
# Si el idioma no existe, usar español por defecto.

@app.get("/collaborator/{name}")
async def welcome_collaborator(
    name: str,
    language: str = "es",
) -> dict[str, str]:
    """
    Da la bienvenida a un colaborador en el idioma especificado.
    
    Args:
        name: Nombre del colaborador
        language: Código de idioma (es, en, fr, de, it, pt)
    
    Returns:
        dict: Mensaje de bienvenida personalizado
    """
    # Obtener el template del saludo (usar español por defecto)
    greeting_template = GREETINGS.get(language, GREETINGS["es"])
    greeting = greeting_template.format(name=name)
    
    return {
        "message": greeting,
        "language": language,
        "collaborator": name,
        "role": "team-member",
    }


# ============================================
# TODO 4: SALUDO FORMAL
# ============================================
# Implementa el endpoint GET /greet/{name}/formal
#
# Parámetros:
# - name (path): Nombre/apellido de la persona
# - title (query, default="Sr./Sra."): Título formal
#
# Debe retornar:
# {
#     "greeting": "Estimado/a Dr. García, es un placer saludarle.",
#     "title": "Dr.",
#     "name": "García"
# }

@app.get("/project/{code}/info")
async def get_project_info(
    code: str,
    detail_level: str = "basic",
) -> dict[str, str | int | bool]:
    """
    Obtiene información de un proyecto por su código.
    
    Args:
        code: Código único del proyecto (ej: PROJ-001)
        detail_level: Nivel de detalle (basic, full)
    
    Returns:
        dict: Información del proyecto
    """
    # Información básica del proyecto
    basic_info = {
        "code": code,
        "name": f"Proyecto {code}",
        "status": "active",
        "team_size": 5,
    }
    
    # Si se solicita detalle completo
    if detail_level == "full":
        basic_info["description"] = "Proyecto de desarrollo de software colaborativo"
        basic_info["start_date"] = "2026-01-15"
        basic_info["deadline"] = "2026-06-30"
        basic_info["budget"] = 50000
        basic_info["tasks_completed"] = 15
        basic_info["tasks_total"] = 45
    
    return basic_info


# ============================================
# TODO 5: SALUDO SEGÚN LA HORA
# ============================================
# Implementa el endpoint GET /greet/{name}/time-based
#
# Parámetros:
# - name (path): Nombre de la persona
# - hour (query): Hora del día (0-23)
#
# Lógica:
# - 5 <= hour < 12: "Buenos días, {name}!"
# - 12 <= hour < 18: "Buenas tardes, {name}!"
# - else: "Buenas noches, {name}!"
#
# Debe retornar:
# {
#     "greeting": "Buenos días, Ana!",
#     "hour": 10,
#     "period": "morning"
# }

# Función auxiliar para determinar el servicio disponible según la hora
def get_service_status(hour: int) -> tuple[str, str, list[str]]:
    """
    Determina el estado del servicio según la hora.
    
    Args:
        hour: Hora del día (0-23)
    
    Returns:
        tuple: (mensaje, período, servicios_disponibles)
    """
    if 6 <= hour < 12:
        return (
            "Horario matutino - Planificación y reuniones activas",
            "morning",
            ["planning", "meetings", "code-review"]
        )
    elif 12 <= hour < 18:
        return (
            "Horario vespertino - Desarrollo y colaboración activos",
            "afternoon",
            ["development", "collaboration", "testing"]
        )
    else:
        return (
            "Horario nocturno - Soporte y mantenimiento",
            "night",
            ["support", "maintenance", "deployment"]
        )


@app.get("/service/schedule")
async def get_service_schedule(
    hour: int,
) -> dict[str, str | int | list[str]]:
    """
    Obtiene el estado del servicio según la hora del día.
    
    Args:
        hour: Hora del día (0-23)
    
    Returns:
        dict: Estado del servicio y funcionalidades disponibles
    """
    # Validar que hour esté entre 0-23
    if not 0 <= hour <= 23:
        return {
            "error": "Hora inválida",
            "message": "La hora debe estar entre 0 y 23",
        }
    
    # Obtener estado del servicio
    message, period, services = get_service_status(hour)
    
    return {
        "message": message,
        "hour": hour,
        "period": period,
        "available_services": services,
        "status": "operational",
    }


# ============================================
# TODO 6: HEALTH CHECK
# ============================================
# Implementa el endpoint GET /health
#
# Debe retornar:
# {
#     "status": "healthy",
#     "service": "greeting-api",
#     "version": "1.0.0"
# }

@app.get("/health")
async def health_check() -> dict[str, str]:
    """Verifica el estado de la API de gestión de proyectos."""
    return {
        "status": "healthy",
        "service": "project-management-api",
        "domain": "collaborative-project-management",
        "version": "1.0.0",
    }


# ============================================
# VERIFICACIÓN
# ============================================
# Una vez completados todos los TODOs:
#
# 1. Ejecutar:
#    docker compose up --build
#
# 2. Probar en el navegador:
#    http://localhost:8000/docs
#
# 3. Verificar cada endpoint:
#    - GET /
#    - GET /greet/Carlos
#    - GET /greet/Carlos?language=en
#    - GET /greet/García/formal?title=Dr.
#    - GET /greet/Ana/time-based?hour=10
#    - GET /health
# ============================================
