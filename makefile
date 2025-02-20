# Run all lines of a target in a single shell session
.ONESHELL:
# Use bash as the shell
SHELL=/bin/bash

install_uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh

db_start:
	cd db
	docker compose up -d

db_stop:
	cd db
	docker compose down

api_start:
	./bootstrap.sh
