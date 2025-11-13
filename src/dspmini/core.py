from __future__ import annotations
import numpy as np

def signal_from_pairs(pairs):
    """
    Construye una señal discreta a partir de pares (n, valor).
    Devuelve (n, x) con soporte entero contiguo; rellena con ceros si faltan índices.
    """
    if len(pairs) == 0:
        return np.array([0], dtype=int), np.array([0.0], dtype=float)
    pairs = sorted(pairs, key=lambda p: p[0])
    ns = np.array([int(p[0]) for p in pairs], dtype=int)
    vals = {int(n): float(v) for n, v in pairs}
    n_min, n_max = int(ns.min()), int(ns.max())
    n = np.arange(n_min, n_max + 1, dtype=int)
    x = np.array([vals.get(int(k), 0.0) for k in n], dtype=float)
    return n, x

def rect_centered(N: int):
    """
    Ventana 'cajón' centrada en cero de ancho N (N impar).
    Devuelve (n, w) con n = -N//2 .. +N//2 y w[n]=1.
    """
    if N % 2 == 0:
        raise ValueError("N debe ser impar para centrar en cero.")
    half = N // 2
    n = np.arange(-half, half + 1, dtype=int)
    w = np.ones_like(n, dtype=float)
    return n, w

def _align_on_grid(n_a, a, n_b, b):
    """Alinea dos señales en una misma grilla entera y devuelve (grid, a_grid, b_grid)."""
    gmin = int(min(n_a.min(), n_b.min()))
    gmax = int(max(n_a.max(), n_b.max()))
    grid = np.arange(gmin, gmax + 1, dtype=int)
    ag = np.zeros_like(grid, dtype=float)
    bg = np.zeros_like(grid, dtype=float)
    ag[(n_a - gmin)] = a
    bg[(n_b - gmin)] = b
    return grid, ag, bg

def apply_window(n, x, N: int | None = None):
    """
    Multiplica x[n] por un cajón centrado en cero de ancho N (si N no es None).
    Devuelve (n_eff, x_eff) recortando ceros en los extremos.
    """
    if N is None:
        return n.copy(), x.copy()
    wn, w = rect_centered(N)
    grid, xg, wg = _align_on_grid(n, x, wn, w)
    yg = xg * wg
    nz = np.nonzero(np.abs(yg) > 0)[0]
    if nz.size == 0:
        return np.array([0], dtype=int), np.array([0.0], dtype=float)
    gmin, gmax = int(nz.min()), int(nz.max())
    return grid[gmin:gmax + 1], yg[gmin:gmax + 1]

def conv_discrete(nx, x, nh, h):
    """
    Convolución lineal de dos señales definidas en soportes enteros (nx, x) y (nh, h).
    Devuelve (ny, y) con soporte exacto: ny_min = nx0 + nh0.
    """
    y = np.convolve(x, h, mode="full")
    ny_min = int(nx[0] + nh[0])
    ny = np.arange(ny_min, ny_min + y.size, dtype=int)
    return ny, y

def tftd_numeric(n, x, s=None, N_window: int | None = None):
    """
    X(e^{j2πs}) ≈ ∑_n [x[n]·w[n]] e^{-j2π s n}
    - n, x: soporte y amplitud de la señal
    - s: rejilla de frecuencias normalizadas s ∈ [-0.5, 0.5). Si None, usa 2048 puntos.
    - N_window: ancho del cajón centrado en cero (impar). Si None, no se aplica ventana.
    Devuelve (s, X) con X complejo.
    """
    n_eff, x_eff = apply_window(n, x, N_window)
    if s is None:
        s = np.linspace(-0.5, 0.5, 2048, endpoint=False)
    expo = np.exp(-1j * 2 * np.pi * np.outer(s, n_eff))  # shape (len(s), len(n_eff))
    X = expo @ x_eff.astype(complex)
    return s, X
