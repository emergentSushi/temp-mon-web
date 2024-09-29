FROM python:3.12-slim

EXPOSE 5002

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

RUN poetry config virtualenvs.create true && poetry config virtualenvs.in-project true

WORKDIR /app
COPY . /app

COPY poetry.lock pyproject.toml ./
RUN poetry install

RUN poetry run black . \
	&& poetry run mypy . \
	&& poetry run flake8 . \
	&& poetry run isort --check-only .

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:5002", "app:app"]
