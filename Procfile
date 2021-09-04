release: python manage.py migrate --setting config.settings.production
web: gunicorn config.wsgi --env DJANGO_SETTINGS_MODULE=config.settings.production
