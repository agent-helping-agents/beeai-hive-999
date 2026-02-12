#!/bin/bash
mkdir -p "$HOME/my-gemini-cli"
cd "$HOME/my-gemini-cli" || { echo "Failed to navigate to ~/my-gemini-cli"; exit 1; }
echo "Diagnosing permissions at $(date)" >> project_scan.log
ls -l "$HOME/my-gemini-cli" >> project_scan.log
stat -c '%U:%G %n' "$HOME/my-gemini-cli"/* >> project_scan.log
lsattr "$HOME/my-gemini-cli"/* 2>/dev/null >> project_scan.log || echo "lsattr not available" >> project_scan.log
mount | grep "$HOME" >> project_scan.log || echo "No mount info for $HOME" >> project_scan.log
sestatus 2>/dev/null >> project_scan.log || echo "SELinux not installed" >> project_scan.log
aa-status 2>/dev/null >> project_scan.log || echo "AppArmor not installed" >> project_scan.log
cat project_scan.log
