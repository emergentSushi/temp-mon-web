FROM python:3.8-slim-buster
EXPOSE 5000

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app
COPY ./web-start.sh web-start.sh

RUN useradd appuser && chown -R appuser /app
USER appuser

ENV FLASK_APP=app:app
ENTRYPOINT ["./web-start.sh"]
