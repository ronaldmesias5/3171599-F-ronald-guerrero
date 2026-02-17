from __future__ import annotations

import re
from decimal import Decimal
from datetime import date


def project_code_validator(v: str) -> str:
    """Valida y normaliza el project_code.

    Acepta patrones como AAA-123 o PROJ-0001 (3-6 letras, guión, 3-4 dígitos).
    Devuelve el valor en mayúsculas y sin espacios externos.
    """
    v = v.strip().upper()
    if not re.match(r"^[A-Z]{3,6}-\d{3,4}$", v):
        raise ValueError("project_code must match pattern: AAA-123 or PROJ-0001")
    return v


def budget_validator(v: Decimal) -> Decimal:
    """Normaliza y valida el budget como Decimal con 2 decimales."""
    if v <= 0:
        raise ValueError("budget must be greater than 0")
    return v.quantize(Decimal("0.01"))


def validate_date_order(start_date: date | None, end_date: date | None) -> None:
    """Comprueba que end_date sea igual o posterior a start_date si ambos existen."""
    if start_date is not None and end_date is not None and end_date < start_date:
        raise ValueError("end_date must be equal or after start_date")
