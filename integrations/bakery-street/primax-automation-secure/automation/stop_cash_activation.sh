#!/data/data/com.termux/files/usr/bin/bash
#
# stop_cash_activation.sh
# Stops Cash Activation Protocol background process
#
# Usage: ./stop_cash_activation.sh
#

set -e

echo "🛑 Stopping Cash Activation Protocol..."

# Check if PID file exists
if [ ! -f ~/.cash_activation.pid ]; then
    echo "❌ No PID file found (~/.cash_activation.pid)"
    echo ""
    echo "💡 Cash Activation may not be running."
    echo "   Check with: ps aux | grep cash_activation"
    exit 1
fi

# Read PID
PID=$(cat ~/.cash_activation.pid)

# Check if process is running
if ! ps -p $PID > /dev/null 2>&1; then
    echo "⚠️  Process $PID is not running (stale PID file)"
    rm ~/.cash_activation.pid
    echo "🧹 Cleaned stale PID file"
    exit 0
fi

# Kill process
echo "🔪 Killing process $PID..."
kill $PID

# Wait for process to terminate
sleep 2

# Verify termination
if ps -p $PID > /dev/null 2>&1; then
    echo "⚠️  Process still running, forcing termination..."
    kill -9 $PID
    sleep 1
fi

# Remove PID file
rm ~/.cash_activation.pid

echo "✅ Cash Activation Protocol stopped"
echo "   PID $PID terminated"
echo ""
echo "📊 View final logs with: tail ~/cash_activation.log"
