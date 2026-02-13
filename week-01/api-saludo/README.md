# API de Gestión de Proyectos

Proyecto de la Semana 1 - Bootcamp FastAPI

**Nombre**: Ronald Jefrey Guerrero Mesias  
**Ficha**: 3171599  
**Dominio**: Sistema de gestión de proyectos colaborativos - Servicios Profesionales

## Descripción

API para gestionar proyectos colaborativos. Permite dar bienvenida a colaboradores en varios idiomas, consultar información de proyectos y ver el estado de los servicios por horario.

**Tecnologías**: Python 3.14, FastAPI, Docker

## Requisitos

- Docker Desktop instalado
- Puerto 8000 disponible

## Instalación

1. Clonar el repositorio
2. Ir a la carpeta del proyecto:
```bash
cd bootcamp/week-01/3-proyecto/starter
```

3. Ejecutar con Docker:
```bash
docker compose up --build
```

4. Abrir en el navegador:
- API: http://localhost:8000
- Documentación: http://localhost:8000/docs

## Endpoints

### 1. Información de la API
```
GET /
```
Devuelve información general de la API.

### 2. Bienvenida a colaboradores
```
GET /collaborator/{name}?language=es
```
Da la bienvenida a un colaborador en el idioma especificado.

**Parámetros:**
- `name`: Nombre del colaborador
- `language`: Idioma (es, en, fr, de, it, pt) - opcional, default: es

**Ejemplo:**
```bash
curl http://localhost:8000/collaborator/Maria
curl http://localhost:8000/collaborator/John?language=en
```

### 3. Información de proyectos
```
GET /project/{code}/info?detail_level=basic
```
Consulta información de un proyecto.

**Parámetros:**
- `code`: Código del proyecto (ej: PROJ-001)
- `detail_level`: Nivel de detalle (basic o full) - opcional, default: basic

**Ejemplo:**
```bash
curl http://localhost:8000/project/PROJ-001/info
curl http://localhost:8000/project/PROJ-001/info?detail_level=full
```

### 4. Estado de servicios por horario
```
GET /service/schedule?hour=10
```
Devuelve los servicios disponibles según la hora del día.

**Parámetros:**
- `hour`: Hora del día (0-23)

**Horarios:**
- Mañana (6-11): Planificación, reuniones, code review
- Tarde (12-17): Desarrollo, colaboración, testing
- Noche (18-5): Soporte, mantenimiento, deployment

**Ejemplo:**
```bash
curl http://localhost:8000/service/schedule?hour=10
```

### 5. Health check
```
GET /health
```
Verifica que la API esté funcionando correctamente.

## Comandos útiles

**Detener la API:**
```bash
docker compose down
```

**Ver logs:**
```bash
docker compose logs -f
```

**Reconstruir:**
```bash
docker compose up --build
```

## Estructura del proyecto

```
starter/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
└── src/
    └── main.py
```

