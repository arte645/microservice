FROM python:3.13-slim

WORKDIR /microservice

COPY pyproject.toml /microservice/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . /microservice

EXPOSE 8000

CMD bash -c "poetry run uvicorn src.authApi.main:app --host 0.0.0.0 --port 9000 --forwarded-allow-ips='*'"