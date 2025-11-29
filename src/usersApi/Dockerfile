FROM python:3.13-slim

WORKDIR /microservice

COPY pyproject.toml /microservice/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . /microservice

ENV PYTHONPATH=/microservice

EXPOSE 8000

CMD bash -c "poetry run alembic -c alembic.ini -n usersApi upgrade head && poetry run uvicorn src.usersApi.main:app --host 0.0.0.0 --port 8000 --forwarded-allow-ips='*'"