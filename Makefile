start:
	@docker compose up -d --build

stop:
	@echo "Stopping all services..."
	@docker compose down

build:
	@docker compose build --no-cache

db:
	@echo "Starting postgres..."
	@docker compose up -d postgres

run:
	@poetry run python run.py

logs:
	@echo "Show logs..."
	@docker compose logs -f web

lint:
	@echo "Running pre-commit for all files"
	@poetry run pre-commit run --all-files

migration:
	@echo "Generate alembic migration - $(m) ..."
	@poetry run alembic revision --autogenerate -m $(m)

migrate:
	@echo "Apply alembic migration..."
	@poetry run alembic upgrade head

test:
	@pytest
