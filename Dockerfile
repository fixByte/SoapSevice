FROM python:3.8-slim
RUN apt-get -qq update
RUN apt-get install -y postgresql-client --show-progress
WORKDIR /app
COPY . .
ENV PYTHONPATH=./
RUN pip install -r requirements.txt