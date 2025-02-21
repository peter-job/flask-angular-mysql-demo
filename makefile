# Run all lines of a target in a single shell session
.ONESHELL:
# Use bash as the shell
SHELL=/bin/bash

setup: uv_install uv_venv uv_sync

uv_install:
	curl -LsSf https://astral.sh/uv/install.sh | sh

uv_venv:
	uv venv

uv_sync:
	uv sync

ruff_check:
	uv run ruff check

db_start:
	cd db
	docker compose up -d

db_stop:
	cd db
	docker compose down

api_start:
	export FLASK_APP=./api
	uv run flask --debug run -h 0.0.0.0

api_test:
	uv run python -m unittest discover -s api/tests