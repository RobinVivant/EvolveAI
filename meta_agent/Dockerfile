FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir poetry

WORKDIR /app

COPY ../pyproject.toml ../poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]
