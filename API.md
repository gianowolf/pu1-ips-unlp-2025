# Resumen de API `dspmini`

## Archivos y Funciones

### `signals.py`

dataclass `Signal(n: np.ndarray, x: np.ndarray, name: str | None = None)`

functions:
- `delta(n0=0, n_range=(-K, K)) -> Signal`
- `u(n_range) -> Signal`: Escalón u[n] con u[0]=1
- `rectN(N, centered=False) -> Signal`: cajón de largo N
- `triN(N, centered=False) -> Signal `: triángulo discreto de largo N
- `from_callable(f, n_range, name=None) -> Signal`
- `from_csv(path, n_col="n", x_col="x", name=None) -> Signal`

### `transforms.py`
  - `tftd(x, n, s_grid, K) -> np.ndarray`: X(e^{j2πs}) = ∑_{n=-∞}^{∞} x[n] e^{-j2π s n}, aproximada con rectN(K)
  - `itftd(X, s_grid, n, K) -> np.ndarray`: x[n] ≈ ∫_{-0.5}^{0.5} X(e^{j2πs}) e^{j2π s n} ds, suma rectangular

### `systems.py`

dataclass `SystemSLID(name: str, b: np.ndarray, a: np.ndarray)`

- `impulse_response(system, n_len) -> Signal`: h[0..n_len-1]
- `freq_response_TFTD(system, s_grid, K) -> (np.ndarray, np.ndarray) (s_grid, H(e^{j2πs}))`: vía TFTD numérica de h[n] ventana rectN(K)
- `filter_by_diff_eq(system, signal: Signal) -> Signal`
- `filter_by_conv(system, signal: Signal, h_len) -> Signal` conv con h

### `plots.py`
  - `plot_time(n, x, title="")`
  - `plot_mag_phase(s, X, title="")`

## Guía de Ejecución (Ubuntu)

### Requisitos

- Python 3.11+ o Docker

### Instalación local

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install numpy scipy matplotlib
```

### Ejecución de prueba

```
PYTHONPATH=./src python examples.py
```

### Resultados esperados (resumen)

- TFTD{δ[n]} ≈ constante en módulo.

- TFTD{rectN} tipo sinc.

- Sistema boxN (FIR):

H(e^{j2πs}) numérica de boxN cercana a la forma analítica: |H| ≈ |sin(πNs)/(N sin(πs))|.
