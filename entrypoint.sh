#! /bin/bash


docker exec -it container_id python manage.py createsuperuser
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py loaddata re.json--no-input
python manage.py loaddata ra.json--no-input
python manage.py collectstatic --no-input
python manage.py runserver 0.0.0.0:8000


