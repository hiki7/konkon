FROM python:3.11 AS requirements-stage

WORKDIR /tmp
RUN pip install poetry==1.5.0
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./src/main_app/alembic.ini .
COPY ./src/main_app/migrations/ ./migrations/

COPY --from=requirements-stage /tmp/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . .

ENV PYTHONPATH=/code/src

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "src.main_app.main:app"]
#they are exist two commands - CMD and ENTRYPOINT
#ENTRYPOINT is used for appending the commands, whereas the CMD is used for fully replacing commands
