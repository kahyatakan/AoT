"""Görselleştirme testleri."""

import pytest
import sympy as sp

from aot import TaylorExpansion


class TestVisualization:
    def setup_method(self):
        self.x = sp.Symbol("x")
        self.x1, self.x2 = sp.symbols("x1 x2")
        self.x1_, self.x2_, self.x3_ = sp.symbols("x1 x2 x3")

    def test_plot_1d_returns_figure(self):
        """1D plot() matplotlib Figure döndürmeli."""
        import matplotlib.pyplot as plt
        x = self.x
        T = TaylorExpansion(sp.sin(x), [x], point=[0], order=2)
        fig = T.plot()
        assert isinstance(fig, plt.Figure)
        plt.close("all")

    def test_plot_2d_returns_figure_matplotlib(self):
        """2D plot() matplotlib Figure döndürmeli (backend='matplotlib')."""
        import matplotlib.pyplot as plt
        x1, x2 = self.x1, self.x2
        T = TaylorExpansion(x1**2 + x2**2, [x1, x2], point=[0, 0], order=2)
        fig = T.plot(backend="matplotlib")
        assert isinstance(fig, plt.Figure)
        plt.close("all")

    def test_plot_3d_raises(self):
        """3D fonksiyon için plot() NotImplementedError fırlatmalı."""
        x1, x2, x3 = self.x1_, self.x2_, self.x3_
        T = TaylorExpansion(x1 + x2 + x3, [x1, x2, x3], point=[0, 0, 0], order=2)
        with pytest.raises(NotImplementedError):
            T.plot()
