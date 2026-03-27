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

    def test_sin_order2(self):
        """sin(x) point=[0], order=2 → x olmalı (2. mertebe açılım)."""
        x = self.x
        T = TaylorExpansion(sp.sin(x), [x], point=[0], order=2)
        assert sym_equal(T.symbolic, x)

    def test_sin_order5(self):
        """sin(x) point=[0], order=5 → x - x³/6 + x⁵/120."""
        x = self.x
        T = TaylorExpansion(sp.sin(x), [x], point=[0], order=5)
        expected = x - x**3 / 6 + x**5 / 120
        assert sym_equal(T.symbolic, expected)

    def test_exp_order3(self):
        """e^x point=[0], order=3 → 1 + x + x²/2 + x³/6."""
        x = self.x
        T = TaylorExpansion(sp.exp(x), [x], point=[0], order=3)
        expected = 1 + x + x**2 / 2 + x**3 / 6
        assert sym_equal(T.symbolic, expected)

    def test_exp_order2(self):
        """e^x point=[0], order=2 → 1 + x + x²/2."""
        x = self.x
        T = TaylorExpansion(sp.exp(x), [x], point=[0], order=2)
        expected = 1 + x + x**2 / 2
        assert sym_equal(T.symbolic, expected)

    def test_high_order_sin(self):
        """sin(x) point=[0], order=50 → hatasız hesaplanmalı."""
        x = self.x
        T = TaylorExpansion(sp.sin(x), [x], point=[0], order=50)
        # Polinom olmalı (O terimi olmamalı)
        assert not T.symbolic.has(sp.Order)
        # Belirli bir noktada değerlendir
        val = float(T.symbolic.subs(x, 0.1).evalf())
        import math
        assert abs(val - math.sin(0.1)) < 1e-10

    def test_symbolic_point(self):
        """e^x point=[a], order=2 → sembolik genel Taylor formülü."""
        x = self.x
        a = sp.Symbol("a")
        T = TaylorExpansion(sp.exp(x), [x], point=[a], order=2)
        # exp(a) + (x-a)*exp(a) + (x-a)²*exp(a)/2
        expected = sp.exp(a) + (x - a) * sp.exp(a) + (x - a)**2 * sp.exp(a) / 2
        assert sym_equal(T.symbolic, expected)

    def test_gradient_none_for_1d(self):
        """1D için gradient None olmalı."""
        x = self.x
        T = TaylorExpansion(sp.exp(x), [x], point=[0], order=2)
        assert T.gradient is None

    def test_hessian_none_for_1d(self):
        """1D için hessian None olmalı."""
        x = self.x
        T = TaylorExpansion(sp.exp(x), [x], point=[0], order=2)
        assert T.hessian is None

    def test_evaluate_1d(self):
        """e^x açılımı, x=0.1 civarında küçük hata vermeli."""
        x = self.x
        T = TaylorExpansion(sp.exp(x), [x], point=[0], order=5)
        val = T.evaluate({x: 0.1})
        import math
        assert abs(val - math.exp(0.1)) < 1e-6

    def test_latex_returns_string(self):
        """latex() string döndürmeli."""
        x = self.x
        T = TaylorExpansion(sp.sin(x), [x], point=[0], order=5)
        assert isinstance(T.latex(), str)
        assert len(T.latex()) > 0

    def test_latex_max_terms(self):
        """latex(max_terms=3) → 3 terim + \\cdots içermeli."""
        x = self.x
        T = TaylorExpansion(sp.exp(x), [x], point=[0], order=20)
        result = T.latex(max_terms=3)
        assert r"\cdots" in result

    def test_latex_full(self):
        """latex(max_terms=None) → \\cdots içermemeli."""
        x = self.x
        T = TaylorExpansion(sp.exp(x), [x], point=[0], order=5)
        result = T.latex(max_terms=None)
        assert r"\cdots" not in result

    def test_repr_latex(self):
        """_repr_latex_() $ işaretiyle başlamalı ve bitmeli."""
        x = self.x
        T = TaylorExpansion(sp.exp(x), [x], point=[0], order=2)
        assert T._repr_latex_().startswith("$")
        assert T._repr_latex_().endswith("$")

    def test_str_truncation(self):
        """__str__ yüksek mertebede '...' içermeli."""
        x = self.x
        T = TaylorExpansion(sp.exp(x), [x], point=[0], order=20)
        s = str(T)
        assert "..." in s


# ---------------------------------------------------------------------------
# 2D testler
# ---------------------------------------------------------------------------

class Test2D:
    def setup_method(self):
        self.x1, self.x2 = sp.symbols("x1 x2")

    def test_exp_symbolic_at_origin(self):
        """e^(x1²+x2²) orijinde açılım → 1 + x1² + x2²."""
        x1, x2 = self.x1, self.x2
        f = sp.exp(x1**2 + x2**2)
        T = TaylorExpansion(f, [x1, x2], point=[0, 0], order=2)
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
        val_t = T.evaluate({x1: 0.01, x2: 0.01})
        val_f = float(f.subs({x1: 0.01, x2: 0.01}).evalf())
        assert abs(val_t - val_f) < 1e-6

    def test_rational_function(self):
        """x1³/(x1²+x2²) point=[1,1] → hatasız hesaplanmalı."""
        x1, x2 = self.x1, self.x2
        f = x1**3 / (x1**2 + x2**2)
        T = TaylorExpansion(f, [x1, x2], point=[1, 1], order=2)
        assert isinstance(T.symbolic, sp.Expr)

    def test_order3_raises(self):
        """2D fonksiyonda order=3 → NotImplementedError."""
        x1, x2 = self.x1, self.x2
        with pytest.raises(NotImplementedError):
            TaylorExpansion(x1 + x2, [x1, x2], point=[0, 0], order=3)


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
    def test_point_none_raises(self):
        """point=None → ValueError."""
        x = sp.Symbol("x")
        with pytest.raises(ValueError, match="Açılım noktası"):
            TaylorExpansion(sp.sin(x), [x], point=None, order=2)

    def test_point_required(self):
        """point argümanı verilmezse → TypeError."""
        x = sp.Symbol("x")
        with pytest.raises(TypeError):
            TaylorExpansion(sp.sin(x), [x])  # type: ignore[call-arg]

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

    def test_order_too_large(self):
        """order=1001 → ValueError."""
        x = sp.Symbol("x")
        with pytest.raises(ValueError, match="1000"):
            TaylorExpansion(sp.exp(x), [x], point=[0], order=1001)

    def test_order_zero_raises(self):
        """order=0 → ValueError."""
        x = sp.Symbol("x")
        with pytest.raises(ValueError):
            TaylorExpansion(sp.sin(x), [x], point=[0], order=0)

    def test_undefined_at_point(self):
        """1/x point=[0] → ValueError (sıfıra bölme)."""
        x = sp.Symbol("x")
        with pytest.raises(ValueError):
            TaylorExpansion(1 / x, [x], point=[0], order=2)
