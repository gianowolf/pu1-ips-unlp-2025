FROM python:3.11

# Evita prompts interactivos y usa backend headless para matplotlib
ENV DEBIAN_FRONTEND=noninteractive
ENV MPLBACKEND=Agg
WORKDIR /app

# Copia requirements e instala dependencias
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto
COPY . /app

# Kernel de Jupyter dentro del contenedor (opcional)
RUN python -m ipykernel install --user --name dsp-mini --display-name "Python (dsp-mini)"

EXPOSE 8888
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser"]