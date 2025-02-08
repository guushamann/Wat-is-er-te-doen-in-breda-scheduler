FROM debian:bookworm-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /scraper

COPY . .
RUN uv sync --frozen
# Setut crawl4ai, important!! does not work without this
RUN uv run crawl4ai-setup

EXPOSE 8086
CMD ["uv", "run",  "app.py"]
