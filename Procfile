release: python manage.py migrate

web: gunicorn -b 127.0.0.1:8000 gunicorn kite_runner.wsgi:application
