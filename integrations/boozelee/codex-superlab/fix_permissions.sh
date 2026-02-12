#!/bin/bash
mkdir -p "$HOME/my-gemini-cli"
sudo chown -R boozelee:boozelee "$HOME/my-gemini-cli"
sudo chmod -R u+rwX "$HOME/my-gemini-cli"
sudo chattr -i "$HOME/my-gemini-cli"/* 2>/dev/null || true
find "$HOME/my-gemini-cli" -name "*.sh" -exec chmod +x {} \;
find "$HOME/my-gemini-cli" -name "*.py" -exec chmod +x {} \;
echo "Fixed at $(date)" >> "$HOME/my-gemini-cli/project_scan.log"
ls -l "$HOME/my-gemini-cli" >> "$HOME/my-gemini-cli/project_scan.log"
cat "$HOME/my-gemini-cli/project_scan.log"
