# Sistema de Gestión de Proyectos Colaborativos

**Nombre:** Ronald Jefrey Guerrero Mesías

**Ficha:** 3171599

**Dominio asignado:** Sistema de Gestión de Proyectos Colaborativos

## Descripción

Implementación de una API REST para la entidad `Project` con las características pedidas en el entregable.

- Campos implementados: `id`, `project_code`, `name`, `description` (opcional), `client`, `start_date`, `end_date` (opcional), `budget`, `status`, `is_active`, `created_at`, `updated_at`.
- Validaciones: `project_code` con patrón y normalización, `budget` > 0 (normalizado a 2 decimales), `end_date >= start_date`.
- Endpoints: `POST /projects/`, `GET /projects/`, `GET /projects/{id}`, `GET /projects/by-code/{code}`, `PATCH /projects/{id}`, `DELETE /projects/{id}`.
- Almacenamiento: `InMemoryDB` (volátil) para ejecutar sin configuración de bases de datos.
- Tests: suite con pruebas para creación, duplicado, validación de fechas y borrado.

## Verificación rápida

- Levantar servidor y abrir `/docs` para revisar esquemas y probar endpoints.
- Crear un `Project` con `project_code` válido y comprobar respuesta 201.
- Intentar crear un `Project` con código duplicado y comprobar respuesta 409.
- Enviar `end_date < start_date` y comprobar error de validación (422/400).
- Ejecutar tests y comprobar `4 passed`.

## Archivos clave

- `main.py` — endpoints.
- `models.py` — schemas y validaciones.
- `database.py` — `InMemoryDB`.
- `tests/` — pruebas automatizadas.
- `requirements.txt` — dependencias.

## Ejecutar localmente (rápido)

```bash
cd bootcamp/week-02/3-proyecto/starter
python -m venv .venv
# Windows
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Abrir: `http://localhost:8000/docs`

## Ejecutar tests

```powershell
set PYTHONPATH=bootcamp\week-02\3-proyecto
.venv\Scripts\python.exe -m pytest bootcamp\week-02\3-proyecto\starter\tests -q
```

