"""TaylorExpansion: sembolik Taylor serisi açılım motoru."""

from __future__ import annotations

import sympy as sp

from .utils import validate_inputs


class TaylorExpansion:
    """1D–3D fonksiyonlar için 2. mertebe Taylor (Maclaurin) açılımı.

    Args:
        f: Açılım yapılacak SymPy ifadesi.
        variables: Bağımsız değişken sembolleri (uzunluk 1–3).
        point: Açılım noktası. Sayısal veya sembolik liste; None → orijin.
        order: Açılım mertebesi. Şu an sadece 2 desteklenir.
        _simplify: False verilirse son ifadeye sp.simplify uygulanmaz.

    Attributes:
        symbolic: Sembolik Taylor açılım ifadesi.
        gradient: Gradient vektörü (sp.Matrix, n×1).
        hessian: Hessian matrisi (sp.Matrix, n×n).
    """

    def __init__(
        self,
        f: sp.Expr,
        variables: list[sp.Symbol],
        point: list | None = None,
        order: int = 2,
        _simplify: bool = True,
    ) -> None:
        self._f = f
        self._variables = variables
        self._order = order
        self._n = len(variables)
        self._point = validate_inputs(f, variables, point, order)
        self._simplify_flag = _simplify

        # Sembolik hesaplamalar
        self.gradient: sp.Matrix = self._compute_gradient()
        self.hessian: sp.Matrix = self._compute_hessian()
        self.symbolic: sp.Expr = self._compute_taylor()

    # ------------------------------------------------------------------
    # Özel hesap metotları
    # ------------------------------------------------------------------

    def _compute_gradient(self) -> sp.Matrix:
        """Jacobian ile gradient hesaplar (n×1 sütun vektör)."""
        return sp.Matrix([self._f]).jacobian(self._variables).T

    def _compute_hessian(self) -> sp.Matrix:
        """Hessian matrisini hesaplar (n×n)."""
        return sp.hessian(self._f, self._variables)

    def _compute_taylor(self) -> sp.Expr:
        """2. mertebe Taylor açılımını sembolik olarak hesaplar."""
        subs = dict(zip(self._variables, self._point))

        # f(a)
        f_a = self._f.subs(subs)

        # ∇f(a)
        grad_a = self.gradient.subs(subs)

        # H(a)
        hess_a = self.hessian.subs(subs)

        # (x - a) vektörü
        x_minus_a = sp.Matrix(self._variables) - sp.Matrix(self._point)

        # 1. terim: f(a)
        term1 = f_a

        # 2. terim: ∇f(a)ᵀ (x - a)
        term2 = grad_a.dot(x_minus_a)

        # 3. terim: ½ (x-a)ᵀ H(a) (x-a)
        term3 = sp.Rational(1, 2) * (x_minus_a.T * hess_a * x_minus_a)[0]

        taylor = term1 + term2 + term3

        if self._simplify_flag:
            taylor = sp.simplify(taylor)

        return taylor

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def latex(self) -> str:
        """Taylor açılımının LaTeX string temsilini döndürür.

        Returns:
            Dolar işareti içermeyen LaTeX string.
        """
        return sp.latex(self.symbolic)

    def evaluate(self, point_dict: dict[sp.Symbol, float]) -> float:
        """Taylor açılımını verilen noktada sayısal olarak değerlendirir.

        Args:
            point_dict: {sembol: değer} sözlüğü.

        Returns:
            Sayısal float sonuç.
        """
        return float(self.symbolic.subs(point_dict).evalf())

    def to_numeric(self):
        """Orijinal fonksiyonu lambdify ile sayısal fonksiyona çevirir.

        Returns:
            numpy uyumlu callable.
        """
        from .numerical import make_numeric_func
        return make_numeric_func(self._f, self._variables)

    def taylor_to_numeric(self):
        """Taylor yaklaşımını lambdify ile sayısal fonksiyona çevirir.

        Returns:
            numpy uyumlu callable.
        """
        from .numerical import make_numeric_func
        return make_numeric_func(self.symbolic, self._variables)

    def plot(self, **kwargs):
        """Orijinal fonksiyon ve Taylor yaklaşımını görselleştirir.

        Args:
            **kwargs: visualization modülüne iletilen ek parametreler.

        Returns:
            matplotlib Figure veya plotly Figure nesnesi.

        Raises:
            NotImplementedError: 3D (n=3) fonksiyonlar için.
        """
        from .visualization import plot_expansion
        return plot_expansion(self, **kwargs)

    def _repr_latex_(self) -> str:
        """Jupyter'da LaTeX render için."""
        return f"${sp.latex(self.symbolic)}$"

    def __repr__(self) -> str:
        return (
            f"TaylorExpansion(f={self._f}, point={self._point}, "
            f"order={self._order}, n={self._n})"
        )
