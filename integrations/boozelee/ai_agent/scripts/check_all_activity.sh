#!/bin/bash
# Check all GitHub activity: PRs, bounties, comments

set -e

echo "🔍 CHECKING ALL GITHUB ACTIVITY"
echo "=================================="
echo ""

# Check for PRs
echo "📋 YOUR OPEN PULL REQUESTS:"
echo "----------------------------"
gh search prs "author:@me is:open" --json number,title,repository,url,createdAt --limit 20 2>/dev/null | \
  jq -r '.[] | "  PR #\(.number): \(.title)\n    Repo: \(.repository.nameWithOwner)\n    URL: \(.url)\n"' || echo "  No open PRs found"

echo ""
echo "🎯 ASSIGNED BOUNTIES/ISSUES:"
echo "----------------------------"
gh search issues "assignee:@me is:open" --json number,title,repository,labels,url --limit 20 2>/dev/null | \
  jq -r '.[] | "  Issue #\(.number): \(.title)\n    Repo: \(.repository.nameWithOwner)\n    Labels: \(.labels | map(.name) | join(", "))\n    URL: \(.url)\n"' || echo "  No assigned issues"

echo ""
echo "💬 RECENT MENTIONS (Need Response):"
echo "------------------------------------"
gh api /notifications --jq '.[] | select(.reason == "mention" or .reason == "comment") | {repo: .repository.full_name, title: .subject.title, type: .subject.type, url: .subject.url}' 2>/dev/null | \
  jq -r '"  [\(.type)] \(.repo)\n    \(.title)\n    \(.url)\n"' | head -30 || echo "  No recent mentions"

echo ""
echo "🔥 RECENT ACTIVITY (Last 24h):"
echo "-------------------------------"
gh search issues "involves:@me is:open updated:>=2026-02-08" --json number,title,repository,updatedAt,url --limit 20 2>/dev/null | \
  jq -r '.[] | "  #\(.number): \(.title)\n    Repo: \(.repository.nameWithOwner)\n    Updated: \(.updatedAt)\n    URL: \(.url)\n"' || echo "  No recent activity"

echo ""
echo "💰 OPEN BOUNTIES (Available to Claim):"
echo "---------------------------------------"
gh search issues "is:open label:bounty,bug-bounty,reward no:assignee" --limit 15 --json number,title,repository,labels,url 2>/dev/null | \
  jq -r '.[] | "  💰 #\(.number): \(.title)\n    Repo: \(.repository.nameWithOwner)\n    URL: \(.url)\n"' || echo "  No unclaimed bounties found"

echo ""
echo "=================================="
echo "✅ Activity check complete!"
echo ""
echo "Next steps:"
echo "  1. Pick an item from above"
echo "  2. Run: ./scripts/finish_bounty.sh REPO ISSUE_NUMBER"
echo "  3. Or: ./scripts/respond_comment.sh REPO ISSUE_NUMBER"
