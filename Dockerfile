FROM python:3.8-slim-buster
EXPOSE 5000
EXPOSE 8000

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

RUN useradd appuser && chown -R appuser /app
USER appuser

ENV FLASK_APP=app:app
RUN ["chmod", "+x", "./web-start.sh"]
ENTRYPOINT ["/bin/bash", "./web-start.sh"]
