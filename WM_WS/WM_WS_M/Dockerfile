# 1. Usar una imagen oficial de Python como base ligera
FROM python:3.11-slim

# 2. Definir el directorio de trabajo dentro del contenedor
WORKDIR /WM_WS_M

COPY WM_WS_M.py /WM_WS_M/


EXPOSE 5000

CMD ["python", "WM_WS_M.py","5001","0.0.0.0","5000","12345678"]
