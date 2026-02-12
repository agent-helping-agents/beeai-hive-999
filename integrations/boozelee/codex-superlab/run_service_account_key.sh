#!/bin/bash
mkdir -p "$HOME/my-gemini-cli"
cd "$HOME/my-gemini-cli" || { echo "Failed to navigate to ~/my-gemini-cli"; exit 1; }
chmod +x create_service_account_key.sh
./create_service_account_key.sh
