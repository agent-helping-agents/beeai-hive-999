#!/bin/bash
# BeeAI Hive 999 - Repo Cleanup Script
# Run this to prepare for marketplace listing

echo "🐝 BeeAI Hive 999 - Cleanup Script"
echo "=================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directories to remove (backups, cache, etc.)
REMOVE_DIRS=(
    ".backup-*"
    ".venv"
    "__pycache__"
    ".pytest_cache"
    ".ruff_cache"
    ".simulator_ledger"
    "logs"
)

# Files to remove
REMOVE_FILES=(
    "*.pyc"
    "*.pyo"
    ".env"
    "*.log"
)

echo "Step 1: Removing backup and cache directories..."
for dir in "${REMOVE_DIRS[@]}"; do
    if ls $dir >/dev/null 2>&1; then
        echo -e "${YELLOW}Removing: $dir${NC}"
        rm -rf $dir
    fi
done

echo ""
echo "Step 2: Removing cache files..."
for pattern in "${REMOVE_FILES[@]}"; do
    files=$(find . -name "$pattern" -type f 2>/dev/null)
    if [ -n "$files" ]; then
        echo -e "${YELLOW}Removing files matching: $pattern${NC}"
        find . -name "$pattern" -type f -delete
    fi
done

echo ""
echo "Step 3: Checking for large files..."
echo "Files over 10MB:"
find . -size +10M -not -path "./.git/*" -exec ls -lh {} \; 2>/dev/null | head -10

echo ""
echo "Step 4: Creating .gitignore if missing..."
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Backup files
*.bak
*~
\#*\#
._*

# Git
.git/
!.gitignore
EOF
    echo -e "${GREEN}Created .gitignore${NC}"
else
    echo -e "${YELLOW}.gitignore already exists${NC}"
fi

echo ""
echo "Step 5: Git status..."
git status --short 2>/dev/null || echo "Not a git repository or git not available"

echo ""
echo "Step 6: List core files for verification..."
echo "Core directories:"
ls -d */ 2>/dev/null | grep -v "\.git"

echo ""
echo "=================================="
echo -e "${GREEN}✅ Cleanup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Review git status above"
echo "2. Test: python beehave.py help"
echo "3. Record demo video"
echo "4. Update landing-page/index.html with video URL"
