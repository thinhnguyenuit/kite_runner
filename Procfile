release: python manage.py migrate

web: gunicorn gunicorn posthog.wsgi:application
