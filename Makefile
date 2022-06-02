.PHONY: install build test lint format publish
.DEFAULT_GOAL := test

install:
	poetry install -E toml -E yaml -E vault

build:
	poetry build

test:
	coverage run -a -m py.test src tests -vv
	coverage report
	coverage xml

lint:
	flake8 src tests
	isort --check-only src tests
	pydocstyle src tests
	black --check src tests
	mypy src tests
	bandit src

format:
	isort src tests
	black src tests

publish: build
	poetry publish -u __token__ -p '${PYPI_PASSWORD}' --no-interaction
