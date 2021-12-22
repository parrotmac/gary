FROM python:3.10

EXPOSE 8000

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.4

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . ./

# Uncomment to monkey-patch sendgrid library to use ngrok tunnel
# RUN sed -i 's/https:\/\/api.sendgrid.com/https:\/\/yogurt.ngrok.io/g' /usr/local/lib/python3.10/site-packages/sendgrid/sendgrid.py

CMD ["/app/scripts/server"]