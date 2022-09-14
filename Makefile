dev:
	#sudo apt-get install libbz2-dev libreadline-dev #if you python compiled without it requires rebuild
	poetry install

poetry_run_spider: #recommended, easy debugging
	/home/v/.cache/pypoetry/virtualenvs/gsheet-example-iE8nAoYg-py3.10/bin/python3 -m poetry run python3 scraper/spiders/spider.py

poetry_crawl_quote:
	poetry run scrapy crawl quote

compose_crawl_quote:
	docker-compose run scrapy scrapy crawl quote

pytest:
	poetry run pytest

# all formatters (note: this modifies files in-place)
format: autoflake black isort docformatter

lint: mypy pylint


# linters
pylint:
	find scraper -type f -name "*.py" | xargs poetry run pylint

mypy:
	poetry run mypy --strict --show-error-codes scraper

# formatters
autoflake:
	find scraper -type f -name "*.py" | xargs poetry run autoflake --in-place --remove-unused-variables --remove-all-unused-imports

black:
	poetry run black scraper

isort:
	poetry run isort scraper

docformatter:
	poetry run docformatter --recursive --in-place --wrap-summaries 120 --wrap-descriptions 120 scraper