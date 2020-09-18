web: gunicorn backend.wsgi --log-file -
worker: celery -A backend worker -B --loglevel=info