.PHONY: help init build run test lint format
.DEFAULT_GOAL := help

init:
	poetry install -E toml -E yaml

build:
	poetry build

test:
	poetry run pytest \
		--doctest-modules \
		--cov-report term-missing \
		--cov-report term:skip-covered \
		--cov=src \
		-vv \
		--ff \
		src tests

lint:
	poetry run flake8 src/ tests/
	poetry run isort -rc -c src/ tests/
	poetry run black --diff --check src/ tests/

format:
	poetry run isort -rc src tests
	poetry run black src tests

publish: build
	lucha cicd publish pypi
