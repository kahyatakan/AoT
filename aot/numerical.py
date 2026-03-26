"""Sayısal değerlendirme: lambdify sarmalayıcıları."""

from __future__ import annotations

from typing import Callable

import numpy as np
import sympy as sp


def make_numeric_func(
    expr: sp.Expr,
    variables: list[sp.Symbol],
) -> Callable:
    """SymPy ifadesini numpy uyumlu sayısal fonksiyona çevirir.

    Elde edilen fonksiyon hem skaler hem meshgrid (element-wise) girdi
    kabul eder; bu sayede plot için doğrudan kullanılabilir.

    Args:
        expr: Sayısallaştırılacak SymPy ifadesi.
        variables: Bağımsız değişken sembolleri.

    Returns:
        ``(*args) -> np.ndarray | float`` imzalı callable.
        1D için ``f(x)``, 2D için ``f(x1, x2)``, 3D için ``f(x1, x2, x3)``
        şeklinde çağrılır.
    """
    # Scalar SymPy Matrix ifadelerini önce scalar'a çevir
    if isinstance(expr, (sp.MatrixBase,)):
        if expr.shape == (1, 1):
            expr = expr[0, 0]
        else:
            raise ValueError("Matris ifadeleri sayısallaştırılamaz; scalar ifade verin.")

    f_num = sp.lambdify(variables, expr, modules=["numpy"])
    return f_num
