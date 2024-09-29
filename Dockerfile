FROM python:3.12-slim-bookworm
EXPOSE 5000

COPY pyproject.toml .
COPY poetry.lock .
RUN python -m pip install poetry
RUN poetry install

#Uncomment to copy your local db file into the docker image for debugging
COPY grid_data.db data/grid_data.db

WORKDIR /app
COPY . /app

RUN useradd appuser && chown -R appuser /app
USER appuser

ENV FLASK_APP=app:app

# This gets overriden in the debug config
ENTRYPOINT ["/bin/bash", "./web-start.sh"]
