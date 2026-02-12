#!/usr/bin/env python3
"""
Supabase Secrets Manager - Python Version
Manages LangSmith, OpenAI, and other API keys for Hive 999
"""

import os
import sys
import subprocess
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def run_sql(sql: str) -> bool:
    """Execute SQL via Supabase CLI."""
    try:
        result = subprocess.run(
            ["supabase", "db", "execute", sql],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("❌ Supabase CLI not found. Install with:")
        print("   npm install -g supabase")
        return False

def init_vault():
    """Initialize Supabase Vault extension."""
    sql = """
    CREATE EXTENSION IF NOT EXISTS vault WITH SCHEMA vault;
    """
    return run_sql(sql)

def add_secret(name: str, value: str, description: str = "") -> bool:
    """Add or update a secret in Vault."""
    # First delete existing
    delete_sql = f"DELETE FROM vault.secrets WHERE name = '{name}';"
    run_sql(delete_sql)
    
    # Insert new
    insert_sql = f"""
    INSERT INTO vault.secrets (name, secret, description)
    VALUES ('{name}', '{value}', '{description}');
    """
    return run_sql(insert_sql)

def get_secret(name: str) -> str:
    """Retrieve a secret from Vault."""
    sql = f"SELECT secret FROM vault.secrets WHERE name = '{name}';"
    try:
        result = subprocess.run(
            ["supabase", "db", "execute", sql],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except:
        return None

def list_secrets():
    """List all secrets in Vault."""
    sql = "SELECT name, description, created_at FROM vault.secrets;"
    try:
        result = subprocess.run(
            ["supabase", "db", "execute", sql],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Could not list secrets. Is Supabase running?")
    except Exception as e:
        print(f"Error: {e}")

def interactive_setup():
    """Interactive setup wizard."""
    print("""
╔════════════════════════════════════════════════════════════════╗
║     🐝 HIVE 999 - Supabase Secrets Manager (Python)            ║
╚════════════════════════════════════════════════════════════════╝
""")
    
    # Check if supabase is initialized
    if not Path("supabase/config.toml").exists():
        print("⚠️  No Supabase project found!")
        print("\nOptions:")
        print("  1. Initialize: supabase init")
        print("  2. Link existing: supabase link --project-ref <id>")
        return
    
    print("📋 Available actions:")
    print("  1. Add LangSmith API key")
    print("  2. Add OpenAI API key")
    print("  3. Add Anthropic API key")
    print("  4. Add all secrets")
    print("  5. List current secrets")
    print("  6. Export secrets to .env")
    print("  7. Exit")
    
    choice = input("\nSelect (1-7): ").strip()
    
    if choice == "1":
        key = input("Enter LangSmith API key: ").strip()
        if key:
            if add_secret("LANGSMITH_API_KEY", key, "LangSmith tracing"):
                print("✅ LangSmith API key added!")
            else:
                print("❌ Failed to add key")
    
    elif choice == "2":
        key = input("Enter OpenAI API key: ").strip()
        if key:
            if add_secret("OPENAI_API_KEY", key, "OpenAI GPT models"):
                print("✅ OpenAI API key added!")
            else:
                print("❌ Failed to add key")
    
    elif choice == "3":
        key = input("Enter Anthropic API key: ").strip()
        if key:
            if add_secret("ANTHROPIC_API_KEY", key, "Claude models"):
                print("✅ Anthropic API key added!")
            else:
                print("❌ Failed to add key")
    
    elif choice == "4":
        print("\n--- LangSmith ---")
        ls_key = input("Enter LangSmith API key: ").strip()
        print("\n--- OpenAI ---")
        oa_key = input("Enter OpenAI API key: ").strip()
        print("\n--- Anthropic (optional) ---")
        an_key = input("Enter Anthropic API key: ").strip()
        
        success = True
        if ls_key and not add_secret("LANGSMITH_API_KEY", ls_key, "LangSmith tracing"):
            success = False
        if oa_key and not add_secret("OPENAI_API_KEY", oa_key, "OpenAI GPT models"):
            success = False
        if an_key and not add_secret("ANTHROPIC_API_KEY", an_key, "Claude models"):
            success = False
        
        if success:
            print("\n✅ All secrets added successfully!")
        else:
            print("\n⚠️  Some secrets failed to add")
    
    elif choice == "5":
        print("\n📋 Current secrets:")
        list_secrets()
    
    elif choice == "6":
        export_to_env()
    
    elif choice == "7":
        print("👋 Goodbye!")
        return

def export_to_env():
    """Export secrets to .env file."""
    env_path = Path(".env")
    
    secrets = {
        "LANGSMITH_API_KEY": get_secret("LANGSMITH_API_KEY"),
        "OPENAI_API_KEY": get_secret("OPENAI_API_KEY"),
        "ANTHROPIC_API_KEY": get_secret("ANTHROPIC_API_KEY"),
    }
    
    with open(env_path, "a") as f:
        f.write("\n# Hive 999 Secrets (auto-exported)\n")
        for name, value in secrets.items():
            if value:
                f.write(f"export {name}={value}\n")
                print(f"✅ Exported {name}")
    
    print(f"\n📁 Secrets exported to {env_path}")
    print("To load: source .env")

def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "list":
            list_secrets()
        elif command == "export":
            export_to_env()
        elif command == "init":
            if init_vault():
                print("✅ Vault initialized")
            else:
                print("❌ Failed to initialize vault")
        else:
            print(f"Unknown command: {command}")
            print("Usage: python manage_secrets.py [list|export|init]")
    else:
        interactive_setup()

if __name__ == "__main__":
    main()
