.PHONY: help install dev test lint format clean run docker-build docker-run docker-stop

help:
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make dev           - Install development dependencies"
	@echo "  make test          - Run tests with coverage"
	@echo "  make lint          - Run linters (ruff)"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Clean up cache and build files"
	@echo "  make run           - Run the development server"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"
	@echo "  make docker-stop   - Stop Docker container"

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing

lint:
	ruff check app/ tests/
	black --check app/ tests/

format:
	black app/ tests/
	ruff check --fix app/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/ .ruff_cache/ .mypy_cache/

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t fastapi-webapp:latest .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down
