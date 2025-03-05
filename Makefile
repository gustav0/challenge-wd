ifeq ($(shell command -v docker-compose),)
    ifeq ($(shell docker compose version > /dev/null 2>&1 && echo yes),yes)
        COMPOSE_CMD = docker compose
    else
        $(error Neither 'docker-compose' nor 'docker compose' is available. Please install Docker Compose.)
    endif
else
    COMPOSE_CMD = docker-compose
endif

.PHONY: help
help: # Show help for each of the Makefile recipes.
	@echo "Help page:"
	@grep -E '^[a-zA-Z0-9 -]+:.*#' Makefile | \
		sort | \
		while read -r l; do \
			target=$$(echo $$l | cut -f 1 -d':'); \
			description=$$(echo $$l | cut -f 2- -d'#'); \
			printf "\t\033[1;32m%-16s\033[00m - %s\n" "$$target" "$$description"; \
		done

.PHONY: build
build: # Build docker image. Allows `args="--no-cache"` and other compose buildptions
	$(COMPOSE_CMD) build _base $(args)

.PHONY: migrations
migrations: # Generate migrations. Allows -m="custom_migration_name"
	$(COMPOSE_CMD) run --rm alembic revision --autogenerate -m "$(m)"

.PHONY: migrate
migrate: # Apply migrations
	$(COMPOSE_CMD) run --rm alembic upgrade head

.PHONY: run
run: # Start FastAPI and Celery. Allows `args="-d"` and other compose options
	$(COMPOSE_CMD) up celery api $(args)

.PHONY: pull
pull: # Start FastAPI and Celery in the background
	$(COMPOSE_CMD) pull

.PHONY: revert
revert_migrate: # Unapply a single migration
	$(COMPOSE_CMD) run --rm alembic downgrade -1

.PHONY: test
test: # Executes tests. Allows `args="-k test_name"` and other pytest options
	$(COMPOSE_CMD) run --rm test $(args)
