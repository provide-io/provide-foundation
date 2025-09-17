#!/bin/bash

# Git Squash to Develop Script
# This script creates a develop branch from current state and squashes all commits into one

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔀 Git Squash to Develop Script${NC}"
echo "=================================================="

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Not in a git repository${NC}"
    exit 1
fi

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
echo -e "${BLUE}📍 Current branch: ${CURRENT_BRANCH}${NC}"

# Check if develop branch already exists
if git branch --list | grep -q "develop"; then
    echo -e "${YELLOW}⚠️  Warning: 'develop' branch already exists${NC}"
    read -p "Do you want to delete it and recreate? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git branch -D develop
        echo -e "${GREEN}✅ Deleted existing develop branch${NC}"
    else
        echo -e "${RED}❌ Aborted${NC}"
        exit 1
    fi
fi

# Stash any uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}📦 Stashing uncommitted changes...${NC}"
    git stash push -m "Auto-stash before squash-to-develop $(date)"
    STASHED=true
else
    STASHED=false
fi

# Get the merge base with origin/main (last common commit)
MERGE_BASE=$(git merge-base HEAD origin/main)
echo -e "${BLUE}🔍 Merge base with origin/main: ${MERGE_BASE:0:8}${NC}"

# Count commits to be squashed
COMMIT_COUNT=$(git log --oneline ${MERGE_BASE}..HEAD | wc -l | tr -d ' ')
echo -e "${BLUE}📊 Commits to squash: ${COMMIT_COUNT}${NC}"

if [ "$COMMIT_COUNT" -eq 0 ]; then
    echo -e "${GREEN}✅ No commits to squash. Creating develop branch from current state.${NC}"
    git checkout -b develop
else
    # Create develop branch
    echo -e "${YELLOW}🌿 Creating develop branch...${NC}"
    git checkout -b develop

    # Generate commit message with summary of squashed commits
    echo -e "${YELLOW}📝 Generating commit message...${NC}"
    COMMIT_MSG_FILE=$(mktemp)

    # Main commit message
    echo "🔀 Squashed ${COMMIT_COUNT} commits into develop branch" > "$COMMIT_MSG_FILE"
    echo "" >> "$COMMIT_MSG_FILE"
    echo "This commit consolidates the following changes:" >> "$COMMIT_MSG_FILE"
    echo "" >> "$COMMIT_MSG_FILE"

    # Add list of original commits
    git log --oneline ${MERGE_BASE}..HEAD --reverse | sed 's/^/- /' >> "$COMMIT_MSG_FILE"

    echo "" >> "$COMMIT_MSG_FILE"
    echo "Generated on $(date)" >> "$COMMIT_MSG_FILE"
    echo "" >> "$COMMIT_MSG_FILE"
    echo "🤖 Generated with Claude Code" >> "$COMMIT_MSG_FILE"

    # Reset to merge base and commit all changes
    echo -e "${YELLOW}🔄 Resetting to merge base and creating squashed commit...${NC}"
    git reset --soft ${MERGE_BASE}

    # Commit with the generated message
    git commit -F "$COMMIT_MSG_FILE"

    # Clean up temp file
    rm "$COMMIT_MSG_FILE"

    echo -e "${GREEN}✅ Successfully created squashed commit${NC}"
fi

# Restore stashed changes if any
if [ "$STASHED" = true ]; then
    echo -e "${YELLOW}📦 Restoring stashed changes...${NC}"
    git stash pop
    echo -e "${GREEN}✅ Stashed changes restored${NC}"
fi

# Show final status
echo ""
echo -e "${GREEN}🎉 Successfully created develop branch with squashed commits!${NC}"
echo ""
echo -e "${BLUE}📋 Summary:${NC}"
echo -e "  • Branch: $(git branch --show-current)"
echo -e "  • Commits squashed: ${COMMIT_COUNT}"
echo -e "  • Last commit: $(git log --oneline -1)"
echo ""
echo -e "${YELLOW}📝 Next steps:${NC}"
echo -e "  • Review the squashed commit: ${BLUE}git show${NC}"
echo -e "  • Push to remote: ${BLUE}git push -u origin develop${NC}"
echo -e "  • Switch back to main: ${BLUE}git checkout ${CURRENT_BRANCH}${NC}"