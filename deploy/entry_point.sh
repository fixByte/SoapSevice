#!/usr/bin/bash

python soap_service/storage/init_db.py
gunicorn -b :8000 soap_service.server.server

exec "$@"