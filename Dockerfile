FROM python:3.10-buster

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python - --version=1.2.2

WORKDIR /app

COPY poetry.lock pyproject.toml ./
ENV PATH="/root/.local/bin:${PATH}"
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . ./

CMD ["/app/scripts/server"]
