"""FastAPI backend — AOT web arayüzü için REST API."""

from __future__ import annotations

import asyncio
import sys
import os

import sympy as sp
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Proje kökünü sys.path'e ekle (server/ dışından import için)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aot import TaylorExpansion
from aot.parser import latex_to_sympy

from .schemas import ExpandRequest, ExpandResponse, ErrorResponse

app = FastAPI(
    title="AOT API",
    description="Anvil of Taylor — Taylor serisi açılım API'si",
    version="0.2.0",
)

# CORS — geliştirme ortamı
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_TIMEOUT_SECONDS = 30


async def _compute_expansion(req: ExpandRequest) -> ExpandResponse:
    """Hesaplamayı ayrı thread'de çalıştırır (blocking sympy için)."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _sync_expand, req)


def _sync_expand(req: ExpandRequest) -> ExpandResponse:
    """Senkron hesaplama — thread pool'da çalışır."""
    # 1. LaTeX → sympy
    expr, variables = latex_to_sympy(req.latex)

    # 2. Taylor açılımı
    T = TaylorExpansion(
        f=expr,
        variables=variables,
        point=req.point,
        order=req.order,
    )

    # 3. Grafik JSON
    try:
        plot_json = T.plot(output="json")
    except Exception:
        plot_json = None

    # 4. Yanıtı oluştur
    dim = len(variables)
    return ExpandResponse(
        symbolic_latex=T.latex(),
        variables=[sp.latex(v) for v in variables],
        dimension=dim,
        gradient_latex=sp.latex(T.gradient) if T.gradient is not None else None,
        hessian_latex=sp.latex(T.hessian) if T.hessian is not None else None,
        plot_json=plot_json,
    )


@app.post("/api/expand")
async def expand(req: ExpandRequest, request: Request) -> JSONResponse:
    """LaTeX fonksiyon girişini alıp Taylor açılımını hesaplar.

    Args:
        req: Açılım isteği (latex, point, order).

    Returns:
        ExpandResponse veya ErrorResponse JSON.
    """
    try:
        result = await asyncio.wait_for(
            _compute_expansion(req),
            timeout=_TIMEOUT_SECONDS,
        )
        return JSONResponse(result.model_dump())

    except asyncio.TimeoutError:
        error = ErrorResponse(
            error_type="math_error",
            message=f"Hesaplama {_TIMEOUT_SECONDS} saniyede tamamlanamadı.",
            hint="Daha düşük bir order değeri deneyin.",
        )
        return JSONResponse(error.model_dump(), status_code=408)

    except ValueError as exc:
        msg = str(exc)
        if "parse edilemedi" in msg or "LaTeX" in msg.lower():
            error_type = "parse_error"
            hint = "LaTeX sözdizimini kontrol edin. Süslü parantezlerin eşleştiğinden emin olun."
        elif "tanımsız" in msg or "sıfıra bölme" in msg:
            error_type = "math_error"
            hint = "Farklı bir açılım noktası seçin."
        else:
            error_type = "validation_error"
            hint = None
        error = ErrorResponse(error_type=error_type, message=msg, hint=hint)
        return JSONResponse(error.model_dump(), status_code=200)

    except NotImplementedError as exc:
        error = ErrorResponse(
            error_type="validation_error",
            message=str(exc),
            hint="Çok değişkenli fonksiyonlar için order=2 kullanın.",
        )
        return JSONResponse(error.model_dump(), status_code=200)

    except Exception as exc:
        error = ErrorResponse(
            error_type="math_error",
            message=f"Beklenmeyen hata: {type(exc).__name__}",
            hint="Fonksiyonu ve açılım noktasını kontrol edin.",
        )
        return JSONResponse(error.model_dump(), status_code=200)


@app.get("/health")
async def health() -> dict:
    """Sağlık kontrolü endpoint'i."""
    return {"status": "ok", "version": "0.2.0"}
