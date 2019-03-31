#FROM python:3.7.0-alpine3.8
FROM python:3.7.3-stretch

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py

CMD flask run --host=0.0.0.0

