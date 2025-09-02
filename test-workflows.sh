#!/bin/bash
# Test GitHub Actions workflows locally with act
set -e

echo "🧪 Testing GitHub Workflows with act"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Docker
echo -n "Checking Docker... "
if docker version > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Running${NC}"
else
    echo -e "${RED}❌ Not running${NC}"
    echo "Please start Docker Desktop and try again"
    exit 1
fi

# Check act
echo -n "Checking act... "
if command -v act > /dev/null 2>&1; then
    ACT_VERSION=$(act --version | head -n1)
    echo -e "${GREEN}✅ Installed${NC} ($ACT_VERSION)"
else
    echo -e "${RED}❌ Not installed${NC}"
    echo "Install with: brew install act"
    exit 1
fi

# Setup secrets if needed
if [ ! -f .secrets ]; then
    cp .secrets.example .secrets
    echo -e "${YELLOW}⚠️  Created .secrets file - please add your tokens${NC}"
    echo "   Edit .secrets and add your tokens, then run this script again"
    exit 0
fi

# Function to run a job and report results
run_job() {
    local workflow=$1
    local job=$2
    local description=$3
    
    echo ""
    echo "▶️  Testing: $description"
    echo -n "   Status: "
    
    if act -j "$job" -W ".github/workflows/$workflow" --quiet 2>/dev/null; then
        echo -e "${GREEN}✅ Passed${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  Failed (this is okay for local testing)${NC}"
        return 1
    fi
}

# Function to run a workflow
run_workflow() {
    local workflow=$1
    local event=$2
    local description=$3
    
    echo ""
    echo "▶️  Testing Workflow: $description"
    echo -n "   Status: "
    
    if act "$event" -W ".github/workflows/$workflow" --quiet 2>/dev/null; then
        echo -e "${GREEN}✅ Passed${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  Failed (this is okay for local testing)${NC}"
        return 1
    fi
}

echo ""
echo "Starting workflow tests..."
echo "--------------------------"

# Test individual jobs
run_job "ci.yml" "quality" "Code Quality Checks"
run_job "ci.yml" "test" "Test Suite (Python 3.11)" || true
run_job "ci.yml" "package" "Package Build" || true

# Test full workflows
run_workflow "docs.yml" "push" "Documentation Validation" || true

# Test with dry run
echo ""
echo "▶️  Testing: Release Workflow (dry run)"
echo -n "   Status: "
if act workflow_dispatch -W .github/workflows/release.yml --dryrun > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Valid${NC}"
else
    echo -e "${YELLOW}⚠️  Issues detected${NC}"
fi

echo ""
echo "===================================="
echo -e "${GREEN}✨ Workflow testing complete!${NC}"
echo ""
echo "Notes:"
echo "  • Some failures are expected when running locally"
echo "  • macOS runners are simulated with Linux containers"
echo "  • Network operations (Codecov, PyPI) will fail without real tokens"
echo "  • For full validation, push to GitHub and check Actions tab"
echo ""
echo "To run specific tests:"
echo "  act -j quality                    # Run quality checks only"
echo "  act -j test                       # Run tests only"
echo "  act push                          # Simulate push event"
echo "  act pull_request                  # Simulate PR event"
echo "  act -l                           # List all available jobs"