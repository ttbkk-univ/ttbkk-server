FROM python:3.9.5

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./src /app/src
COPY manage.py /app/manage.py
COPY env.py /app/env.py

RUN mkdir -p /app/statics
RUN python3 manage.py collectstatic --noinput
ENTRYPOINT ["gunicorn", "src.ttbkk.wsgi", "--bind", "0.0.0.0:8000"]
