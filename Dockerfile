FROM python:3.8
WORKDIR /app
COPY . .
RUN ls -a
ARG PYTHONPATH=./
RUN pip install -r requirements.txt
RUN python -c "from soap_service.storage import db;db.init_db()"
EXPOSE 8000
CMD gunicorn -b :8000 soap_service.server.server