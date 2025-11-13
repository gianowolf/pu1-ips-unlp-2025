from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
import math

def stem_discrete(n, x, title=None):
    plt.figure()
    # Evitar deprecations: usar keywords
    markerline, stemlines, baseline = plt.stem(n, x)
    plt.xlabel("n")
    plt.ylabel("amplitud")
    if title:
        plt.title(title)
    plt.grid(True)
    plt.show()

def plot_mag(s, X, title_prefix: str = ""):
    plt.figure()
    plt.plot(s, np.abs(X))
    plt.xlabel("s (frecuencia normalizada)")
    plt.ylabel("|X(e^{j2πs})|")
    if title_prefix:
        plt.title(f"{title_prefix}: magnitud")
    plt.grid(True)
    plt.show()

def plot_phase(s, X, title_prefix: str = ""):
    # Fase desenrollada
    plt.figure()
    plt.plot(s, np.unwrap(np.angle(X)))
    plt.xlabel("s (frecuencia normalizada)")
    plt.ylabel("∠X(e^{j2πs}) [rad]")
    if title_prefix:
        plt.title(f"{title_prefix}: fase")
    plt.grid(True)
    plt.show()


# -----------------------------
# Utilidades de ejes (tiempo)
# -----------------------------
def _int_xlim_from_n(n: np.ndarray):
    """
    Reglas:
    (1) Mostrar solo enteros en el eje x.
    (2) Si len(n) < 11 -> xlim = [-5, 5].
    (3) Si len(n) >= 11 -> expandir 10% del span a ambos lados.
        Ej.: n va de -5 a 95 -> span=100 -> xlim = [-15, 105].
    """
    n = np.asarray(n, dtype=int)
    if n.size == 0:
        return -5, 5

    if n.size < 11:
        return -5, 5

    n0, n1 = int(n.min()), int(n.max())
    span = max(1, n1 - n0)  # evitar cero
    pad = max(1, int(round(0.10 * span)))
    x0 = n0 - pad
    x1 = n1 + pad
    return x0, x1

def _set_integer_xticks(ax, x0: int, x1: int, max_ticks: int = 21):
    """
    Fija ticks enteros entre x0 y x1. Si el rango es grande, submuestrea para no
    saturar el gráfico.
    """
    if x0 > x1:
        x0, x1 = x1, x0
    rng = x1 - x0
    if rng <= 0:
        ticks = [x0]
    else:
        step = max(1, rng // max(1, max_ticks - 1))
        ticks = np.arange(x0, x1 + 1, step, dtype=int)
    ax.set_xticks(ticks)

# -----------------------------
# Utilidades de ejes (frecuencia)
# -----------------------------
def _round_to_1dec(x):
    return np.round(x * 10) / 10.0

def _freq_ticks_0p1(ax, s):
    """
    Fija marcas cada 0.1 en el eje de frecuencias, cubriendo el intervalo [min(s), max(s)].
    Si s está en [-0.5, 0.5), se obtienen las marcas requeridas: …, -0.3, -0.2, …, 0.3, 0.4, …
    """
    smin = float(np.min(s))
    smax = float(np.max(s))
    a = _round_to_1dec(math.floor(smin * 10) / 10.0)
    b = _round_to_1dec(math.ceil (smax * 10) / 10.0)
    ticks = np.arange(a, b + 1e-9, 0.1)
    ax.set_xticks(ticks)

# -----------------------------
# Grilla tiempo-frecuencia
# -----------------------------
def plot_grid_time_freq(n, x, s, X, title_prefix=""):
    """
    Grafica en una grilla 2x2:
    (1) x[n] en tiempo (ticks enteros y límites según reglas solicitadas).
    (2) X(e^{j2πs}) parte real/imag.
    (3) |X| con ticks de frecuencia a paso 0.1.
    (4) fase(X) desenrollada con ticks de frecuencia a paso 0.1.
    """
    n = np.asarray(n, dtype=int)
    x = np.asarray(x, dtype=float)
    s = np.asarray(s, dtype=float)
    X = np.asarray(X)

    fig, axs = plt.subplots(2, 2, figsize=(11, 7))
    if title_prefix:
        fig.suptitle(title_prefix, fontsize=12)

    # ---- (1) Tiempo ----
    ax_t = axs[0, 0]
    ax_t.stem(n, x)  # Matplotlib >=3.9: no usar 'use_line_collection'
    ax_t.set_title("Tiempo")
    ax_t.set_xlabel("n")
    ax_t.set_ylabel("amplitud")
    ax_t.grid(True)

    # Límites y ticks enteros según reglas
    x0, x1 = _int_xlim_from_n(n)
    ax_t.set_xlim(x0, x1)
    _set_integer_xticks(ax_t, x0, x1)

    # ---- (2) X(e^{j2πs}) Re/Im ----
    ax_reim = axs[0, 1]
    ax_reim.plot(s, np.real(X), label="Re")
    ax_reim.plot(s, np.imag(X), label="Im", linestyle="--")
    ax_reim.set_title("X(e^{j2πs})")
    ax_reim.set_xlabel("s (frecuencia normalizada)")
    ax_reim.grid(True)
    ax_reim.legend()
    _freq_ticks_0p1(ax_reim, s)

    # ---- (3) |X| ----
    ax_mag = axs[1, 0]
    ax_mag.plot(s, np.abs(X))
    ax_mag.set_title("|X(e^{j2πs})|")
    ax_mag.set_xlabel("s (frecuencia normalizada)")
    ax_mag.grid(True)
    _freq_ticks_0p1(ax_mag, s)

    # ---- (4) ∠X ----
    ax_ph = axs[1, 1]
    ax_ph.plot(s, np.unwrap(np.angle(X)))
    ax_ph.set_title("∠X(e^{j2πs}) [rad]")
    ax_ph.set_xlabel("s (frecuencia normalizada)")
    ax_ph.grid(True)
    _freq_ticks_0p1(ax_ph, s)

    plt.tight_layout(rect=(0, 0, 1, 0.95) if title_prefix else None)
    plt.show()