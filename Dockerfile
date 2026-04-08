FROM python:3.10-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml README.md ./
COPY api/ api/
COPY env/ env/
COPY models/ models/
COPY tasks/ tasks/
COPY utils/ utils/
COPY graders/ graders/
COPY datasets/ datasets/

RUN uv sync --no-dev

EXPOSE 7860

CMD ["uv", "run", "server"]