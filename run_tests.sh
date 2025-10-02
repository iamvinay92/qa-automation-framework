#!/bin/bash

# QA Automation Framework - Test Runner Script
# This script provides easy one-command test execution

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🚀 QA Automation Framework - Test Execution${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

# Function to display menu
show_menu() {
    echo -e "${YELLOW}Select test suite to run:${NC}"
    echo "1) Run ALL tests (API + UI)"
    echo "2) Run API tests only"
    echo "3) Run UI tests only"
    echo "4) Run smoke tests only"
    echo "5) Run with HTML report"
    echo "6) Run with Allure report"
    echo "7) Quick demo (UI test only)"
    echo "0) Exit"
    echo ""
}

# Function to check dependencies
check_dependencies() {
    echo -e "${BLUE}Checking dependencies...${NC}"
    
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 is not installed${NC}"
        exit 1
    fi
    
    if ! python3 -m pip show pytest &> /dev/null; then
        echo -e "${YELLOW}⚠️  Installing dependencies...${NC}"
        pip install -r requirements.txt
    fi
    
    echo -e "${GREEN}✅ All dependencies ready${NC}"
    echo ""
}

# Run all tests
run_all_tests() {
    echo -e "${GREEN}▶️  Running ALL tests (API + UI)...${NC}"
    echo ""
    pytest -v --tb=short
}

# Run API tests
run_api_tests() {
    echo -e "${GREEN}▶️  Running API tests...${NC}"
    echo ""
    pytest api_tests/ -v --tb=short
}

# Run UI tests
run_ui_tests() {
    echo -e "${GREEN}▶️  Running UI tests...${NC}"
    echo ""
    pytest ui_tests/ -v --browser=chrome --tb=short
}

# Run smoke tests
run_smoke_tests() {
    echo -e "${GREEN}▶️  Running smoke tests...${NC}"
    echo ""
    pytest -m smoke -v --tb=short
}

# Run with HTML report
run_with_html_report() {
    echo -e "${GREEN}▶️  Running tests with HTML report...${NC}"
    echo ""
    pytest -v --html=reports/test-report.html --self-contained-html
    echo ""
    echo -e "${GREEN}✅ Report generated: reports/test-report.html${NC}"
    open reports/test-report.html 2>/dev/null || echo "Open reports/test-report.html in your browser"
}

# Run with Allure report
run_with_allure_report() {
    echo -e "${GREEN}▶️  Running tests with Allure report...${NC}"
    echo ""
    pytest --alluredir=reports/allure-results
    
    if command -v allure &> /dev/null; then
        echo ""
        echo -e "${GREEN}✅ Generating Allure report...${NC}"
        allure serve reports/allure-results
    else
        echo ""
        echo -e "${YELLOW}⚠️  Allure not installed. Install with: brew install allure${NC}"
        echo -e "${YELLOW}   Report data saved in: reports/allure-results/${NC}"
    fi
}

# Quick demo
run_quick_demo() {
    echo -e "${GREEN}▶️  Running Quick Demo (UI test)...${NC}"
    echo -e "${YELLOW}   This is the test shown in the GIF demo${NC}"
    echo ""
    pytest ui_tests/tests/test_twitch_search.py::TestTwitchSearch::test_search_starcraft_and_select_streamer -v --browser=chrome
}

# Main script
check_dependencies

# If argument provided, run directly
if [ $# -eq 1 ]; then
    case $1 in
        all)
            run_all_tests
            ;;
        api)
            run_api_tests
            ;;
        ui)
            run_ui_tests
            ;;
        smoke)
            run_smoke_tests
            ;;
        html)
            run_with_html_report
            ;;
        allure)
            run_with_allure_report
            ;;
        demo)
            run_quick_demo
            ;;
        *)
            echo -e "${RED}Invalid option: $1${NC}"
            echo "Usage: ./run_tests.sh [all|api|ui|smoke|html|allure|demo]"
            exit 1
            ;;
    esac
    exit 0
fi

# Interactive menu
while true; do
    show_menu
    read -p "Enter choice [0-7]: " choice
    echo ""
    
    case $choice in
        1)
            run_all_tests
            break
            ;;
        2)
            run_api_tests
            break
            ;;
        3)
            run_ui_tests
            break
            ;;
        4)
            run_smoke_tests
            break
            ;;
        5)
            run_with_html_report
            break
            ;;
        6)
            run_with_allure_report
            break
            ;;
        7)
            run_quick_demo
            break
            ;;
        0)
            echo -e "${BLUE}Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please try again.${NC}"
            echo ""
            ;;
    esac
done

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Test execution completed!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

