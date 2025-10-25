#!/usr/bin/env bash
# Test runner script for Django Financial API
# Ensures correct Python path and virtual environment usage

set -e

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Activate virtual environment if not already activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${BLUE}Activating virtual environment...${NC}"
    source venv/bin/activate
fi

# Run tests with coverage
echo -e "${BLUE}Running tests with coverage...${NC}"
python -m pytest "$@"

# Check exit code
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
else
    echo -e "${RED}✗ Tests failed${NC}"
    exit 1
fi
