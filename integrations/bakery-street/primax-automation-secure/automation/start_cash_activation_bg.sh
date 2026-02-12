#!/data/data/com.termux/files/usr/bin/bash
#
# start_cash_activation_bg.sh
# Starts Cash Activation Protocol in background mode
#
# Usage: ./start_cash_activation_bg.sh
#

set -e

echo "🚀 Starting Cash Activation Protocol..."

# Load environment variables if config exists
if [ -f ~/cash_activation.env ]; then
    echo "📋 Loading environment from ~/cash_activation.env"
    source ~/cash_activation.env
else
    echo "⚠️  No cash_activation.env found - using system environment"
fi

# Check if already running
if [ -f ~/.cash_activation.pid ]; then
    OLD_PID=$(cat ~/.cash_activation.pid)
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "❌ Cash Activation already running (PID: $OLD_PID)"
        echo "   Use ./stop_cash_activation.sh to stop it first"
        exit 1
    else
        echo "🧹 Cleaning stale PID file"
        rm ~/.cash_activation.pid
    fi
fi

# Start protocol in background
echo "🎯 Launching background process..."
nohup python3 ~/cash_activation_protocol.py > ~/cash_activation.log 2>&1 &
CASH_PID=$!

# Save PID
echo $CASH_PID > ~/.cash_activation.pid

echo "✅ Cash Activation Protocol started"
echo "   PID: $CASH_PID"
echo "   Log: ~/cash_activation.log"
echo ""
echo "📊 Monitor with: ./view_cash_logs.sh"
echo "🛑 Stop with: ./stop_cash_activation.sh"
