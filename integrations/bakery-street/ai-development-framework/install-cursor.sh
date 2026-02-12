#!/bin/bash
set -euo pipefail

# Config
INSTALL_DIR="/opt/cursor"
DOWNLOAD_URL="https://github.com/getcursor/cursor/releases/latest/download/Cursor-linux-x86_64.AppImage"

echo -e "\033[1;34mInstalling Cursor Editor\033[0m"
echo "========================"

# Create install dir
sudo mkdir -p "$INSTALL_DIR"
sudo chown $USER:$USER "$INSTALL_DIR"

# Use existing AppImage or download
echo -e "\n➤ Locating AppImage..."
if [[ -f "/home/booze/Downloads/Cursor-1.5.7-x86_64.AppImage" ]]; then
    echo "Using existing AppImage from Downloads folder"
    cp "/home/booze/Downloads/Cursor-1.5.7-x86_64.AppImage" "$INSTALL_DIR/cursor.AppImage"
else
    echo "Downloading AppImage..."
    if ! wget --show-progress -O "$INSTALL_DIR/cursor.AppImage" "$DOWNLOAD_URL"; then
        echo -e "\033[1;31m❌ Download failed! Trying alternative URL...\033[0m"
        wget --show-progress -O "$INSTALL_DIR/cursor.AppImage" \
            "https://github.com/getcursor/cursor/releases/latest/download/Cursor-linux-x86_64.AppImage" --retry-connrefused
    fi
fi

# Verify AppImage integrity more thoroughly
echo -e "\n➤ Verifying download..."
if file "$INSTALL_DIR/cursor.AppImage" | grep -q "HTML"; then
    echo -e "\033[1;31m❌ Downloaded file is HTML (server error)!\033[0m"
    head "$INSTALL_DIR/cursor.AppImage"
    rm -f "$INSTALL_DIR/cursor.AppImage"
    exit 1
elif [[ ! -s "$INSTALL_DIR/cursor.AppImage" ]]; then
    echo -e "\033[1;31m❌ Downloaded file is empty!\033[0m"
    rm -f "$INSTALL_DIR/cursor.AppImage"
    exit 1
elif ! file "$INSTALL_DIR/cursor.AppImage" | grep -q "AppImage"; then
    echo -e "\033[1;31m❌ Downloaded file is not a valid AppImage!\033[0m"
    echo "This could be due to:"
    echo "1. Corrupted download"
    echo "2. Incorrect download source"
    echo "3. Server-side issues"
    rm -f "$INSTALL_DIR/cursor.AppImage"
    exit 1
fi

# Make executable
chmod +x "$INSTALL_DIR/cursor.AppImage"

# Create desktop entry
echo -e "\n➤ Creating desktop integration..."
cat <<EOF | sudo tee /usr/share/applications/cursor.desktop
[Desktop Entry]
Name=Cursor
Exec=/opt/cursor/cursor.AppImage --no-sandbox
Icon=applications-development
Type=Application
Categories=Development;IDE;
StartupWMClass=cursor
Comment=Build fast with AI
Terminal=false
EOF

echo -e "\n✅ Installation complete! You can now:"
echo "- Launch from your application menu"
echo "- Run from terminal: /opt/cursor/cursor.AppImage"
