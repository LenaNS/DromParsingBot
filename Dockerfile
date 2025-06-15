FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-dev && \
    pip install --upgrade pip

RUN pip install uv

COPY uv.lock pyproject.toml .

RUN uv sync

COPY src/ src/

CMD ["sh", "-c", "uv run ./src/main.py"]