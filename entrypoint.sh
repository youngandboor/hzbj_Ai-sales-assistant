#!/bin/bash

# 等待数据库就绪
echo "Waiting for database..."
while ! nc -z test-db-mysql.ns-jj1vgrim.svc 3306; do
  sleep 0.1
done
echo "Database is ready!"


cd backend && source ../venv/bin/activate && python manage.py runserver 0.0.0.0:8000