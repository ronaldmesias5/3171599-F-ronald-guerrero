from __future__ import annotations

from typing import List, Optional
from decimal import Decimal
from datetime import datetime

from .models import ProjectResponse, ProjectCreate, ProjectUpdate


class InMemoryDB:
    def __init__(self) -> None:
        self._data: List[dict] = []
        self._id = 1

    def _now(self) -> datetime:
        return datetime.utcnow()

    def create(self, payload: ProjectCreate) -> ProjectResponse:
        # uniqueness check should be done externally before create
        item = payload.model_dump()
        item["id"] = self._id
        item["created_at"] = self._now()
        item["updated_at"] = None
        self._data.append(item)
        self._id += 1
        return ProjectResponse(**item)

    def get(self, _id: int) -> Optional[ProjectResponse]:
        for item in self._data:
            if item["id"] == _id:
                return ProjectResponse(**item)
        return None

    def get_by_code(self, code: str) -> Optional[ProjectResponse]:
        code = code.strip().upper()
        for item in self._data:
            if item["project_code"].upper() == code:
                return ProjectResponse(**item)
        return None

    def list(self, skip: int = 0, limit: int = 10, **filters) -> List[ProjectResponse]:
        results = self._data
        # basic filters: status, client
        if filters.get("status"):
            results = [r for r in results if r.get("status") == filters.get("status")]
        if filters.get("client"):
            results = [r for r in results if r.get("client") == filters.get("client")]
        sliced = results[skip: skip + limit]
        return [ProjectResponse(**s) for s in sliced]

    def update(self, _id: int, payload: ProjectUpdate) -> Optional[ProjectResponse]:
        for i, item in enumerate(self._data):
            if item["id"] == _id:
                updated = {**item, **{k: v for k, v in payload.model_dump().items() if v is not None}}
                updated["updated_at"] = self._now()
                self._data[i] = updated
                return ProjectResponse(**updated)
        return None

    def delete(self, _id: int) -> bool:
        for i, item in enumerate(self._data):
            if item["id"] == _id:
                del self._data[i]
                return True
        return False


# Singleton DB for the starter
db = InMemoryDB()

