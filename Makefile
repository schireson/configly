.PHONY: install build test lint format publish
.DEFAULT_GOAL := test

install:
	poetry install -E toml -E yaml -E vault

build:
	poetry build

test:
	coverage run -a -m py.test src tests -vv
	coverage report
	poetry run coverage xml

lint:
	poetry run flake8 src tests
	poetry run isort --check-only --recursive src tests
	poetry run pydocstyle src tests
	poetry run black --check src tests
	poetry run mypy src tests
	poetry run bandit src

format:
	poetry run isort --recursive src tests
	poetry run black src tests

publish: build
	poetry publish -u __token__ -p '${PYPI_PASSWORD}' --no-interaction
