.PHONY: help build up down logs migrate test

help:
	@echo "NHL Fantasy Optimizer - Makefile Commands"
	@echo ""
	@echo "  make build        - Build Docker containers"
	@echo "  make up           - Start all services"
	@echo "  make down         - Stop all services"
	@echo "  make logs         - View logs"
	@echo "  make migrate      - Run database migrations"
	@echo "  make test         - Run tests"
	@echo "  make shell        - Open Django shell"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

migrate:
	docker-compose exec backend python manage.py migrate

createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

shell:
	docker-compose exec backend python manage.py shell

test:
	docker-compose exec backend pytest

clean:
	docker-compose down -v
	rm -rf backend/__pycache__ backend/*/__pycache__
