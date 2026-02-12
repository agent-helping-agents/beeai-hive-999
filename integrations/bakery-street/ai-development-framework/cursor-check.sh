#!/bin/bash

# Check installation base
echo -e "\033[1;34m1. Installation Check:\033[0m"
# Check for multiple versions
echo "Checking for existing installations:"
find /opt /usr/local/bin /usr/bin $HOME -iname '*cursor*.AppImage' -exec ls -l {} + 2>/dev/null

if [[ -f /opt/cursor/cursor.AppImage ]]; then
    echo -e "\n✅ Official Cursor AppImage exists"
    echo -n "Version check: "
    /opt/cursor/cursor.AppImage --version || echo "Failed to get version"
else
    echo -e "\n❌ Official Cursor AppImage NOT FOUND in /opt/cursor/"
fi

# Check permissions and integrity
echo -e "\n\033[1;34m2. Permissions Check:\033[0m"
if [[ -f /opt/cursor/cursor.AppImage ]]; then
    ls -l /opt/cursor/cursor.AppImage
    echo -n "Executable check: "
    [[ -x /opt/cursor/cursor.AppImage ]] && echo "OK" || echo "Missing execute permission"
else
    echo "Skipping permissions check - no AppImage found"
fi

# Check dependencies
echo -e "\n\033[1;34m3. Dependencies Check:\033[0m"
if [[ -f /opt/cursor/cursor.AppImage ]]; then
    echo "Shared library dependencies:"
    ldd /opt/cursor/cursor.AppImage | grep -v "not found" | grep . || echo "All dependencies found"
    ldd /opt/cursor/cursor.AppImage | grep "not found" || true
fi

echo -ne "\nFUSE status: "
if which fuse2fs >/dev/null; then
    echo "✅ FUSE installed (version $(fusermount -V))"
else
    echo "❌ FUSE not installed"
fi

# Check desktop integration
echo -e "\nChecking desktop entry:"
ls -l /usr/share/applications/cursor.desktop

# Check running process
echo -e "\nChecking if running:"
pgrep -a "cursor"
