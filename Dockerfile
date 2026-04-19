FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY knowledge/ ./knowledge/

RUN uv sync --frozen

RUN mkdir -p inputs outputs uploads

EXPOSE 8000

CMD ["uv", "run", "serve"]
