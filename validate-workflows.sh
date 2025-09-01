#!/bin/bash
# Validate GitHub Actions workflows without Docker/act
# This script simulates the key checks from the workflows

set -e

echo "🧪 Validating GitHub Workflows (Docker-free)"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Change to project directory
cd /Users/tim/code/gh/provide-io/provide-foundation

# Source the environment
echo -e "${BLUE}Setting up environment...${NC}"
source env.sh > /dev/null 2>&1

echo ""
echo "🔍 Quality Checks"
echo "-----------------"

# 1. Ruff Linting
echo -n "Ruff Linting: "
if ruff check src/ --quiet 2>/dev/null; then
    echo -e "${GREEN}✅ Passed${NC}"
else
    echo -e "${YELLOW}⚠️  Has issues (run 'ruff check src/' for details)${NC}"
fi

# 2. Ruff Formatting
echo -n "Ruff Format: "
if ruff format --check src/ --quiet 2>/dev/null; then
    echo -e "${GREEN}✅ Properly formatted${NC}"
else
    echo -e "${YELLOW}⚠️  Needs formatting (run 'ruff format src/')${NC}"
fi

# 3. MyPy Type Checking
echo -n "MyPy Types: "
if mypy src/ --no-error-summary 2>/dev/null | grep -q "Success"; then
    echo -e "${GREEN}✅ Type safe${NC}"
else
    echo -e "${YELLOW}⚠️  Type issues exist${NC}"
fi

echo ""
echo "🧪 Test Suite"
echo "-------------"

# 4. Run Tests
echo -n "Pytest: "
TEST_OUTPUT=$(pytest tests/ -q --tb=no 2>&1 | tail -1)
if echo "$TEST_OUTPUT" | grep -q "passed"; then
    echo -e "${GREEN}✅ $TEST_OUTPUT${NC}"
else
    echo -e "${YELLOW}⚠️  $TEST_OUTPUT${NC}"
fi

echo ""
echo "📦 Package Build"
echo "----------------"

# 5. Version Check
echo -n "Version Check: "
if python scripts/version_checker.py > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Versions consistent${NC}"
else
    echo -e "${YELLOW}⚠️  Version mismatch${NC}"
fi

# 6. Build Package
echo -n "Package Build: "
if uv build --quiet > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Build successful${NC}"
    # Check if package was created
    if ls dist/*.whl > /dev/null 2>&1; then
        WHEEL=$(ls -t dist/*.whl | head -1)
        SIZE=$(du -h "$WHEEL" | cut -f1)
        echo "   📦 Created: $(basename $WHEEL) ($SIZE)"
    fi
else
    echo -e "${RED}❌ Build failed${NC}"
fi

echo ""
echo "📚 Documentation"
echo "----------------"

# 7. Check examples
echo -n "Example Scripts: "
EXAMPLE_COUNT=$(ls examples/*.py 2>/dev/null | wc -l | tr -d ' ')
if [ "$EXAMPLE_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✅ $EXAMPLE_COUNT examples found${NC}"
    # Test one example
    if python examples/basic_usage.py > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅ basic_usage.py runs${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  No examples found${NC}"
fi

# 8. Documentation files
echo -n "Documentation: "
DOC_COUNT=$(find docs -name "*.md" | wc -l | tr -d ' ')
echo -e "${GREEN}✅ $DOC_COUNT markdown files${NC}"

echo ""
echo "🚀 Workflow Files"
echo "-----------------"

# 9. YAML Validation
echo -n "YAML Syntax: "
ERROR_COUNT=0
for workflow in .github/workflows/*.yml; do
    if ! python -c "import yaml; yaml.safe_load(open('$workflow'))" 2>/dev/null; then
        ((ERROR_COUNT++))
    fi
done

if [ $ERROR_COUNT -eq 0 ]; then
    echo -e "${GREEN}✅ All workflows valid${NC}"
else
    echo -e "${RED}❌ $ERROR_COUNT workflow(s) have errors${NC}"
fi

# 10. List workflows
echo -e "\nWorkflows available:"
for workflow in .github/workflows/*.yml; do
    NAME=$(basename "$workflow" .yml)
    echo "  • $NAME"
done

echo ""
echo "============================================="
echo -e "${GREEN}✨ Validation Complete!${NC}"
echo ""
echo "Summary:"
echo "  • Most checks can be run without Docker/act"
echo "  • For full GitHub Actions testing, push to a branch"
echo "  • Use 'ruff format src/' to auto-fix formatting"
echo "  • Use 'pytest -xvs' for detailed test output"
echo ""
echo "To fix linting issues:"
echo "  ruff check src/ --fix"
echo "  ruff format src/"
echo ""
echo "To run specific checks:"
echo "  pytest tests/           # Run all tests"
echo "  mypy src/              # Type checking"
echo "  uv build               # Build package"