
db:
    docker compose down || true
    docker compose up -d

db-clone environment_name="production":
    poetry run python development.py database clone --from {{environment_name}}

secrets:
    poetry run python development.py secrets get

upload-secrets:
    poetry run python development.py secrets upload
