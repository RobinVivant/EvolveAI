FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir poetry

WORKDIR /app/meta_agent

COPY pyproject.toml poetry.lock* /app/

# Add this line to copy requirements.txt
COPY requirements.txt /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Add this line to install requirements
RUN pip install -r /app/requirements.txt

COPY . /app/

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["poetry", "run", "flask", "run", "--port=5000"]
