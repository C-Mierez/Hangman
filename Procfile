release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn core.wsgi --log-file -
web: daphne core.routing:application --port $PORT --bind 0.0.0.0 -v2
worker: python3 manage.py runworker channel_layer -v2