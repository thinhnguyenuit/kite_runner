release: python manage.py migrate

web: gunicorn gunicorn kite_runner.wsgi:application
