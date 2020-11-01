FROM  python:3.8-slim-buster

LABEL maintainer=""

RUN  apt-get update -y && apt-get  install -y redis-server

COPY app /app

RUN pip install --no-cache-dir -r /app/requirements.txt

RUN chmod +x /app/entrypoint.sh
WORKDIR /app

ENTRYPOINT ["/app/entrypoint.sh"]
