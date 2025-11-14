# PU1 – IPS 2025

Estructura principal:

- `notebooks/`
  - `01_Ejercicio_1.ipynb`
  - `02_Ejercicio_2.ipynb`
- `data/`
  - `senial_14253.csv`
  - `ha.csv`
  - `audio.wav`

## 1. Ejecución en Python (sin Docker)

### 1.1. Requisitos

- Python 3.11

### 1.2. Creación de entorno virtual

En Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

En Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 1.3. Ejecución de Jupyter Lab

Con el entorno virtual activado:

```bash
jupyter lab
```

Se abrirá una URL en el navegador (o se mostrará una URL con un `token` en la terminal).
Dentro de Jupyter Lab, abrir los notebooks del directorio `notebooks/`:

* `01_Ejercicio_1.ipynb`
* `02_Ejercicio_2.ipynb`

---

## 2. Uso con Docker

Esta opción es útil si no se desea instalar Python ni dependencias en el sistema.

### 2.1. Requisitos

* Docker
* Docker Compose (v2 o superior, generalmente incluido en Docker Desktop)

### 2.2. Construcción de la imagen

Desde el directorio raíz del proyecto:

```bash
docker compose build
```

### 2.3. Ejecución de Jupyter Lab

```bash
docker compose up
```

En la terminal aparecerá una línea similar a:

```text
http://127.0.0.1:8888/lab?token=<TOKEN>
```

Copiar y pegar esa URL en el navegador.
Los notebooks se encuentran en el directorio `notebooks/` dentro de Jupyter Lab.

Para detener el servicio:

```bash
docker compose down
```
`