FROM python:3.9.5

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./src/apps/brand /app/src/apps/brand
COPY ./src/apps/hashtag /app/src/apps/hashtag
COPY ./src/apps/place /app/src/apps/place
COPY ./src/apps/user /app/src/apps/user
COPY ./src/ttbkk /app/src/ttbkk
COPY manage.py /app/manage.py
COPY env.py /app/env.py

RUN mkdir -p /app/statics
RUN python3 manage.py collectstatic --noinput
ENTRYPOINT ["gunicorn", "src.ttbkk.wsgi", "--bind", "0.0.0.0:8000"]
