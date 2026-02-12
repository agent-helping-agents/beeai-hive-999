#!/data/data/com.termux/files/usr/bin/bash
#
# view_cash_logs.sh
# View Cash Activation Protocol logs in real-time
#
# Usage: ./view_cash_logs.sh
#

set -e

LOG_FILE=~/cash_activation.log

# Check if log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "❌ Log file not found: $LOG_FILE"
    echo ""
    echo "💡 Cash Activation Protocol may not be running yet."
    echo "   Start with: ./start_cash_activation_bg.sh"
    exit 1
fi

# Check if protocol is running
if [ -f ~/.cash_activation.pid ]; then
    PID=$(cat ~/.cash_activation.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ Cash Activation running (PID: $PID)"
    else
        echo "⚠️  Cash Activation not running (stale PID file)"
    fi
else
    echo "⚠️  Cash Activation not running (no PID file)"
fi

echo "📊 Viewing logs from: $LOG_FILE"
echo "   Press Ctrl+C to exit"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Tail logs with follow
tail -f "$LOG_FILE"
