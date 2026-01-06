FROM python:3.13-slim

WORKDIR /microservice

COPY pyproject.toml /microservice/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . /microservice

ENV PYTHONPATH=/microservice

CMD ["python", "-m", "src.previewWorker.main"]