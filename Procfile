release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn core.wsgi --log-file -
web: daphne core.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2