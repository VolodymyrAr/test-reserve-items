run:
	@docker compose up -d --build

stop:
	@echo "Stopping all services..."
	@docker compose down

logs:
	@echo "Show logs..."
	@docker compose logs -f web

lint:
	@echo "Running pre-commit for all files"
	@poetry run pre-commit run --all-files
