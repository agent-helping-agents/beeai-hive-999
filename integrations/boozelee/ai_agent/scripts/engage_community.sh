#!/bin/bash
# Daily community engagement

set -e

echo "🌟 Community Engagement"
echo "======================"

python3 social_automator.py --mode engage --daily

echo ""
echo "✅ Community engagement complete!"
