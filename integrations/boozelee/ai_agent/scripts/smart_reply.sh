#!/bin/bash
# Smart reply to GitHub mentions

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <issue_number>"
    exit 1
fi

ISSUE_NUMBER=$1

echo "💬 Smart Reply to Issue #$ISSUE_NUMBER"
python3 social_automator.py --mode reply --issue-number "$ISSUE_NUMBER"
