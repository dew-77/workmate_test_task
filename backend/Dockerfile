FROM python:3.12-slim

ENV POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    PATH="/root/.local/bin:$PATH"

RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python - && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN poetry --version

WORKDIR /app

COPY . .

RUN poetry install --no-root --no-dev

ENV PYTHONPATH=/app

CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi"]
