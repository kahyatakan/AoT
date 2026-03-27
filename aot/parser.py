"""LaTeX string → SymPy ifadesi dönüştürücü."""

from __future__ import annotations

import re

import sympy as sp

# Bilinen sabitler — değişken listesinden çıkarılır
_KNOWN_CONSTANTS: frozenset[str] = frozenset({'pi', 'e', 'E', 'I', 'oo', 'zoo', 'nan'})

# Fonksiyon komutları için regex parçası
_FUNC_PAT = r'(?:sin|cos|tan|sec|csc|cot|ln|log|arctan|arcsin|arccos|exp|sqrt)'
_FUNC_CMD = r'(\\' + _FUNC_PAT + r')'


def latex_to_sympy(latex_str: str) -> tuple[sp.Expr, list[sp.Symbol]]:
    """LaTeX string'i SymPy ifadesi ve değişken listesine dönüştürür.

    Args:
        latex_str: Dönüştürülecek LaTeX string (örn. r"\\frac{x^3}{x^2+y^2}").

    Returns:
        ``(expr, variables)`` tuple'ı:
        - ``expr``: SymPy ifadesi
        - ``variables``: Serbest değişken sembolleri, adına göre sıralı

    Raises:
        ValueError: LaTeX parse edilemezse veya 4+ değişken tespit edilirse.
    """
    preprocessed = _preprocess_latex(latex_str)
    expr = _parse(preprocessed)
    expr = _postprocess_expr(expr)
    variables = _detect_variables(expr)
    return expr, variables


# ---------------------------------------------------------------------------
# Ön işleme
# ---------------------------------------------------------------------------

def _preprocess_latex(s: str) -> str:
    """Parse öncesi LaTeX string ön işlemeleri.

    Args:
        s: Ham LaTeX string.

    Returns:
        Parse edilmeye hazır dönüştürülmüş string.
    """
    s = s.strip()

    # \func x_{1} → \func(x_{1}) — brace'li subscript, parensiz
    s = re.sub(_FUNC_CMD + r'\s+x_\{(\d+)\}', r'\1(x_{\2})', s)
    # \func x_1 → \func(x_1) — bare subscript, } ile bitmeyecek
    s = re.sub(_FUNC_CMD + r'\s+x_(\d+)(?!\})', r'\1(x_\2)', s)
    # \func x → \func(x) — tek harfli arg, parensiz
    s = re.sub(_FUNC_CMD + r'\s+([a-zA-Z])\b', r'\1(\2)', s)

    # Çarpma operatörleri
    s = s.replace(r'\cdot', '*')
    s = s.replace(r'\times', '*')

    # Parantez kısaltmaları
    s = s.replace(r'\left', '')
    s = s.replace(r'\right', '')

    # \ln → \log (sympy'de log = doğal logaritma)
    s = s.replace(r'\ln', r'\log')

    return s


# ---------------------------------------------------------------------------
# Parse
# ---------------------------------------------------------------------------

def _parse(preprocessed: str) -> sp.Expr:
    """Ön işlenmiş string'i SymPy ifadesine çevirir.

    Önce sympy'nin antlr tabanlı parser'ını dener; başarısız olursa
    latex2sympy2 fallback'ini kullanır.

    Args:
        preprocessed: Ön işlenmiş LaTeX string.

    Returns:
        SymPy ifadesi.

    Raises:
        ValueError: Her iki yöntem de başarısız olursa.
    """
    from sympy.parsing.latex import parse_latex

    try:
        expr = parse_latex(preprocessed)
        if expr is None:
            raise ValueError("parse_latex None döndürdü")
        return expr
    except Exception as primary_exc:
        # Fallback: latex2sympy2 (opsiyonel bağımlılık)
        try:
            from latex2sympy2 import latex2sympy  # type: ignore[import]
            expr = latex2sympy(preprocessed)
            if expr is None:
                raise ValueError("latex2sympy None döndürdü")
            return expr
        except ImportError:
            pass
        except Exception:
            pass

        _raise_parse_error(preprocessed, primary_exc)


def _raise_parse_error(latex_str: str, exc: Exception) -> None:
    """Anlaşılır parse hata mesajı üretir ve fırlatır.

    Args:
        latex_str: Parse edilemeyen string.
        exc: Asıl istisna.

    Raises:
        ValueError: Her zaman.
    """
    msg = f"'{latex_str}' ifadesi parse edilemedi."
    if latex_str.count('{') != latex_str.count('}'):
        msg += " Olası sorun: kapanmamış süslü parantez '}'."
    elif latex_str.count('(') != latex_str.count(')'):
        msg += " Olası sorun: kapanmamış parantez ')'."
    raise ValueError(msg) from exc


# ---------------------------------------------------------------------------
# Son işleme
# ---------------------------------------------------------------------------

def _postprocess_expr(expr: sp.Expr) -> sp.Expr:
    """Parse sonrası ifade düzeltmeleri.

    Args:
        expr: Ham parse sonucu.

    Returns:
        Düzeltilmiş SymPy ifadesi.
    """
    # e veya E sembolü → sp.E (Euler sabiti)
    for name in ('e', 'E'):
        sym = sp.Symbol(name)
        if sym in expr.free_symbols:
            expr = expr.subs(sym, sp.E)

    # pi sembolü → sp.pi
    pi_sym = sp.Symbol('pi')
    if pi_sym in expr.free_symbols:
        expr = expr.subs(pi_sym, sp.pi)

    # x_{1} gibi subscript sembolleri → x1
    for sym in list(expr.free_symbols):
        name = sym.name
        clean = re.sub(r'_\{(\d+)\}', r'\1', name)
        if clean != name:
            expr = expr.subs(sym, sp.Symbol(clean))

    # log(x, E) → log(x) (normalize)
    expr = expr.replace(
        lambda ex: (
            ex.func == sp.log
            and len(ex.args) == 2
            and ex.args[1] == sp.E
        ),
        lambda ex: sp.log(ex.args[0]),
    )

    return expr


# ---------------------------------------------------------------------------
# Değişken tespiti
# ---------------------------------------------------------------------------

def _detect_variables(expr: sp.Expr) -> list[sp.Symbol]:
    """İfadedeki serbest değişkenleri tespit eder ve sıralar.

    Args:
        expr: SymPy ifadesi.

    Returns:
        Sıralı değişken listesi.

    Raises:
        ValueError: 4 veya daha fazla değişken varsa.
    """
    free = expr.free_symbols
    variables = [
        s for s in free
        if s.name not in _KNOWN_CONSTANTS and not s.is_number
    ]

    if len(variables) > 3:
        raise ValueError(
            f"{len(variables)} değişken tespit edildi: "
            f"{sorted(s.name for s in variables)}. "
            "AOT en fazla 3 değişken destekler."
        )

    variables.sort(key=_sort_key)
    return variables


def _sort_key(sym: sp.Symbol) -> tuple[str, int]:
    """Değişken sıralama anahtarı: x < x1 < x2 < y < z.

    Args:
        sym: SymPy sembolü.

    Returns:
        (prefix, number) tuple'ı.
    """
    name = sym.name
    match = re.match(r'^([a-zA-Z]+)(\d*)$', name)
    if match:
        prefix = match.group(1)
        num = int(match.group(2)) if match.group(2) else -1
        return (prefix, num)
    return (name, -1)
