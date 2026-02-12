import json
import os
from pathlib import Path

# --- The Master List of Models ---
MODELS = {
    "1": ("Gemini 3 Pro (Preview)", "gemini-3-pro-preview"),
    "2": ("Gemini 3 Flash (Preview)", "gemini-3-flash-preview"),
    "3": ("Gemini 3 Deep Think", "gemini-3-deep-think-preview"),
    "4": ("Gemini 2.5 Pro (Stable)", "gemini-2.5-pro"),
    "5": ("Gemini 2.5 Flash (Stable)", "gemini-2.5-flash"),
    "6": ("Gemini 2.0 Flash Thinking", "gemini-2.0-flash-thinking-exp-01-21"),
}

CONFIG_PATH = Path.home() / ".gemini" / "settings.json"

def load_settings():
    if not CONFIG_PATH.exists():
        return {}
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_settings(data):
    # Ensure directories exist
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)

def main():
    print(f"--- 🤖 Gemini CLI Model Switcher ---")
    print(f"Config file: {CONFIG_PATH}\n")
    
    # 1. Force Enable Preview Features (Required for v3)
    data = load_settings()
    if "general" not in data: data["general"] = {}
    if not data["general"].get("previewFeatures"):
        data["general"]["previewFeatures"] = True
        print("✅ Auto-enabled 'Preview Features' (required for Gemini 3)")

    # 2. Display Menu
    current_model = data.get("model", {}).get("name", "Unknown")
    print(f"Current Model: \033[1;32m{current_model}\033[0m\n")
    
    print("Available Models:")
    for key, (name, model_id) in MODELS.items():
        print(f"[{key}] {name}")
    
    choice = input("\nSelect a model number (or 'q' to quit): ").strip()
    
    if choice in MODELS:
        name, model_id = MODELS[choice]
        if "model" not in data: data["model"] = {}
        data["model"]["name"] = model_id
        
        # Special handling for "Thinking" models to ensure they work
        if "thinking" in model_id:
             # Ensure thinking budget isn't zeroed out if your CLI supports it
             if "parameters" not in data["model"]: data["model"]["parameters"] = {}
             # Optional: set a default budget if needed, usually defaults are fine
        
        save_settings(data)
        print(f"\n✨ Success! Switched to: {name} ({model_id})")
        print("Restart your CLI for changes to take effect.")
    else:
        print("No changes made.")

if __name__ == "__main__":
    main()
