# 🔍 Proyecto Semana 03: API de Catálogo — Sistema de Gestión de Proyectos Colaborativos

## 🏛️ Dominio Asignado

**Dominio**: Sistema de gestión de proyectos colaborativos | Servicios Profesionales

---

## 🎯 Objetivo

Construir una **API de catálogo** con búsqueda avanzada y filtros múltiples para gestionar equipos de trabajo y sus proyectos colaborativos.

---

## 🗂️ Entidades del Dominio

### Team (Categoría)
Representa equipos de trabajo o áreas profesionales.

```python
Team:
    id: int
    code: str          # Ej: "DEV", "QA", "OPS"
    name: str          # Ej: "Desarrollo", "Calidad"
    description: str
    is_active: bool
```

### Project (Entidad Principal)
Representa proyectos gestionados por equipos.

```python
Project:
    id: int
    code: str          # Ej: "PRJ-001"
    name: str          # Nombre del proyecto
    team_id: int       # FK a Team
    status: str        # planning / active / completed / cancelled
    start_date: date
    end_date: date
    budget: float
    is_active: bool
```

---

## 🔎 Filtros Implementados (7 filtros)

```
GET /projects/?team=1&status=active&min_budget_gte=5000&max_budget_lte=50000&search=api&sort_by=budget&order=desc&page=1&per_page=10
```

| Filtro | Tipo | Descripción |
|--------|------|-------------|
| `team` | int | Filtrar proyectos por equipo |
| `status` | str | Estado: planning / active / completed / cancelled |
| `min_budget_gte` | float | Presupuesto mínimo >= valor |
| `max_budget_lte` | float | Presupuesto máximo <= valor |
| `search` | str | Búsqueda en nombre y código |
| `sort_by` | str | Campo de ordenamiento (id, name, budget, status) |
| `order` | str | asc / desc |
| `page` | int | Número de página |
| `per_page` | int | Resultados por página (máx 100) |

---

## 🚀 Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/teams/` | Listar equipos |
| POST | `/teams/` | Crear equipo |
| GET | `/teams/{id}` | Obtener equipo por ID |
| PUT | `/teams/{id}` | Actualizar equipo |
| DELETE | `/teams/{id}` | Eliminar equipo |
| GET | `/projects/` | Listar proyectos con filtros y paginación |
| POST | `/projects/` | Crear proyecto |
| GET | `/projects/{id}` | Obtener proyecto por ID |
| PUT | `/projects/{id}` | Actualizar proyecto |
| DELETE | `/projects/{id}` | Eliminar proyecto |

---

## 🐳 Ejecución con Docker

```bash
cd bootcamp/week-03/3-proyecto/starter
docker compose up --build
```

Accede a la documentación en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📝 Ejemplos de uso

```bash
# Crear equipo
curl -X POST http://localhost:8000/teams/ \
  -H "Content-Type: application/json" \
  -d '{"code": "DEV", "name": "Desarrollo", "description": "Equipo de desarrollo de software"}'

# Crear proyecto
curl -X POST http://localhost:8000/projects/ \
  -H "Content-Type: application/json" \
  -d '{"code": "PRJ-001", "name": "API Colaborativa", "team_id": 1, "status": "active", "budget": 15000.00}'

# Listar proyectos con filtros
curl "http://localhost:8000/projects/?status=active&sort_by=budget&order=desc&page=1&per_page=5"
```

---

## ✅ Criterios de Evaluación Cubiertos

| Criterio | Estado |
|----------|--------|
| CRUD categorías (teams) | ✅ |
| CRUD entidades (projects) | ✅ |
| 7+ filtros coherentes con el dominio | ✅ |
| Búsqueda por nombre/código | ✅ |
| Paginación y ordenamiento | ✅ |
| Documentación OpenAPI/Swagger | ✅ |
| Docker funcional | ✅ |

---

[← Volver a Prácticas](../2-practicas/) | [Recursos →](../4-recursos/)
