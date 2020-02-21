FROM python:3.8
WORKDIR /app
COPY . .
RUN ls -a
ARG PYTHONPATH=./
RUN pip install -r requirements.txt
RUN python soap_service/storage/init_db.py
EXPOSE 8000
CMD gunicorn -b :8000 soap_service.server.server