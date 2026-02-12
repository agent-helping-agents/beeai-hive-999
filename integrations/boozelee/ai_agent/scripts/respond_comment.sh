#!/bin/bash
# Respond to comments with AI assistance

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <owner/repo> <issue_number>"
    echo "Example: $0 anthropics/anthropic-sdk-python 123"
    exit 1
fi

REPO=$1
ISSUE=$2

echo "💬 RESPONDING TO COMMENTS: $REPO #$ISSUE"
echo "=========================================="
echo ""

# Get issue and comments
echo "📥 Fetching comments..."
gh issue view $ISSUE --repo $REPO --json title,body,comments > /tmp/comments_${ISSUE}.json

TITLE=$(jq -r '.title' /tmp/comments_${ISSUE}.json)
COMMENT_COUNT=$(jq -r '.comments | length' /tmp/comments_${ISSUE}.json)

echo "  Issue: $TITLE"
echo "  Comments: $COMMENT_COUNT"
echo ""

# Show recent comments
echo "Recent comments:"
echo "----------------"
jq -r '.comments[-3:] | .[] | "  [@\(.author.login)] \(.body | .[0:100])...\n"' /tmp/comments_${ISSUE}.json
echo ""

# Generate AI response
echo "🤖 Generating AI response..."
python3 social_automator.py --mode reply --issue-number $ISSUE

echo ""
read -p "Post this response? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # The script already posted if auto-comment is enabled
    echo "  ✅ Response handling complete!"
fi

echo ""
echo "=========================================="
echo "✅ Comment response complete!"
