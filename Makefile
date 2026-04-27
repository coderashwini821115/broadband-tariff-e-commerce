# Makefile for common development tasks

.PHONY: help build up down restart logs shell migrate makemigrations createsuperuser test coverage clean

help:
	@echo "Broadband B2C Platform - Development Commands"
	@echo "=============================================="
	@echo "make build          - Build Docker images"
	@echo "make up             - Start all services"
	@echo "make down           - Stop all services"
	@echo "make restart        - Restart all services"
	@echo "make logs           - View logs (all services)"
	@echo "make shell          - Open Django shell"
	@echo "make migrate        - Run database migrations"
	@echo "make makemigrations - Create new migrations"
	@echo "make createsuperuser- Create Django superuser"
	@echo "make test           - Run tests"
	@echo "make coverage       - Run tests with coverage report"
	@echo "make clean          - Remove all containers and volumes"
	@echo "make lint           - Run code linters"
	@echo "make format         - Format code with black and isort"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started! API available at http://localhost:8000"
	@echo "API Docs: http://localhost:8000/api/docs/"
	@echo "Flower: http://localhost:5555/"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

shell:
	docker-compose exec web python manage.py shell_plus

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

test:
	docker-compose exec web pytest -v

coverage:
	docker-compose exec web pytest --cov --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

clean:
	docker-compose down -v
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf htmlcov .coverage .pytest_cache

lint:
	docker-compose exec web flake8 apps config
	docker-compose exec web pylint apps config

format:
	docker-compose exec web black apps config tests
	docker-compose exec web isort apps config tests

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

backup-db:
	docker-compose exec db pg_dump -U postgres broadband_platform > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db:
	@echo "Usage: make restore-db FILE=backup_file.sql"
	docker-compose exec -T db psql -U postgres broadband_platform < $(FILE)
