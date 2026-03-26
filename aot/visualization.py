"""Görselleştirme: 1D ve 2D Taylor açılım grafikleri."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import sympy as sp

if TYPE_CHECKING:
    from .core import TaylorExpansion

# Renk sabitleri
_COLOR_ORIGINAL = "steelblue"
_COLOR_TAYLOR = "crimson"
_ALPHA_SURFACE = 0.65


def plot_expansion(te: "TaylorExpansion", **kwargs):
    """Boyuta göre uygun plot fonksiyonunu çağırır.

    Args:
        te: TaylorExpansion nesnesi.
        **kwargs: 1D veya 2D plot fonksiyonuna iletilir.

    Returns:
        matplotlib veya plotly Figure nesnesi.

    Raises:
        NotImplementedError: 3D (n=3) fonksiyonlar için.
    """
    n = te._n
    if n == 1:
        return _plot_1d(te, **kwargs)
    elif n == 2:
        return _plot_2d(te, **kwargs)
    else:
        raise NotImplementedError(
            "3D fonksiyonlar (f: R³→R) 4 boyutlu görselleştirme gerektirir. "
            "Sembolik ve sayısal sonuçlara T.symbolic / T.evaluate() ile erişin."
        )


def _plot_1d(
    te: "TaylorExpansion",
    xlim: tuple[float, float] | None = None,
    n_points: int = 400,
):
    """1D fonksiyon için matplotlib grafiği.

    Args:
        te: TaylorExpansion nesnesi.
        xlim: x eksen sınırları. None → açılım noktası ±3.
        n_points: Grafik için örnekleme sayısı.

    Returns:
        matplotlib Figure nesnesi.
    """
    import matplotlib.pyplot as plt

    var = te._variables[0]
    a0 = float(te._point[0])

    if xlim is None:
        xlim = (a0 - 3.0, a0 + 3.0)

    x_vals = np.linspace(xlim[0], xlim[1], n_points)

    f_num = te.to_numeric()
    t_num = te.taylor_to_numeric()

    y_orig = f_num(x_vals)
    y_tayl = t_num(x_vals)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_vals, y_orig, color=_COLOR_ORIGINAL, lw=2, label=f"$f({sp.latex(var)})$")
    ax.plot(x_vals, y_tayl, color=_COLOR_TAYLOR, lw=2, ls="--", label="Taylor (order=2)")
    ax.scatter([a0], [float(f_num(a0))], color="red", zorder=5, s=60, label="Açılım noktası")
    ax.set_xlabel(f"${sp.latex(var)}$")
    ax.set_ylabel("$f$")
    ax.legend()
    ax.set_title("Orijinal Fonksiyon vs Taylor Açılımı")
    ax.grid(True, alpha=0.3)

    return fig


def _plot_2d(
    te: "TaylorExpansion",
    xlim: tuple[float, float] | None = None,
    ylim: tuple[float, float] | None = None,
    n_points: int = 60,
    backend: str = "auto",
):
    """2D fonksiyon için interaktif (plotly) veya statik (matplotlib) grafik.

    Args:
        te: TaylorExpansion nesnesi.
        xlim: x₁ eksen sınırları. None → açılım noktası ±2.
        ylim: x₂ eksen sınırları. None → açılım noktası ±2.
        n_points: Her eksende örnekleme sayısı.
        backend: ``"plotly"``, ``"matplotlib"``, veya ``"auto"`` (plotly varsa kullanır).

    Returns:
        plotly Figure veya matplotlib Figure nesnesi.
    """
    a0 = float(te._point[0])
    a1 = float(te._point[1])

    if xlim is None:
        xlim = (a0 - 2.0, a0 + 2.0)
    if ylim is None:
        ylim = (a1 - 2.0, a1 + 2.0)

    x1_vals = np.linspace(xlim[0], xlim[1], n_points)
    x2_vals = np.linspace(ylim[0], ylim[1], n_points)
    X1, X2 = np.meshgrid(x1_vals, x2_vals)

    f_num = te.to_numeric()
    t_num = te.taylor_to_numeric()

    Z_orig = f_num(X1, X2)
    Z_tayl = t_num(X1, X2)

    # Backend seçimi
    use_plotly = False
    if backend == "plotly":
        use_plotly = True
    elif backend == "auto":
        try:
            import plotly  # noqa: F401
            use_plotly = True
        except ImportError:
            use_plotly = False

    if use_plotly:
        return _plot_2d_plotly(X1, X2, Z_orig, Z_tayl, te._point)
    else:
        return _plot_2d_matplotlib(X1, X2, Z_orig, Z_tayl, te._point)


def _plot_2d_plotly(X1, X2, Z_orig, Z_tayl, point):
    """Plotly ile interaktif 3D yüzey grafiği."""
    import plotly.graph_objects as go

    fig = go.Figure()

    fig.add_trace(go.Surface(
        x=X1, y=X2, z=Z_orig,
        colorscale="Blues",
        opacity=_ALPHA_SURFACE,
        name="Orijinal f",
        showscale=False,
    ))

    fig.add_trace(go.Surface(
        x=X1, y=X2, z=Z_tayl,
        colorscale="Reds",
        opacity=_ALPHA_SURFACE,
        name="Taylor",
        showscale=False,
    ))

    a0, a1 = float(point[0]), float(point[1])
    # Açılım noktasının z değeri için orijin değerini yaklaştır
    z_point = float(Z_orig[
        abs(X2[:, 0] - a1).argmin(),
        abs(X1[0, :] - a0).argmin()
    ])

    fig.add_trace(go.Scatter3d(
        x=[a0], y=[a1], z=[z_point],
        mode="markers",
        marker=dict(size=8, color="red"),
        name="Açılım noktası",
    ))

    fig.update_layout(
        scene=dict(
            xaxis_title="x₁",
            yaxis_title="x₂",
            zaxis_title="f(x₁,x₂)",
        ),
        title="Orijinal Fonksiyon vs Taylor Açılımı",
        legend=dict(x=0, y=1),
    )

    return fig


def _plot_2d_matplotlib(X1, X2, Z_orig, Z_tayl, point):
    """Matplotlib ile statik 3D yüzey grafiği (plotly fallback)."""
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot_surface(X1, X2, Z_orig, alpha=_ALPHA_SURFACE, color=_COLOR_ORIGINAL, label="Orijinal")
    ax.plot_surface(X1, X2, Z_tayl, alpha=_ALPHA_SURFACE, color=_COLOR_TAYLOR, label="Taylor")

    a0, a1 = float(point[0]), float(point[1])
    z_point = float(Z_orig[
        abs(X2[:, 0] - a1).argmin(),
        abs(X1[0, :] - a0).argmin()
    ])
    ax.scatter([a0], [a1], [z_point], color="red", s=80, zorder=5)

    ax.set_xlabel("x₁")
    ax.set_ylabel("x₂")
    ax.set_zlabel("f(x₁,x₂)")
    ax.set_title("Orijinal Fonksiyon vs Taylor Açılımı")

    return fig
