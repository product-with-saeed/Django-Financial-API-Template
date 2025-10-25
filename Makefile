.PHONY: help install install-dev test lint format type-check security clean migrate run shell coverage pre-commit-install pre-commit-run docker-build docker-up docker-down

# Default target
.DEFAULT_GOAL := help

# Python interpreter
PYTHON := python3
PIP := $(PYTHON) -m pip
MANAGE := $(PYTHON) manage.py

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

##@ General

help: ## Display this help message
	@echo "$(BLUE)Django Financial API - Makefile Commands$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make $(GREEN)<target>$(NC)\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Installation

install: ## Install production dependencies
	@echo "$(BLUE)Installing production dependencies...$(NC)"
	$(PIP) install -r requirements/base.txt
	$(PIP) install -r requirements/production.txt
	@echo "$(GREEN)✓ Production dependencies installed$(NC)"

install-dev: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	$(PIP) install -r requirements/base.txt
	$(PIP) install -r requirements/development.txt
	$(PIP) install -r requirements/testing.txt
	@echo "$(GREEN)✓ Development dependencies installed$(NC)"

pre-commit-install: ## Install pre-commit hooks
	@echo "$(BLUE)Installing pre-commit hooks...$(NC)"
	pre-commit install
	pre-commit install --hook-type commit-msg
	@echo "$(GREEN)✓ Pre-commit hooks installed$(NC)"

##@ Development

run: ## Start Django development server
	@echo "$(BLUE)Starting development server...$(NC)"
	$(MANAGE) runserver

shell: ## Open Django shell
	@echo "$(BLUE)Opening Django shell...$(NC)"
	$(MANAGE) shell

migrate: ## Run Django migrations
	@echo "$(BLUE)Running migrations...$(NC)"
	$(MANAGE) migrate
	@echo "$(GREEN)✓ Migrations completed$(NC)"

makemigrations: ## Create new migrations
	@echo "$(BLUE)Creating migrations...$(NC)"
	$(MANAGE) makemigrations
	@echo "$(GREEN)✓ Migrations created$(NC)"

createsuperuser: ## Create Django superuser
	@echo "$(BLUE)Creating superuser...$(NC)"
	$(MANAGE) createsuperuser

collectstatic: ## Collect static files
	@echo "$(BLUE)Collecting static files...$(NC)"
	$(MANAGE) collectstatic --noinput
	@echo "$(GREEN)✓ Static files collected$(NC)"

##@ Testing

test: ## Run tests with coverage
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	pytest
	@echo "$(GREEN)✓ Tests completed$(NC)"

test-unit: ## Run unit tests only
	@echo "$(BLUE)Running unit tests...$(NC)"
	pytest -m unit
	@echo "$(GREEN)✓ Unit tests completed$(NC)"

test-integration: ## Run integration tests only
	@echo "$(BLUE)Running integration tests...$(NC)"
	pytest -m integration
	@echo "$(GREEN)✓ Integration tests completed$(NC)"

test-fast: ## Run tests without coverage (faster)
	@echo "$(BLUE)Running fast tests...$(NC)"
	pytest --no-cov
	@echo "$(GREEN)✓ Fast tests completed$(NC)"

test-verbose: ## Run tests with verbose output
	@echo "$(BLUE)Running verbose tests...$(NC)"
	pytest -vv
	@echo "$(GREEN)✓ Verbose tests completed$(NC)"

coverage: ## Generate coverage report
	@echo "$(BLUE)Generating coverage report...$(NC)"
	pytest --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Coverage report generated at htmlcov/index.html$(NC)"

coverage-open: coverage ## Generate and open coverage report in browser
	@echo "$(BLUE)Opening coverage report...$(NC)"
	@command -v xdg-open > /dev/null && xdg-open htmlcov/index.html || open htmlcov/index.html

##@ Code Quality

lint: ## Run all linters (flake8, mypy, bandit)
	@echo "$(BLUE)Running flake8...$(NC)"
	flake8 api config --config=.flake8
	@echo "$(GREEN)✓ flake8 passed$(NC)"
	@echo "$(BLUE)Running mypy...$(NC)"
	mypy api config --config-file=pyproject.toml || true
	@echo "$(GREEN)✓ mypy completed$(NC)"
	@echo "$(BLUE)Running bandit...$(NC)"
	bandit -c pyproject.toml -r api config || true
	@echo "$(GREEN)✓ All linters completed$(NC)"

format: ## Format code with black and isort
	@echo "$(BLUE)Formatting code with black...$(NC)"
	black api config --config=pyproject.toml
	@echo "$(GREEN)✓ black formatting completed$(NC)"
	@echo "$(BLUE)Sorting imports with isort...$(NC)"
	isort api config --settings-path=pyproject.toml
	@echo "$(GREEN)✓ isort completed$(NC)"

format-check: ## Check code formatting without changes
	@echo "$(BLUE)Checking code formatting...$(NC)"
	black --check api config --config=pyproject.toml
	isort --check-only api config --settings-path=pyproject.toml
	@echo "$(GREEN)✓ Format check completed$(NC)"

type-check: ## Run mypy type checking
	@echo "$(BLUE)Running mypy type checking...$(NC)"
	mypy api config --config-file=pyproject.toml
	@echo "$(GREEN)✓ Type checking completed$(NC)"

security: ## Run security checks with bandit
	@echo "$(BLUE)Running security scan with bandit...$(NC)"
	bandit -c pyproject.toml -r api config
	@echo "$(GREEN)✓ Security scan completed$(NC)"

complexity: ## Check code complexity with radon
	@echo "$(BLUE)Checking code complexity...$(NC)"
	radon cc api config -a -nb
	@echo "$(GREEN)✓ Complexity check completed$(NC)"

pre-commit-run: ## Run all pre-commit hooks
	@echo "$(BLUE)Running pre-commit hooks...$(NC)"
	pre-commit run --all-files
	@echo "$(GREEN)✓ Pre-commit checks completed$(NC)"

check: lint test ## Run all checks (lint + test)
	@echo "$(GREEN)✓ All checks passed$(NC)"

##@ Database

db-reset: ## Reset database (WARNING: Deletes all data)
	@echo "$(RED)WARNING: This will delete all data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(BLUE)Resetting database...$(NC)"; \
		rm -f db.sqlite3; \
		$(MANAGE) migrate; \
		echo "$(GREEN)✓ Database reset completed$(NC)"; \
	else \
		echo "$(YELLOW)Database reset cancelled$(NC)"; \
	fi

db-dump: ## Create database backup
	@echo "$(BLUE)Creating database backup...$(NC)"
	$(MANAGE) dumpdata --natural-foreign --natural-primary --indent=2 > backup_$$(date +%Y%m%d_%H%M%S).json
	@echo "$(GREEN)✓ Database backup created$(NC)"

db-load: ## Load database from backup (requires BACKUP_FILE variable)
	@echo "$(BLUE)Loading database from backup...$(NC)"
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "$(RED)Error: BACKUP_FILE variable required$(NC)"; \
		echo "Usage: make db-load BACKUP_FILE=backup_20231225_120000.json"; \
		exit 1; \
	fi
	$(MANAGE) loaddata $(BACKUP_FILE)
	@echo "$(GREEN)✓ Database loaded from backup$(NC)"

##@ Cleanup

clean: ## Remove all temporary files and caches
	@echo "$(BLUE)Cleaning up temporary files...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".tox" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build dist .eggs
	@echo "$(GREEN)✓ Cleanup completed$(NC)"

clean-all: clean ## Remove all temporary files, caches, and virtualenv
	@echo "$(RED)WARNING: This will remove the virtual environment!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(BLUE)Removing virtual environment...$(NC)"; \
		rm -rf venv .venv; \
		echo "$(GREEN)✓ Full cleanup completed$(NC)"; \
	else \
		echo "$(YELLOW)Full cleanup cancelled$(NC)"; \
	fi

##@ Docker

docker-build: ## Build Docker containers
	@echo "$(BLUE)Building Docker containers...$(NC)"
	docker-compose build
	@echo "$(GREEN)✓ Docker build completed$(NC)"

docker-up: ## Start Docker containers
	@echo "$(BLUE)Starting Docker containers...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Docker containers started$(NC)"

docker-down: ## Stop Docker containers
	@echo "$(BLUE)Stopping Docker containers...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Docker containers stopped$(NC)"

docker-logs: ## View Docker logs
	docker-compose logs -f

docker-shell: ## Open shell in Django container
	docker-compose exec web bash

##@ Documentation

docs-serve: ## Serve documentation locally
	@echo "$(BLUE)Serving documentation...$(NC)"
	@command -v python3 > /dev/null && python3 -m http.server 8001 -d docs/ || echo "$(RED)Python not found$(NC)"

##@ Quick Actions

quick-start: install-dev migrate pre-commit-install ## Quick setup for new developers
	@echo "$(GREEN)✓ Quick start completed!$(NC)"
	@echo "$(BLUE)Run 'make run' to start the development server$(NC)"

ci: format-check lint test ## Run CI checks locally
	@echo "$(GREEN)✓ CI checks passed!$(NC)"

deploy-check: ## Pre-deployment checks
	@echo "$(BLUE)Running pre-deployment checks...$(NC)"
	$(MANAGE) check --deploy
	@echo "$(GREEN)✓ Deployment checks passed$(NC)"

##@ Information

show-urls: ## Show all registered URLs
	@echo "$(BLUE)Registered URLs:$(NC)"
	$(MANAGE) show_urls 2>/dev/null || $(MANAGE) dumpdata --format=json contenttypes | grep -o '"app_label": "[^"]*"' | sort -u

show-settings: ## Show current Django settings
	@echo "$(BLUE)Django Settings:$(NC)"
	$(MANAGE) diffsettings

show-migrations: ## Show migration status
	@echo "$(BLUE)Migration Status:$(NC)"
	$(MANAGE) showmigrations

version: ## Show project version
	@echo "$(BLUE)Django Financial API v1.0.0$(NC)"
	@$(PYTHON) --version
	@$(MANAGE) --version
