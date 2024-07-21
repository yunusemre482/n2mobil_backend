#!/bin/bash
echo "Creating Migrations..."
python manage.py makemigrations

echo "===================================="

echo "Starting Migrations..."
python manage.py migrate
echo "===================================="

echo "Starting Server..."
echo "Server Started... You can now access the server at http://localhost:8000/api/v1/"
python manage.py runserver localhost:8000



