FROM python:3.11-slim


WORKDIR /WM_WS_E


COPY requirements.txt /WM_WS_E/

RUN pip install --no-cache-dir -r ../requirements.txt

COPY WM_WS_E.py /WM_WS_E/

EXPOSE 9092
CMD ["python", "WM_WS_E.py","localhost","9092","0.0.0.0","5003"]
