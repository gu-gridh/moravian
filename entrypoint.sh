#!/bin/sh

# Wait for the database to be ready
while ! nc -z "$HOST" "$PORT"; do
  sleep 1
done

echo "Postgres ready. Do migrations and load data..."
python moravian/moravian/manage.py migrate
python moravian/moravian/manage.py makemigrations pages
python moravian/moravian/manage.py migrate pages
python moravian/moravian/manage.py makemigrations trxnviewer
python moravian/moravian/manage.py migrate trxnviewer

echo "Clean up data and load sample data... (DON'T USE IN PRODUCTION!!)"
python moravian/moravian/manage.py flush --no-input
# Create superuser if it doesn't exist
echo "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='moravian_admin').exists():
    User.objects.create_superuser('moravian_admin', 'admin@example.com', 'adminpass_test')
" | python moravian/moravian/manage.py shell

python moravian/moravian/manage.py loaddata sample_fixture
python moravian/moravian/manage.py collectstatic --noinput

exec python moravian/moravian/manage.py runserver 0.0.0.0:8000