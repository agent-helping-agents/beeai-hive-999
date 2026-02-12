#!/bin/bash
# Daily bounty hunting routine

set -e

echo "🌅 DAILY BOUNTY ROUTINE - $(date)"
echo "================================================"
echo ""

# 1. Check all activity
echo "1️⃣ Checking all activity..."
./scripts/check_all_activity.sh > /tmp/daily_activity.txt
cat /tmp/daily_activity.txt
echo ""

# 2. Community engagement
echo "2️⃣ Running community engagement..."
python3 social_automator.py --mode engage --daily
echo ""

# 3. Find new bounties
echo "3️⃣ Scanning for new bounties..."
python3 scripts/bounty_finder.py
echo ""

# 4. Update RAG knowledge base
echo "4️⃣ Updating knowledge base..."
if [ -d "docs" ] && [ "$(ls -A docs)" ]; then
    ./scripts/update_rag.sh
else
    echo "  No docs to index (skip)"
fi
echo ""

echo "================================================"
echo "✅ Daily routine complete!"
echo ""
echo "📊 Summary saved to: /tmp/daily_activity.txt"
echo ""
echo "Next actions:"
echo "  • Review activity in /tmp/daily_activity.txt"
echo "  • Pick a bounty to work on"
echo "  • Run: ./scripts/finish_bounty.sh REPO ISSUE"
