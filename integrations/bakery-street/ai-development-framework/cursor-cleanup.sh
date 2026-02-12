#!/bin/bash

# Remove all Cursor installations except the official one
echo -e "\033[1;31mRemoving duplicate Cursor installations...\033[0m"

# Find all AppImages except the official one
find /opt /usr/local/bin /usr/bin $HOME -iname '*cursor*.AppImage' ! -path '/opt/cursor/cursor.AppImage' -exec sh -c '
    echo -e "\033[1;33mFound duplicate:\033[0m $1"
    read -p "Delete this file? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo rm -v "$1"
    fi
' sh {} \;

# Remove desktop entry if requested
if [[ -f /usr/share/applications/cursor.desktop ]]; then
    echo -e "\n\033[1;33mFound desktop entry:\033[0m"
    ls -l /usr/share/applications/cursor.desktop
    read -p "Remove desktop entry? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo rm -v /usr/share/applications/cursor.desktop
    fi
fi

echo -e "\n\033[1;32mCleanup complete!\033[0m"
