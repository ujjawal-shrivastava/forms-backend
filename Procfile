web: gunicorn backend.wsgi --log-file -
celery -A backend.celery worker -B --loglevel=info