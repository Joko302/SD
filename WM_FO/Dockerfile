# 1. Usar una imagen oficial de Python como base ligera
FROM python:3.11-slim

# 2. Definir el directorio de trabajo dentro del contenedor
WORKDIR /WM_FO

# 3. Copiar tu archivo de Python desde el ordenador actual al contenedor
COPY ../requirements.txt /WM_FO/

RUN pip install --no-cache-dir -r ../requirements.txt

COPY WM_FO.py /WM_FO/

# 4. Indicar el comando que se ejecutará al arrancar el contenedor
EXPOSE 9092

CMD ["python", "WM_FO.py"]
