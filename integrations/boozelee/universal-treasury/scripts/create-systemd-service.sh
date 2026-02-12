#!/bin/bash
set -e

echo "🚀 Creating Systemd Service for Universal Treasury CLI"
echo "===================================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ This script must be run as root"
    exit 1
fi

# Get user information
READ_USER="$SUDO_USER"
if [ -z "$READ_USER" ]; then
    read -p "Enter the username to run the service: " READ_USER
fi

USER_HOME=$(eval echo "~$READ_USER")

# Create systemd service file
echo "📄 Creating systemd service file..."

SERVICE_CONTENT="[Unit]
Description=Universal Treasury CLI Service
After=network.target

[Service]
Type=simple
User=$READ_USER
Group=$READ_USER
ExecStart=/usr/bin/podman run --rm \\
    --pod treasury-pod \\
    --name treasury-cli \\
    -v \"$USER_HOME/.treasury:/home/appuser/.treasury\" \\
    -v \"$USER_HOME/workspace/universal-treasury/config:/app/config\" \\
    local/universal-treasury-cli:1.0.0
ExecStop=/usr/bin/podman stop treasury-cli
Restart=always
RestartSec=30
Environment=PODMAN_SYSTEMD_UNIT=%n
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target"

echo "$SERVICE_CONTENT" | sudo tee /etc/systemd/system/treasury-cli.service > /dev/null

echo "✅ Systemd service created"

# Reload systemd
echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload
echo "✅ Systemd reloaded"

# Enable and start service
echo "🎯 Enabling and starting service..."
sudo systemctl enable treasury-cli.service
sudo systemctl start treasury-cli.service
echo "✅ Service enabled and started"

# Show service status
echo ""
echo "📊 Service Status:"
sudo systemctl status treasury-cli.service --no-pager

echo ""
echo "🎉 Systemd Service Setup Complete!"
echo "=================================="
echo "Service commands:"
echo "  sudo systemctl start treasury-cli    # Start service"
echo "  sudo systemctl stop treasury-cli     # Stop service"
echo "  sudo systemctl restart treasury-cli  # Restart service"
echo "  sudo systemctl status treasury-cli   # Check status"
echo "  journalctl -u treasury-cli -f       # View logs"
echo ""
echo "The service will automatically start on boot"
echo "and restart if it crashes."