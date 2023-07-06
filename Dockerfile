FROM python:3.11.3

WORKDIR /code

# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/run/helloworld/Dockerfile

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

COPY requirements.prod.txt ./requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY louis ./louis
COPY app.py app.py
COPY static static

ENTRYPOINT gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 --forwarded-allow-ips "*" app:app