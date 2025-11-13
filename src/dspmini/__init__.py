# src/dspmini/__init__.py
"""
Paquete principal de dspmini.

Expone las funciones públicas de los submódulos:
- core: construcción, alineación, ventana, convolución y TFTD numérica.
- plotting: utilidades de trazado en tiempo y frecuencia.

Autor: Gian Franco Lasala
"""

from __future__ import annotations

# ---- API: núcleo ----
from .core import (
    signal_from_pairs,
    rect_centered,
    apply_window,
    conv_discrete,
    tftd_numeric,
)

# ---- API: gráficos ----
from .plotting import (
    stem_discrete,
    plot_mag,
    plot_phase,
    plot_grid_time_freq,
)

__all__ = [
    # core
    "signal_from_pairs",
    "rect_centered",
    "apply_window",
    "conv_discrete",
    "tftd_numeric",
    # plotting
    "stem_discrete",
    "plot_mag",
    "plot_phase",
    "plot_grid_time_freq",
]
