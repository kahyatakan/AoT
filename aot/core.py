"""TaylorExpansion: sembolik Taylor serisi açılım motoru."""

from __future__ import annotations

import sympy as sp

from .utils import validate_inputs


class TaylorExpansion:
    """1D–3D fonksiyonlar için Taylor serisi açılımı.

    1D fonksiyonlarda order=1..1000 desteklenir (sp.series ile).
    2D/3D fonksiyonlarda şimdilik yalnızca order=2 desteklenir (gradient + Hessian).

    Args:
        f: Açılım yapılacak SymPy ifadesi.
        variables: Bağımsız değişken sembolleri (uzunluk 1–3).
        point: Açılım noktası. Sayısal veya sembolik liste; None yasaktır.
        order: Açılım mertebesi. 1D'de 1–1000, çok değişkenlide yalnızca 2.
        _simplify: False verilirse son ifadeye sp.simplify uygulanmaz.

    Attributes:
        symbolic: Sembolik Taylor açılım ifadesi.
        gradient: Gradient vektörü (sp.Matrix, n×1). Yalnızca n>=2.
        hessian: Hessian matrisi (sp.Matrix, n×n). Yalnızca n>=2.
    """

    def __init__(
        self,
        f: sp.Expr,
        variables: list[sp.Symbol],
        point: list,
        order: int = 2,
        _simplify: bool = True,
    ) -> None:
        self._f = f
        self._variables = variables
        self._order = order
        self._n = len(variables)
        self._point = validate_inputs(f, variables, point, order)
        self._simplify_flag = _simplify

        # Sembolik hesaplamalar — 1D ve çok değişkenli ayrı yollar
        if self._n == 1:
            self.gradient: sp.Matrix | None = None
            self.hessian: sp.Matrix | None = None
            self.symbolic: sp.Expr = self._compute_1d()
        else:
            self.gradient = self._compute_gradient()
            self.hessian = self._compute_hessian()
            self.symbolic = self._compute_nd()

    # ------------------------------------------------------------------
    # Hesap metotları — 1D
    # ------------------------------------------------------------------

    def _compute_1d(self) -> sp.Expr:
        """sp.series() ile 1D Taylor açılımı hesaplar."""
        var = self._variables[0]
        a = self._point[0]

        try:
            taylor_expr = sp.series(self._f, var, a, n=self._order + 1)
            result = taylor_expr.removeO()
        except (ZeroDivisionError, OverflowError, ValueError) as exc:
            raise ValueError(
                f"f fonksiyonu açılım noktası a=[{a}]'da açılamıyor: {exc}. "
                "Farklı bir açılım noktası deneyin."
            ) from exc

        # Sonsuzluk / NaN kontrolü
        if result.has(sp.oo) or result.has(sp.nan) or result.has(sp.zoo):
            raise ValueError(
                f"f fonksiyonu açılım noktası a=[{a}]'da tanımsızdır "
                "(sıfıra bölme veya sonsuzluk). Farklı bir açılım noktası deneyin."
            )

        if self._simplify_flag:
            result = sp.simplify(result)

        return result

    # ------------------------------------------------------------------
    # Hesap metotları — çok değişkenli (n >= 2)
    # ------------------------------------------------------------------

    def _compute_gradient(self) -> sp.Matrix:
        """Jacobian ile gradient hesaplar (n×1 sütun vektör)."""
        return sp.Matrix([self._f]).jacobian(self._variables).T

    def _compute_hessian(self) -> sp.Matrix:
        """Hessian matrisini hesaplar (n×n)."""
        return sp.hessian(self._f, self._variables)

    def _compute_nd(self) -> sp.Expr:
        """2. mertebe çok değişkenli Taylor açılımını hesaplar."""
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

        # Sonsuzluk kontrolü
        if taylor.has(sp.oo) or taylor.has(sp.nan) or taylor.has(sp.zoo):
            raise ValueError(
                f"f fonksiyonu açılım noktası a={[str(p) for p in self._point]}'da "
                "tanımsızdır (sıfıra bölme veya sonsuzluk). "
                "Farklı bir açılım noktası deneyin."
            )

        if self._simplify_flag:
            taylor = sp.simplify(taylor)

        return taylor

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def latex(self, max_terms: int | None = 10) -> str:
        """Taylor açılımının LaTeX string temsilini döndürür.

        Args:
            max_terms: Gösterilecek maksimum terim sayısı.
                None verilirse tüm terimler gösterilir.
                Varsayılan: 10.

        Returns:
            Dolar işareti içermeyen LaTeX string.
        """
        return self._to_latex_truncated(max_terms)

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

    # ------------------------------------------------------------------
    # Yardımcı metotlar
    # ------------------------------------------------------------------

    def _to_latex_truncated(self, max_terms: int | None) -> str:
        """Sembolik ifadeyi max_terms kadar terim LaTeX olarak verir."""
        expr = self.symbolic

        if max_terms is None:
            return sp.latex(expr)

        # Terimleri sırala (kuvvet sırasına göre)
        terms = expr.as_ordered_terms()

        if len(terms) <= max_terms:
            return sp.latex(expr)

        # İlk max_terms terimi al, kalanını … ile göster
        shown = sp.Add(*terms[:max_terms])
        return sp.latex(shown) + r" + \cdots"

    def _to_str_truncated(self, max_terms: int = 5) -> str:
        """Sembolik ifadeyi max_terms kadar terim str olarak verir."""
        expr = self.symbolic
        terms = expr.as_ordered_terms()

        if len(terms) <= max_terms:
            return str(expr)

        shown = sp.Add(*terms[:max_terms])
        return str(shown) + " + ..."

    def _repr_latex_(self) -> str:
        """Jupyter'da LaTeX render için (ilk 10 terim)."""
        return f"${self._to_latex_truncated(10)}$"

    def __str__(self) -> str:
        return self._to_str_truncated(5)

    def __repr__(self) -> str:
        return (
            f"TaylorExpansion(f={self._f}, point={self._point}, "
            f"order={self._order}, n={self._n})"
        )
