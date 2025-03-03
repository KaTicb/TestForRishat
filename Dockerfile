FROM python:3.12-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV HOME=/home/worker_user/TestForRishat
ENV APP_HOME=/home/worker_user/TestForRishat/web
RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME/staticfiles
WORKDIR $APP_HOME

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .