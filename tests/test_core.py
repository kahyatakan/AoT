"""TaylorExpansion çekirdek sınıfı testleri."""

import pytest
import sympy as sp

from aot import TaylorExpansion


# ---------------------------------------------------------------------------
# Yardımcı: sembolik eşitlik kontrolü
# ---------------------------------------------------------------------------

def sym_equal(a: sp.Expr, b: sp.Expr) -> bool:
    """İki sembolik ifadenin eşit olup olmadığını kontrol eder."""
    return sp.simplify(a - b) == 0


# ---------------------------------------------------------------------------
# 1D testler
# ---------------------------------------------------------------------------

class Test1D:
    def setup_method(self):
        self.x = sp.Symbol("x")

    def test_sin_maclaurin_order2(self):
        """sin(x) Maclaurin: x=0 → x (order=2 için 1. ve 2. türev terimi)."""
        x = self.x
        T = TaylorExpansion(sp.sin(x), [x], point=None, order=2)
        # sin(0)=0, cos(0)=1 → T = x + 0 = x
        assert sym_equal(T.symbolic, x)

    def test_exp_maclaurin_order2(self):
        """e^x Maclaurin: x=0 → 1 + x + x²/2."""
        x = self.x
        T = TaylorExpansion(sp.exp(x), [x], point=None, order=2)
        expected = 1 + x + x**2 / 2
        assert sym_equal(T.symbolic, expected)

    def test_point_none_equals_origin(self):
        """point=None orijin [0] ile aynı sonucu vermeli."""
        x = self.x
        T_none = TaylorExpansion(sp.cos(x), [x], point=None, order=2)
        T_zero = TaylorExpansion(sp.cos(x), [x], point=[0], order=2)
        assert sym_equal(T_none.symbolic, T_zero.symbolic)

    def test_gradient_shape_1d(self):
        """Gradient 1×1 matris olmalı."""
        x = self.x
        T = TaylorExpansion(sp.exp(x), [x], point=[0], order=2)
        assert T.gradient.shape == (1, 1)

    def test_hessian_shape_1d(self):
        """Hessian 1×1 matris olmalı."""
        x = self.x
        T = TaylorExpansion(sp.exp(x), [x], point=[0], order=2)
        assert T.hessian.shape == (1, 1)

    def test_evaluate_1d(self):
        """e^x açılımı, x=0.1 civarında küçük hata vermeli."""
        x = self.x
        T = TaylorExpansion(sp.exp(x), [x], point=[0], order=2)
        val = T.evaluate({x: 0.1})
        expected = float(sp.exp(sp.Rational(1, 10)).evalf())
        assert abs(val - expected) < 1e-3

    def test_latex_returns_string(self):
        """latex() string döndürmeli."""
        x = self.x
        T = TaylorExpansion(sp.sin(x), [x], point=[0], order=2)
        assert isinstance(T.latex(), str)
        assert len(T.latex()) > 0

    def test_repr_latex(self):
        """_repr_latex_() $ işaretiyle başlamalı."""
        x = self.x
        T = TaylorExpansion(sp.exp(x), [x], point=[0], order=2)
        assert T._repr_latex_().startswith("$")
        assert T._repr_latex_().endswith("$")


# ---------------------------------------------------------------------------
# 2D testler
# ---------------------------------------------------------------------------

class Test2D:
    def setup_method(self):
        self.x1, self.x2 = sp.symbols("x1 x2")

    def test_exp_symbolic_at_origin(self):
        """e^(x1²+x2²) orijinde açılım — mevcut aot.py davranışı korunmalı."""
        x1, x2 = self.x1, self.x2
        f = sp.exp(x1**2 + x2**2)
        T = TaylorExpansion(f, [x1, x2], point=[0, 0], order=2)
        # Orijinde: f(0)=1, gradient(0)=0, hessian(0)=2I
        # T = 1 + x1² + x2²
        expected = 1 + x1**2 + x2**2
        assert sym_equal(T.symbolic, expected)

    def test_gradient_shape_2d(self):
        """Gradient 2×1 matris olmalı."""
        x1, x2 = self.x1, self.x2
        T = TaylorExpansion(x1**2 + x2**2, [x1, x2], point=[0, 0], order=2)
        assert T.gradient.shape == (2, 1)

    def test_hessian_shape_2d(self):
        """Hessian 2×2 matris olmalı."""
        x1, x2 = self.x1, self.x2
        T = TaylorExpansion(x1**2 + x2**2, [x1, x2], point=[0, 0], order=2)
        assert T.hessian.shape == (2, 2)

    def test_quadratic_equals_itself(self):
        """2. dereceli polinom kendine eşit Taylor açılımı vermelidir."""
        x1, x2 = self.x1, self.x2
        f = 3*x1**2 + 2*x1*x2 + x2**2 + 5*x1 - x2 + 7
        T = TaylorExpansion(f, [x1, x2], point=[0, 0], order=2)
        assert sym_equal(T.symbolic, f)

    def test_numerical_accuracy_2d(self):
        """Açılım noktası civarında |f - T| < 1e-6 olmalı."""
        x1, x2 = self.x1, self.x2
        f = sp.exp(x1**2 + x2**2)
        T = TaylorExpansion(f, [x1, x2], point=[0, 0], order=2)
        # Orijin yakınında küçük bir nokta test et
        val_t = T.evaluate({x1: 0.01, x2: 0.01})
        val_f = float(f.subs({x1: 0.01, x2: 0.01}).evalf())
        assert abs(val_t - val_f) < 1e-6


# ---------------------------------------------------------------------------
# 3D testler
# ---------------------------------------------------------------------------

class Test3D:
    def setup_method(self):
        self.x1, self.x2, self.x3 = sp.symbols("x1 x2 x3")

    def test_polynomial_3d_equals_itself(self):
        """3D 2. dereceli polinom kendine eşit açılım vermeli."""
        x1, x2, x3 = self.x1, self.x2, self.x3
        f = x1**2 + x2**2 + x3**2 + x1*x2 + x2*x3
        T = TaylorExpansion(f, [x1, x2, x3], point=[0, 0, 0], order=2)
        assert sym_equal(T.symbolic, f)

    def test_gradient_shape_3d(self):
        """Gradient 3×1 matris olmalı."""
        x1, x2, x3 = self.x1, self.x2, self.x3
        T = TaylorExpansion(x1 + x2 + x3, [x1, x2, x3], point=[0, 0, 0], order=2)
        assert T.gradient.shape == (3, 1)

    def test_hessian_shape_3d(self):
        """Hessian 3×3 matris olmalı."""
        x1, x2, x3 = self.x1, self.x2, self.x3
        T = TaylorExpansion(x1 + x2 + x3, [x1, x2, x3], point=[0, 0, 0], order=2)
        assert T.hessian.shape == (3, 3)


# ---------------------------------------------------------------------------
# Hata testleri
# ---------------------------------------------------------------------------

class TestErrors:
    def test_invalid_order(self):
        """order=3 → NotImplementedError."""
        x = sp.Symbol("x")
        with pytest.raises(NotImplementedError):
            TaylorExpansion(sp.sin(x), [x], point=[0], order=3)

    def test_invalid_dimension_too_many(self):
        """4 değişken → ValueError."""
        syms = sp.symbols("x1 x2 x3 x4")
        with pytest.raises(ValueError):
            TaylorExpansion(syms[0], list(syms), point=[0, 0, 0, 0], order=2)

    def test_invalid_dimension_zero(self):
        """0 değişken → ValueError."""
        x = sp.Symbol("x")
        with pytest.raises(ValueError):
            TaylorExpansion(x, [], point=[], order=2)

    def test_point_length_mismatch(self):
        """point uzunluğu variables ile uyuşmuyorsa ValueError."""
        x1, x2 = sp.symbols("x1 x2")
        with pytest.raises(ValueError):
            TaylorExpansion(x1 + x2, [x1, x2], point=[0], order=2)
