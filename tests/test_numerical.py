"""Sayısal değerlendirme testleri."""

import numpy as np
import pytest
import sympy as sp

from aot import TaylorExpansion


class TestNumerical:
    def setup_method(self):
        self.x = sp.Symbol("x")
        self.x1, self.x2 = sp.symbols("x1 x2")

    def test_to_numeric_1d_scalar(self):
        """1D sayısal fonksiyon skaler girdi kabul etmeli."""
        x = self.x
        T = TaylorExpansion(sp.exp(x), [x], point=[0], order=2)
        f_num = T.to_numeric()
        assert abs(f_num(0.0) - 1.0) < 1e-10

    def test_to_numeric_1d_array(self):
        """1D sayısal fonksiyon numpy array girdi kabul etmeli."""
        x = self.x
        T = TaylorExpansion(sp.exp(x), [x], point=[0], order=2)
        f_num = T.to_numeric()
        x_arr = np.array([0.0, 1.0, 2.0])
        result = f_num(x_arr)
        expected = np.exp(x_arr)
        np.testing.assert_allclose(result, expected, rtol=1e-5)

    def test_taylor_to_numeric_1d(self):
        """Taylor sayısal fonksiyon orijinden yakında doğru sonuç vermeli."""
        x = self.x
        T = TaylorExpansion(sp.exp(x), [x], point=[0], order=2)
        t_num = T.taylor_to_numeric()
        # T(0.1) ≈ 1 + 0.1 + 0.005 = 1.105
        assert abs(t_num(0.1) - 1.105) < 1e-10

    def test_to_numeric_2d_meshgrid(self):
        """2D sayısal fonksiyon meshgrid ile çalışmalı (plot için kritik)."""
        x1, x2 = self.x1, self.x2
        f = x1**2 + x2**2
        T = TaylorExpansion(f, [x1, x2], point=[0, 0], order=2)
        f_num = T.to_numeric()

        x1_arr = np.linspace(-1, 1, 10)
        x2_arr = np.linspace(-1, 1, 10)
        X1, X2 = np.meshgrid(x1_arr, x2_arr)

        Z = f_num(X1, X2)
        assert Z.shape == X1.shape

    def test_lambdify_meshgrid_accuracy(self):
        """Meshgrid üzerinde sayısal değerler doğru olmalı."""
        x1, x2 = self.x1, self.x2
        f = x1**2 + x2**2
        T = TaylorExpansion(f, [x1, x2], point=[0, 0], order=2)
        f_num = T.to_numeric()

        X1, X2 = np.meshgrid([1.0, 2.0], [3.0, 4.0])
        Z = f_num(X1, X2)
        expected = X1**2 + X2**2
        np.testing.assert_allclose(Z, expected)

    def test_taylor_to_numeric_2d_accuracy(self):
        """2D Taylor sayısal değeri açılım noktası yakınında hassas olmalı."""
        x1, x2 = self.x1, self.x2
        f = sp.exp(x1**2 + x2**2)
        T = TaylorExpansion(f, [x1, x2], point=[0, 0], order=2)
        t_num = T.taylor_to_numeric()

        # Orijin yakınında: |T(0.01, 0.01) - f(0.01, 0.01)| < 1e-6
        val_t = t_num(0.01, 0.01)
        val_f = float(f.subs({x1: 0.01, x2: 0.01}).evalf())
        assert abs(val_t - val_f) < 1e-6
