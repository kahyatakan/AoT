"""Yardımcı fonksiyonlar: sembol üretimi ve girdi doğrulama."""

from __future__ import annotations

import warnings

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


def validate_function(
    f: sp.Expr,
    variables: list[sp.Symbol],
    point: list[sp.Basic],
) -> None:
    """Fonksiyon ve açılım noktasını doğrular.

    Args:
        f: Açılım yapılacak SymPy ifadesi.
        variables: Bağımsız değişken sembolleri.
        point: Normalize edilmiş açılım noktası.

    Raises:
        TypeError: f bir sp.Expr değilse.
        ValueError: f açılım noktasında tanımsızsa (sonsuzluk, NaN).
    """
    if not isinstance(f, sp.Basic):
        raise TypeError(
            f"f bir SymPy ifadesi olmalıdır (sp.Expr), {type(f).__name__} verildi."
        )

    # Serbest sembolleri kontrol et
    free = f.free_symbols
    var_set = set(variables)
    point_syms = {p for p in point if isinstance(p, sp.Basic) and p.free_symbols}
    allowed = var_set | {s for ps in point_syms for s in ps.free_symbols}
    extra = free - allowed
    if extra:
        warnings.warn(
            f"Fonksiyon içinde beklenmedik semboller var: {extra}. "
            "Bu semboller açılım sırasında sabit gibi davranır.",
            stacklevel=3,
        )

    # Açılım noktasında fonksiyon değerini kontrol et
    subs = dict(zip(variables, point))
    try:
        val = f.subs(subs)
        # Sembolik noktada (tüm point elemanları sayısal değilse) kontrol atla
        if val.free_symbols:
            return
        val_num = complex(val)
        if (
            val_num != val_num  # NaN kontrolü
            or abs(val_num) == float("inf")
        ):
            raise ValueError(
                f"f fonksiyonu açılım noktası a={[str(p) for p in point]}'da tanımsızdır "
                "(sıfıra bölme veya sonsuzluk). Farklı bir açılım noktası deneyin."
            )
    except (ZeroDivisionError, OverflowError):
        raise ValueError(
            f"f fonksiyonu açılım noktası a={[str(p) for p in point]}'da tanımsızdır "
            "(sıfıra bölme veya sonsuzluk). Farklı bir açılım noktası deneyin."
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
        point: Açılım noktası (sayısal veya sembolik liste). None kabul edilmez.
        order: Taylor açılım mertebesi.

    Returns:
        Normalize edilmiş açılım noktası listesi (sp.Basic elemanları).

    Raises:
        ValueError: point=None, geçersiz boyut veya uyumsuz uzunluklar.
        NotImplementedError: Çok değişkenli fonksiyonlarda order > 2 ise.
    """
    n = len(variables)
    _validate_dimension(n)

    # point zorunlu — None kesinlikle kabul edilmez
    if point is None:
        raise ValueError(
            "Açılım noktası (point) belirtilmelidir. "
            "Orijin için point=[0] veya point=[0,0] kullanın."
        )

    if order < 1:
        raise ValueError(f"order en az 1 olmalıdır, {order} verildi.")

    if n == 1:
        # 1D: order 1–1000 arası serbest
        if order > 1000:
            raise ValueError("order en fazla 1000 olabilir.")
        if order > 100:
            warnings.warn(
                "Yüksek mertebe hesaplaması uzun sürebilir.",
                stacklevel=3,
            )
    else:
        # Çok değişkenli: şimdilik sadece order=2
        if order > 2:
            raise NotImplementedError(
                "Çok değişkenli fonksiyonlarda şu an yalnızca order=2 desteklenir."
            )

    if len(point) != n:
        raise ValueError(
            f"point uzunluğu ({len(point)}) variables uzunluğuyla ({n}) eşleşmiyor."
        )

    # Her elemanı SymPy nesnesine çevir
    normalized = [sp.sympify(p) for p in point]

    # Fonksiyon doğrulaması
    validate_function(f, variables, normalized)

    return normalized
