"""FastAPI endpoint testleri."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from server.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Sağlık kontrolü
# ---------------------------------------------------------------------------

def test_health():
    """GET /health → 200."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


# ---------------------------------------------------------------------------
# 1D açılım
# ---------------------------------------------------------------------------

class TestExpand1D:
    def test_sin_x(self):
        """sin(x) açılımı → status=ok, sembolik sonuç var."""
        resp = client.post("/api/expand", json={
            "latex": r"\sin(x)",
            "point": [0.0],
            "order": 5,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["dimension"] == 1
        assert data["symbolic_latex"]
        assert data["variables"] == ["x"]
        assert data["gradient_latex"] is None  # 1D'de None

    def test_exp_x(self):
        """e^x açılımı → plot_json mevcut."""
        resp = client.post("/api/expand", json={
            "latex": r"e^{x}",
            "point": [0.0],
            "order": 3,
        })
        data = resp.json()
        assert data["status"] == "ok"
        assert data["plot_json"] is not None
        assert "data" in data["plot_json"]

    def test_1d_high_order(self):
        """1D yüksek order → başarılı."""
        resp = client.post("/api/expand", json={
            "latex": r"\sin(x)",
            "point": [0.0],
            "order": 20,
        })
        data = resp.json()
        assert data["status"] == "ok"


# ---------------------------------------------------------------------------
# 2D açılım
# ---------------------------------------------------------------------------

class TestExpand2D:
    def test_exp_2d(self):
        """e^(x1²+x2²) açılımı → gradient ve hessian var."""
        resp = client.post("/api/expand", json={
            "latex": r"e^{x_1^2 + x_2^2}",
            "point": [0.0, 0.0],
            "order": 2,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["dimension"] == 2
        assert data["gradient_latex"] is not None
        assert data["hessian_latex"] is not None
        assert data["plot_json"] is not None

    def test_complex_2d(self):
        """Karmaşık 2D fonksiyon → başarılı."""
        resp = client.post("/api/expand", json={
            "latex": r"\frac{e^{x_1^2+x_2^2}}{\sin(x_1) \cdot \cos(x_2)}",
            "point": [1.0, 0.5],
            "order": 2,
        })
        data = resp.json()
        assert data["status"] == "ok"
        assert data["dimension"] == 2

    def test_2d_order3_error(self):
        """2D, order=3 → hata yanıtı (not implemented)."""
        resp = client.post("/api/expand", json={
            "latex": r"x_1^2 + x_2^2",
            "point": [0.0, 0.0],
            "order": 3,
        })
        data = resp.json()
        assert data["status"] == "error"
        assert data["error_type"] == "validation_error"


# ---------------------------------------------------------------------------
# Hata durumları
# ---------------------------------------------------------------------------

class TestErrors:
    def test_parse_error(self):
        """Bozuk LaTeX → parse_error."""
        resp = client.post("/api/expand", json={
            "latex": r"\frac{x^3}{x^2 + y^2",  # kapanmamış }
            "point": [1.0, 1.0],
            "order": 2,
        })
        data = resp.json()
        assert data["status"] == "error"
        assert data["error_type"] == "parse_error"

    def test_undefined_at_point(self):
        """Açılım noktasında tanımsız → math_error."""
        resp = client.post("/api/expand", json={
            "latex": r"\frac{1}{x}",
            "point": [0.0],
            "order": 2,
        })
        data = resp.json()
        assert data["status"] == "error"
        assert data["error_type"] in ("math_error", "validation_error")

    def test_empty_latex(self):
        """Boş LaTeX → 422 Unprocessable Entity."""
        resp = client.post("/api/expand", json={
            "latex": "",
            "point": [0.0],
            "order": 2,
        })
        assert resp.status_code == 422

    def test_invalid_order(self):
        """order=0 → 422."""
        resp = client.post("/api/expand", json={
            "latex": r"\sin(x)",
            "point": [0.0],
            "order": 0,
        })
        assert resp.status_code == 422
