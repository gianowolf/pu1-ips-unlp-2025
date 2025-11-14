#!/usr/bin/env bash
set -e

# Directorio del proyecto (donde está el script)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Ruta al Python del entorno virtual
VENV_DIR=".venv"
PYTHON="$VENV_DIR/bin/python"
PIP="$VENV_DIR/bin/pip"

# Crea el entorno virtual si no existe
if [ ! -x "$PYTHON" ]; then
    echo "Creando entorno virtual en $VENV_DIR ..."
    python3 -m venv "$VENV_DIR"
    "$PYTHON" -m pip install --upgrade pip
    "$PIP" install -r requirements.txt
else
    echo "Entorno virtual encontrado en $VENV_DIR."
fi

# Ejecuta Jupyter Lab usando el Python del entorno
echo "Iniciando Jupyter Lab..."
exec "$PYTHON" -m jupyter lab
