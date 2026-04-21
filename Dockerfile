FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev

COPY knowledge/ knowledge/
COPY src/ src/

RUN mkdir -p inputs outputs uploads

EXPOSE 7860

ENV PORT=7860

CMD ["uv", "run", "serve"]
