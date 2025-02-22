# Use bash as the shell
SHELL=/bin/bash

setup: uv_install uv_venv uv_sync ui_install

uv_install:
	curl -LsSf https://astral.sh/uv/install.sh | sh

uv_venv:
	uv venv

uv_sync:
	uv sync

db_start:
	cd db && \
	docker compose up -d

db_stop:
	cd db && \
	docker compose down

api_start:
	export FLASK_APP=./api \
	uv run flask --debug run

api_test:
	uv run python -m unittest discover -s api/tests

api_check:
	uv run ruff check

ng_install:
	npm install -g @angular/cli

ui_install:
	cd ui && \
	npm install

ui_test:
	cd ui && \
	npm test

ui_lint:
	cd ui && \
	npm run lint
