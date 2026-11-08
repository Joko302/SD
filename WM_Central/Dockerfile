# 1. Usar una imagen oficial de Python como base ligera
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# 2. Definir el directorio de trabajo dentro del contenedor
WORKDIR /WM_Central

# 3. Copiar tu archivo de Python desde el ordenador actual al contenedor
COPY requirements.txt /WM_Central/

RUN pip install --no-cache-dir -r requirements.txt

COPY WM_Central.py /WM_Central/

# 4. Indicar el comando que se ejecutará al arrancar el contenedor
CMD ["python", "WM_Central.py"]


EXPOSE 5000
EXPOSE 9092
