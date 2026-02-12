#!/bin/bash
# Finish a bounty: analyze, generate solution, create PR

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <owner/repo> <issue_number>"
    echo "Example: $0 anthropics/anthropic-sdk-python 123"
    exit 1
fi

REPO=$1
ISSUE=$2

echo "🎯 FINISHING BOUNTY: $REPO #$ISSUE"
echo "======================================="
echo ""

# Step 1: Get issue details
echo "📋 Step 1: Fetching issue details..."
gh issue view $ISSUE --repo $REPO --json title,body,labels,comments > /tmp/bounty_${ISSUE}.json
TITLE=$(jq -r '.title' /tmp/bounty_${ISSUE}.json)
echo "  Issue: $TITLE"
echo ""

# Step 2: Analyze with AI
echo "🧠 Step 2: Analyzing complexity and requirements..."
python3 bounty_hunter.py --mode analyze --repo $REPO --issue $ISSUE
echo ""

# Step 3: Generate solution proposal
echo "💡 Step 3: Generating solution proposal..."
python3 bounty_hunter.py --mode propose --repo $REPO --issue $ISSUE
echo ""

# Step 4: Post proposal as comment
read -p "📝 Post solution proposal as comment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 bounty_hunter.py --mode propose --repo $REPO --issue $ISSUE --auto-comment
    echo "  ✅ Comment posted!"
fi

# Step 5: Offer to create PR
echo ""
read -p "🚀 Create a PR for this bounty? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating PR branch..."
    BRANCH="bounty-${ISSUE}-$(date +%s)"
    git checkout -b $BRANCH 2>/dev/null || echo "Already on a branch"

    echo ""
    echo "Next steps:"
    echo "  1. Make your code changes"
    echo "  2. git add ."
    echo "  3. git commit -m 'fix: solve issue #$ISSUE'"
    echo "  4. git push origin $BRANCH"
    echo "  5. gh pr create --repo $REPO --base main --title 'Fix #$ISSUE: $TITLE'"
fi

echo ""
echo "======================================="
echo "✅ Bounty workflow complete!"
