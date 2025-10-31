FROM python:3.13-slim

WORKDIR /microservice

COPY pyproject.toml /microservice/

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

EXPOSE 8000

ENV PYTHONPATH=/microservice

COPY . /microservice/

CMD bash -c "poetry run alembic upgrade head && poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000"
