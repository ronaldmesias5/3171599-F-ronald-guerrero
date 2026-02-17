import pytest
import random
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_project_and_get():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        code = f"PROJ-{random.randint(1,9999):04d}"
        payload = {"project_code": code,"name": "Test Project","client": "ACME","start_date": "2026-02-15","budget": "100.00"}
        r = await client.post("/projects/", json=payload)
        if r.status_code != 201:
            print("DEBUG create response:", r.status_code, r.text)
        assert r.status_code == 201
        data = r.json()
        assert data["project_code"] == code

        # GET by id
        pid = data["id"]
        r2 = await client.get(f"/projects/{pid}")
        assert r2.status_code == 200


@pytest.mark.asyncio
async def test_duplicate_project_code():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        code = f"PROJ-{random.randint(1,9999):04d}"
        payload = {"project_code": code,"name": "Dup","client": "ACME","start_date": "2026-02-15","budget": "200.00"}
        r = await client.post("/projects/", json=payload)
        if r.status_code != 201:
            print("DEBUG dup create response:", r.status_code, r.text)
        assert r.status_code == 201

        r2 = await client.post("/projects/", json=payload)
        assert r2.status_code == 409


@pytest.mark.asyncio
async def test_invalid_dates_validation():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        code = f"AAA-{random.randint(100,999)}"
        payload = {"project_code": code,"name": "Bad Dates","client": "ACME","start_date": "2026-02-20","end_date": "2026-02-10","budget": "50.00"}
        r = await client.post("/projects/", json=payload)
        if r.status_code not in (400, 422):
            print("DEBUG bad dates response:", r.status_code, r.text)
        # should be validation error (422) or pydantic error
        assert r.status_code in (400, 422)


@pytest.mark.asyncio
async def test_delete_project():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        code = f"PROJ-{random.randint(1,9999):04d}"
        payload = {"project_code": code,"name": "To Delete","client": "ACME","start_date": "2026-02-15","budget": "10.00"}
        r = await client.post("/projects/", json=payload)
        assert r.status_code == 201
        pid = r.json()["id"]
        r2 = await client.delete(f"/projects/{pid}")
        assert r2.status_code == 204
        r3 = await client.get(f"/projects/{pid}")
        assert r3.status_code == 404
