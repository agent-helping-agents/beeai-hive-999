#!/bin/bash
set -e

WEBHOOK_URL="${SLACK_WEBHOOK_URL:-}"
EMAIL="${ALERT_EMAIL:-}"

if [ -f brain_research_results.txt ]; then
  SUMMARY=$(cat brain_research_results.txt)
  
  if [ -n "$WEBHOOK_URL" ]; then
    curl -X POST -H 'Content-type: application/json' \
      --data "{\"text\":\"🧠 Codex Analysis:\n\`\`\`$SUMMARY\`\`\`\"}" \
      "$WEBHOOK_URL"
    echo "✓ Sent to Slack"
  fi
  
  if [ -n "$EMAIL" ]; then
    echo "$SUMMARY" | mail -s "Codex SuperLab Report" "$EMAIL"
    echo "✓ Sent to Email"
  fi
fi
