import json
import os
import getpass
from pathlib import Path

# --- Configuration ---
CONFIG_PATH = Path.home() / ".gemini" / "settings.json"

def get_new_key():
    print("--- 🔑 Gemini API Key Updater ---")
    print("Option 1: Paste your new key directly.")
    print("Option 2: If using a Vault, ensure your vault exports 'GEMINI_API_KEY' to your env.")
    print("        (This script will configure the CLI to look for that key.)")
    
    choice = input("\nDo you want to (P)aste key or configure (E)nv var? [P/e]: ").lower().strip()
    
    if choice == 'e':
        return "ENV_VAR_MODE"
    else:
        return getpass.getpass(prompt="Paste your new API Key (hidden input): ").strip()

def update_config(new_key_value):
    # 1. Ensure config dir exists
    if not CONFIG_PATH.parent.exists():
        CONFIG_PATH.parent.mkdir(parents=True)
        print(f"Created directory: {CONFIG_PATH.parent}")

    # 2. Load existing settings or create new
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    else:
        data = {}

    # 3. Update the key
    if "context" not in data:
        data["context"] = {}
    
    # If user chose Env Var mode, we don't save the key to the file.
    # We essentially clear it so the CLI is forced to look at the environment.
    if new_key_value == "ENV_VAR_MODE":
        # Remove hardcoded key if it exists to force Env Var usage
        if "key" in data["context"]:
            del data["context"]["key"]
        print("✅ Config updated to prefer Environment Variables.")
        print("   -> Make sure to run: export GEMINI_API_KEY='your_key_here' (or via your Vault)")
    else:
        # Standard mode: Save key to file
        data["context"]["key"] = new_key_value
        print("✅ New API Key saved to settings.json.")

    # 4. Save
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)

def main():
    key = get_new_key()
    if not key:
        print("❌ No key provided. Exiting.")
        return
    
    update_config(key)
    print(f"\nConfiguration file: {CONFIG_PATH}")
    print("You can now run 'gemini' to test.")

if __name__ == "__main__":
    main()
