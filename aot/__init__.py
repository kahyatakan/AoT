"""AOT — Anvil of Taylor: Taylor serisi açılım paketi."""

from .core import TaylorExpansion
from .numerical import make_numeric_func
from .visualization import plot_expansion

__all__ = ["TaylorExpansion", "make_numeric_func", "plot_expansion"]
__version__ = "0.2.0"
