import json
import os
import shutil
from pathlib import Path

# --- Configuration ---
# Standard path for Gemini CLI settings. 
# If your config is stored elsewhere, update this path.
CONFIG_PATH = Path.home() / ".gemini" / "settings.json"

# The specific models you want to 'add' (configure as active)
GEMINI_3_MODELS = {
    "pro": "gemini-3-pro-preview",
    "flash": "gemini-3-flash-preview"
}

def update_gemini_config():
    print(f"🔍 Looking for configuration at: {CONFIG_PATH}")

    if not CONFIG_PATH.exists():
        print("❌ Settings file not found. Please run 'gemini' once to generate the default config, then try again.")
        return

    # 1. Create a backup
    backup_path = CONFIG_PATH.with_suffix(".json.bak")
    shutil.copy(CONFIG_PATH, backup_path)
    print(f"bf Safe: Backup created at {backup_path}")

    # 2. Load the JSON
    try:
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("❌ Error: Your settings.json is corrupted. Aborting.")
        return

    # 3. Apply 'Add All Models' Logic (Enable Previews)
    # This unlocks the hidden Gemini 3 list in the CLI
    if "general" not in data:
        data["general"] = {}
    
    data["general"]["previewFeatures"] = True
    print("✅ Enabled 'Preview Features' (Unlocks Gemini 3 models)")

    # 4. Set Active Model to Gemini 3 Pro
    if "model" not in data:
        data["model"] = {}
    
    # You can switch this to GEMINI_3_MODELS["flash"] if you prefer speed
    new_model = GEMINI_3_MODELS["pro"]
    data["model"]["name"] = new_model
    print(f"✅ Set active model to: {new_model}")

    # 5. Save changes
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print("\n🎉 Success! Restart your terminal or CLI to use Gemini 3.")

if __name__ == "__main__":
    update_gemini_config()
