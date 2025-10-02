# Makefile for QA Automation Framework
# Similar to TestNG.xml in Java projects - provides easy test execution

.PHONY: help install test test-all test-api test-ui test-smoke test-demo clean report

# Default target
.DEFAULT_GOAL := help

# Colors
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m

help: ## Show this help message
	@echo "$(BLUE)═══════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)🚀 QA Automation Framework - Available Commands$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Examples:$(NC)"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run all tests"
	@echo "  make test-demo    - Run quick demo (for GIF)"
	@echo ""

install: ## Install dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	pip install -r requirements.txt
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

test: ## Run all tests (API + UI)
	@echo "$(BLUE)Running all tests...$(NC)"
	pytest -v --tb=short

test-all: test ## Alias for 'test'

test-api: ## Run API tests only
	@echo "$(BLUE)Running API tests...$(NC)"
	pytest api_tests/ -v --tb=short

test-ui: ## Run UI tests only
	@echo "$(BLUE)Running UI tests...$(NC)"
	pytest ui_tests/ -v --browser=chrome --tb=short

test-smoke: ## Run smoke tests only
	@echo "$(BLUE)Running smoke tests...$(NC)"
	pytest -m smoke -v --tb=short

test-demo: ## Run quick demo (UI test for GIF recording)
	@echo "$(BLUE)Running quick demo...$(NC)"
	@echo "$(YELLOW)▶️  This is perfect for GIF recording!$(NC)"
	pytest ui_tests/tests/test_twitch_search.py::TestTwitchSearch::test_search_starcraft_and_select_streamer -v --browser=chrome

test-parallel: ## Run tests in parallel
	@echo "$(BLUE)Running tests in parallel...$(NC)"
	pytest -n auto -v

test-html: ## Run tests with HTML report
	@echo "$(BLUE)Running tests with HTML report...$(NC)"
	pytest -v --html=reports/test-report.html --self-contained-html
	@echo "$(GREEN)✅ Report: reports/test-report.html$(NC)"

test-allure: ## Run tests with Allure report
	@echo "$(BLUE)Running tests with Allure report...$(NC)"
	pytest --alluredir=reports/allure-results
	@echo "$(GREEN)✅ Generating report...$(NC)"
	allure serve reports/allure-results

clean: ## Clean up generated files
	@echo "$(BLUE)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.log" -delete 2>/dev/null || true
	rm -rf reports/*.html reports/allure-results/* 2>/dev/null || true
	@echo "$(GREEN)✅ Cleanup complete$(NC)"

report: ## Open latest HTML report
	@open reports/test-report.html 2>/dev/null || echo "No report found. Run 'make test-html' first."

# Quick shortcuts
demo: test-demo ## Shortcut for test-demo
all: test ## Shortcut for test
api: test-api ## Shortcut for test-api
ui: test-ui ## Shortcut for test-ui
smoke: test-smoke ## Shortcut for test-smoke

