# 1. Usar una imagen oficial de Python como base ligera
FROM python:3.11-slim

# 2. Definir el directorio de trabajo dentro del contenedor
WORKDIR /WM_WS_M

# 3. Copiar tu archivo de Python desde el ordenador actual al contenedor
COPY ../requirements.txt /WM_WS_M/

RUN pip install --no-cache-dir -r ../requirements.txt

COPY WM_WS_M.py /WM_WS_M/

# 4. Indicar el comando que se ejecutará al arrancar el contenedor
EXPOSE 5000

CMD ["python", "WM_WS_M.py"]
