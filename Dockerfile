FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./traefik_prism ./

CMD [ "python", "/app/traefik_prism.py" ]