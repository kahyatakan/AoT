"""LaTeX parser testleri."""

import pytest
import sympy as sp

from aot.parser import latex_to_sympy
from aot import TaylorExpansion


# ---------------------------------------------------------------------------
# Yardımcı
# ---------------------------------------------------------------------------

def sym_equal(a: sp.Expr, b: sp.Expr) -> bool:
    return sp.simplify(a - b) == 0


# ---------------------------------------------------------------------------
# Temel kalıplar
# ---------------------------------------------------------------------------

class TestParseBasic:
    def test_sin(self):
        expr, vars_ = latex_to_sympy(r"\sin(x)")
        x = sp.Symbol("x")
        assert sym_equal(expr, sp.sin(x))
        assert vars_ == [x]

    def test_cos_subscript(self):
        expr, vars_ = latex_to_sympy(r"\cos(x_1)")
        x1 = sp.Symbol("x1")
        assert sym_equal(expr, sp.cos(x1))
        assert vars_ == [x1]

    def test_tan(self):
        expr, vars_ = latex_to_sympy(r"\tan(x)")
        x = sp.Symbol("x")
        assert sym_equal(expr, sp.tan(x))

    def test_arctan(self):
        expr, vars_ = latex_to_sympy(r"\arctan(x)")
        x = sp.Symbol("x")
        assert sym_equal(expr, sp.atan(x))

    def test_arcsin(self):
        expr, vars_ = latex_to_sympy(r"\arcsin(x)")
        x = sp.Symbol("x")
        assert sym_equal(expr, sp.asin(x))

    def test_ln(self):
        expr, vars_ = latex_to_sympy(r"\ln(x)")
        x = sp.Symbol("x")
        assert sym_equal(expr, sp.log(x))

    def test_log(self):
        expr, vars_ = latex_to_sympy(r"\log(x)")
        x = sp.Symbol("x")
        assert sym_equal(expr, sp.log(x))

    def test_exp_simple(self):
        expr, vars_ = latex_to_sympy(r"e^{x}")
        x = sp.Symbol("x")
        assert sym_equal(expr, sp.exp(x))
        assert x in vars_
        assert sp.Symbol("e") not in vars_

    def test_exp_compound(self):
        expr, vars_ = latex_to_sympy(r"e^{x^2 + y^2}")
        x, y = sp.Symbol("x"), sp.Symbol("y")
        assert sym_equal(expr, sp.exp(x**2 + y**2))

    def test_sqrt(self):
        expr, vars_ = latex_to_sympy(r"\sqrt{x}")
        x = sp.Symbol("x")
        assert sym_equal(expr, sp.sqrt(x))

    def test_sqrt_nth(self):
        expr, vars_ = latex_to_sympy(r"\sqrt[3]{x}")
        x = sp.Symbol("x")
        assert sym_equal(expr, x ** sp.Rational(1, 3))

    def test_power(self):
        expr, vars_ = latex_to_sympy(r"x^2")
        x = sp.Symbol("x")
        assert sym_equal(expr, x**2)

    def test_pi(self):
        expr, vars_ = latex_to_sympy(r"\pi")
        assert expr == sp.pi
        assert vars_ == []

    def test_pi_not_in_variables(self):
        """pi sembolik değil, sabit olmalı."""
        expr, vars_ = latex_to_sympy(r"x + \pi")
        assert sp.pi not in vars_
        assert sp.Symbol("pi") not in vars_


# ---------------------------------------------------------------------------
# Subscript değişkenler
# ---------------------------------------------------------------------------

class TestParseSubscript:
    def test_subscript_power(self):
        expr, vars_ = latex_to_sympy(r"x_1^2")
        x1 = sp.Symbol("x1")
        assert sym_equal(expr, x1**2)
        assert vars_ == [x1]

    def test_subscript_sum(self):
        expr, vars_ = latex_to_sympy(r"x_1^2 + x_2^2")
        x1, x2 = sp.Symbol("x1"), sp.Symbol("x2")
        assert sym_equal(expr, x1**2 + x2**2)
        assert vars_ == [x1, x2]

    def test_subscript_product(self):
        expr, vars_ = latex_to_sympy(r"x_1 \cdot x_2")
        x1, x2 = sp.Symbol("x1"), sp.Symbol("x2")
        assert sym_equal(expr, x1 * x2)

    def test_subscript_in_function(self):
        expr, vars_ = latex_to_sympy(r"\cos(x_1)")
        x1 = sp.Symbol("x1")
        assert sym_equal(expr, sp.cos(x1))


# ---------------------------------------------------------------------------
# Kesirli ifadeler
# ---------------------------------------------------------------------------

class TestParseFraction:
    def test_simple_fraction(self):
        expr, vars_ = latex_to_sympy(r"\frac{x}{y}")
        x, y = sp.Symbol("x"), sp.Symbol("y")
        assert sym_equal(expr, x / y)

    def test_rational_function(self):
        expr, vars_ = latex_to_sympy(r"\frac{x^3}{x^2 + y^2}")
        x, y = sp.Symbol("x"), sp.Symbol("y")
        assert sym_equal(expr, x**3 / (x**2 + y**2))

    def test_three_variables(self):
        expr, vars_ = latex_to_sympy(r"\frac{x}{y + z}")
        x, y, z = sp.Symbol("x"), sp.Symbol("y"), sp.Symbol("z")
        assert sym_equal(expr, x / (y + z))
        # Sıra: x < y < z
        assert vars_ == [x, y, z]


# ---------------------------------------------------------------------------
# Büyük bileşik ifadeler
# ---------------------------------------------------------------------------

class TestParseComplex:
    def test_2d_exp_fraction_with_parens(self):
        """e^(x1²+x2²) / (sin(x1)*cos(x2)) — parenli versiyon."""
        expr, vars_ = latex_to_sympy(
            r"\frac{e^{x_1^2+x_2^2}}{\sin(x_1) \cdot \cos(x_2)}"
        )
        x1, x2 = sp.Symbol("x1"), sp.Symbol("x2")
        expected = sp.exp(x1**2 + x2**2) / (sp.sin(x1) * sp.cos(x2))
        assert sym_equal(expr, expected)
        assert vars_ == [x1, x2]

    def test_2d_exp_fraction_no_parens(self):
        """e^(x1²+x2²) / (sin x1 · cos x2) — parensiz versiyon."""
        expr, vars_ = latex_to_sympy(
            r"\frac{e^{x_1^2 + x_2^2}}{\sin x_1 \cdot \cos x_2}"
        )
        x1, x2 = sp.Symbol("x1"), sp.Symbol("x2")
        expected = sp.exp(x1**2 + x2**2) / (sp.sin(x1) * sp.cos(x2))
        assert sym_equal(expr, expected)

    def test_e_not_in_free_symbols(self):
        """e^{...} içinde 'e' sembol olarak kalmamalı."""
        expr, vars_ = latex_to_sympy(r"e^{x}")
        assert sp.Symbol("e") not in expr.free_symbols
        assert sp.Symbol("E") not in expr.free_symbols


# ---------------------------------------------------------------------------
# Değişken tespiti ve sıralama
# ---------------------------------------------------------------------------

class TestVariableDetection:
    def test_single_variable(self):
        _, vars_ = latex_to_sympy(r"\sin(x)")
        assert len(vars_) == 1
        assert vars_[0].name == "x"

    def test_sorted_xy(self):
        _, vars_ = latex_to_sympy(r"x + y")
        assert [v.name for v in vars_] == ["x", "y"]

    def test_sorted_subscripts(self):
        _, vars_ = latex_to_sympy(r"x_1 + x_2 + x_3")
        assert [v.name for v in vars_] == ["x1", "x2", "x3"]

    def test_sorted_mixed(self):
        _, vars_ = latex_to_sympy(r"x + y + z")
        assert [v.name for v in vars_] == ["x", "y", "z"]

    def test_too_many_variables(self):
        """4+ değişken → ValueError."""
        with pytest.raises(ValueError, match="değişken"):
            latex_to_sympy(r"x_1 + x_2 + x_3 + x_4")


# ---------------------------------------------------------------------------
# Hata mesajları
# ---------------------------------------------------------------------------

class TestParseErrors:
    def test_unmatched_brace(self):
        """Kapanmamış süslü parantez → ValueError."""
        with pytest.raises(ValueError):
            latex_to_sympy(r"\frac{x^3}{x^2 + y^2")

    def test_error_message_readable(self):
        """Hata mesajı orijinal string'i içermeli."""
        bad = r"\frac{x^3}{x^2 + y^2"
        with pytest.raises(ValueError, match=r"parse edilemedi"):
            latex_to_sympy(bad)


# ---------------------------------------------------------------------------
# from_latex class method
# ---------------------------------------------------------------------------

class TestFromLatex:
    def test_from_latex_1d(self):
        """from_latex ile 1D sin(x) açılımı."""
        T = TaylorExpansion.from_latex(r"\sin(x)", point=[0], order=5)
        x = sp.Symbol("x")
        expected = x - x**3 / 6 + x**5 / 120
        assert sp.simplify(T.symbolic - expected) == 0

    def test_from_latex_2d(self):
        """from_latex ile 2D kesirli ifade açılımı."""
        T = TaylorExpansion.from_latex(
            r"\frac{e^{x_1^2 + x_2^2}}{\sin(x_1) \cdot \cos(x_2)}",
            point=[1, 0.5],
            order=2,
        )
        assert isinstance(T.symbolic, sp.Expr)
        assert T.gradient is not None
        assert T.hessian is not None

    def test_from_latex_exp(self):
        """from_latex ile e^x açılımı."""
        T = TaylorExpansion.from_latex(r"e^{x}", point=[0], order=3)
        x = sp.Symbol("x")
        expected = 1 + x + x**2 / 2 + x**3 / 6
        assert sp.simplify(T.symbolic - expected) == 0
