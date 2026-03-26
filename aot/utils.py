"""Yardımcı fonksiyonlar: sembol üretimi ve girdi doğrulama."""

from __future__ import annotations

import sympy as sp


def make_symbols(n: int) -> list[sp.Symbol]:
    """n adet x1, x2, ..., xn sembolü üretir.

    Args:
        n: Üretilecek sembol sayısı.

    Returns:
        SymPy Symbol listesi.

    Raises:
        ValueError: n < 1 veya n > 3 ise.
    """
    _validate_dimension(n)
    return list(sp.symbols(f"x1:{n + 1}"))


def _validate_dimension(n: int) -> None:
    """Boyutu 1–3 arasında doğrular.

    Args:
        n: Kontrol edilecek boyut sayısı.

    Raises:
        ValueError: n < 1 veya n > 3 ise.
    """
    if not (1 <= n <= 3):
        raise ValueError(
            f"Boyut 1 ile 3 arasında olmalıdır, {n} verildi."
        )


def validate_inputs(
    f: sp.Expr,
    variables: list[sp.Symbol],
    point: list | None,
    order: int,
) -> list[sp.Basic]:
    """Girdi parametrelerini doğrular ve normalize edilmiş açılım noktasını döndürür.

    Args:
        f: Açılım yapılacak SymPy ifadesi.
        variables: Bağımsız değişken sembolleri.
        point: Açılım noktası (sayısal veya sembolik liste, None ise orijin).
        order: Taylor açılım mertebesi.

    Returns:
        Normalize edilmiş açılım noktası listesi (sp.Basic elemanları).

    Raises:
        ValueError: Geçersiz boyut veya uyumsuz uzunluklar.
        NotImplementedError: order != 2 ise.
    """
    n = len(variables)
    _validate_dimension(n)

    if order != 2:
        raise NotImplementedError(
            f"Şu an sadece order=2 destekleniyor, {order} verildi."
        )

    if point is None:
        # Maclaurin serisi: orijin
        return [sp.Integer(0)] * n

    if len(point) != n:
        raise ValueError(
            f"point uzunluğu ({len(point)}) variables uzunluğuyla ({n}) eşleşmiyor."
        )

    # Her elemanı SymPy nesnesine çevir
    return [sp.sympify(p) for p in point]
