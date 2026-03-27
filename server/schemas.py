"""FastAPI request/response Pydantic modelleri."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, field_validator


class ExpandRequest(BaseModel):
    """POST /api/expand istek gövdesi."""

    latex: str
    point: list[float]
    order: int = 2

    @field_validator("latex")
    @classmethod
    def latex_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("latex boş olamaz")
        return v

    @field_validator("order")
    @classmethod
    def order_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("order en az 1 olmalıdır")
        return v

    @field_validator("point")
    @classmethod
    def point_not_empty(cls, v: list[float]) -> list[float]:
        if len(v) == 0:
            raise ValueError("point en az 1 eleman içermelidir")
        return v


class ExpandResponse(BaseModel):
    """POST /api/expand başarılı yanıt gövdesi."""

    status: str = "ok"
    symbolic_latex: str
    variables: list[str]
    dimension: int
    gradient_latex: str | None = None
    hessian_latex: str | None = None
    plot_json: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    """POST /api/expand hata yanıt gövdesi."""

    status: str = "error"
    error_type: str  # "parse_error" | "math_error" | "validation_error"
    message: str
    hint: str | None = None
