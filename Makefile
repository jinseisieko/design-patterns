.PHONY: install test lint format clean dev docs precommit

# Default target
help:
	@echo "Available commands:"
	@echo "  install   - Install all dependencies"
	@echo "  dev       - Run Flask development server"
	@echo "  test      - Run test suite with coverage"
	@echo "  lint      - Run linter (ruff)"
	@echo "  format    - Format code (black)"
	@echo "  check     - Run lint + format check"
	@echo "  docs      - Build and serve documentation"
	@echo "  precommit - Install pre-commit hooks"
	@echo "  clean     - Remove cache and build files"

install:
	pip install -r requirements-dev.txt
	pre-commit install

dev:
	flask --app app run --debug

test:
	pytest --cov=patterns --cov=app --cov-report=term-missing -v

lint:
	ruff check .

format:
	black .

check:
	ruff check .
	black --check .

docs:
	cd docs && mkdocs serve

precommit:
	pre-commit install

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
