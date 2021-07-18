FROM python:3.9.5

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./brand /app/brand
COPY ./hashtag /app/hashtag
COPY ./place /app/place
COPY ./tbkmap /app/tbkmap
COPY ./user /app/user
COPY manage.py /app/manage.py
COPY env.py /app/env.py


ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
