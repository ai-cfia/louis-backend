FROM python:3.11.3

WORKDIR /code

COPY requirements.prod.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY louis ./louis
COPY app.py app.py
COPY static static
COPY gunicorn_config.py gunicorn_config.py
COPY .env.prod .env

EXPOSE 5000

ENTRYPOINT ["gunicorn", "-c", "gunicorn_config.py", "app:app"]