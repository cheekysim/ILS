# syntax=docker/dockerfile:1

FROM python:3.11-bullseye

WORKDIR /root/app

COPY requirements.txt requirements.txt
RUN pip3 install -y -r requirements.txt

COPY . .

CMD ["gunicorn"  , "-b", "0.0.0.0:3000", "app:app"]
