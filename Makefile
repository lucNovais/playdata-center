.DEFAULT_GOAL := help

COMPOSE := docker compose \
	--env-file platform/.env \
	-f platform/compose.yaml

.PHONY: help validate up down ps logs db-ready

help:
	@echo "make validate  Validate the Compose configuration"
	@echo "make up        Start all containers"
	@echo "make down      Stop all containers"
	@echo "make ps        Show container status"
	@echo "make logs      Show container logs"
	@echo "make db-ready  Check PostgreSQL readiness"

validate:
	$(COMPOSE) config --quiet

up: validate
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

ps:
	$(COMPOSE) ps

logs:
	$(COMPOSE) logs --tail=200

db-ready:
	$(COMPOSE) exec db \
		sh -c 'pg_isready -U "$$POSTGRES_USER" -d "$$POSTGRES_DB"'
