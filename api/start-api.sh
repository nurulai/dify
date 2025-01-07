poetry install

echo "PORT: $PORT"
poetry run flask run --host 0.0.0.0 --port=$PORT --debug