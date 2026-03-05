.PHONY: install format lint test clean run_spider crawl_quote docker_run

# Install dependencies
install:
	uv sync

# Run spiders
run_spider:
	uv run python scraper/spiders/spider.py

crawl_quote:
	uv run scrapy crawl quote

# Docker
docker_run:
	docker-compose run scrapy scrapy crawl quote

# Tests
test:
	uv run pytest

# Formatters (modify files in-place)
format:
	uv run ruff format scraper
	uv run ruff check --fix scraper

# Linters
lint:
	uv run mypy --strict --show-error-codes scraper
	uv run ruff check scraper
