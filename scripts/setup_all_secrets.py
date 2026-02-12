#!/usr/bin/env python3
"""
Unified Secrets Manager for Hive 999
Manages:
- Supabase Vault (LangSmith, OpenAI, etc.)
- Ngrok configuration
- Zoho Mail credentials
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent))

def run_command(cmd, capture=True):
    """Run a shell command."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=capture, text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_supabase():
    """Check if Supabase is initialized."""
    return Path("supabase/config.toml").exists()

def add_to_supabase_vault(name: str, value: str, description: str = ""):
    """Add secret to Supabase Vault."""
    if not check_supabase():
        print(f"⚠️  Supabase not initialized. Saving to .env instead.")
        return add_to_env(name, value)
    
    sql = f"""
    CREATE EXTENSION IF NOT EXISTS vault WITH SCHEMA vault;
    DELETE FROM vault.secrets WHERE name = '{name}';
    INSERT INTO vault.secrets (name, secret, description)
    VALUES ('{name}', '{value}', '{description}');
    """
    
    success, stdout, stderr = run_command(f"supabase db execute \"{sql}\"")
    if success:
        print(f"✅ Added {name} to Supabase Vault")
        return True
    else:
        print(f"⚠️  Could not add to Vault: {stderr}")
        print(f"   Saving to .env instead")
        return add_to_env(name, value)

def add_to_env(name: str, value: str):
    """Add secret to .env file."""
    env_path = Path.home() / ".env"
    
    # Check if already exists
    if env_path.exists():
        content = env_path.read_text()
        if f"export {name}=" in content:
            # Remove existing line
            lines = content.split('\n')
            lines = [l for l in lines if not l.startswith(f"export {name}=")]
            content = '\n'.join(lines)
            env_path.write_text(content)
    
    # Append new value
    with open(env_path, "a") as f:
        f.write(f"export {name}={value}\n")
    
    print(f"✅ Added {name} to ~/.env")
    return True

def setup_ngrok():
    """Setup ngrok authentication."""
    print("\n" + "=" * 55)
    print("NGROK SETUP")
    print("=" * 55)
    print("\nNgrok provides public URLs for local services.")
    print("Required for Zoho domain verification.")
    print("\nGet your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken")
    
    token = input("\nEnter ngrok authtoken (or press Enter to skip): ").strip()
    
    if token:
        success, stdout, stderr = run_command(f"ngrok config add-authtoken {token}")
        if success:
            print("✅ Ngrok configured successfully")
            # Also save to Supabase/env for reference
            add_to_supabase_vault("NGROK_AUTHTOKEN", token, "Ngrok tunneling auth token")
            return True
        else:
            print(f"❌ Failed to configure ngrok: {stderr}")
            return False
    return False

def setup_langsmith():
    """Setup LangSmith API key."""
    print("\n" + "=" * 55)
    print("LANGSMITH SETUP")
    print("=" * 55)
    print("\nLangSmith provides monitoring and tracing for AI agents.")
    print("Get your API key from: https://smith.langchain.com/settings")
    
    key = input("\nEnter LangSmith API key (or press Enter to skip): ").strip()
    
    if key:
        add_to_supabase_vault("LANGSMITH_API_KEY", key, "LangSmith tracing API key")
        
        # Also set project name
        project = input("Enter project name [beeai-hive-999]: ").strip() or "beeai-hive-999"
        add_to_env("LANGSMITH_PROJECT", project)
        
        return True
    return False

def setup_openai():
    """Setup OpenAI API key."""
    print("\n" + "=" * 55)
    print("OPENAI SETUP")
    print("=" * 55)
    print("\nOpenAI provides GPT-4 and GPT-3.5 for cloud backend.")
    print("Get your API key from: https://platform.openai.com/api-keys")
    
    key = input("\nEnter OpenAI API key (or press Enter to skip): ").strip()
    
    if key:
        add_to_supabase_vault("OPENAI_API_KEY", key, "OpenAI API key for GPT models")
        return True
    return False

def setup_zoho():
    """Setup Zoho Mail credentials."""
    print("\n" + "=" * 55)
    print("ZOHO MAIL SETUP")
    print("=" * 55)
    print("\nZoho Mail provides email services for the Mantis agent.")
    print("Domain: bakerstreetbandits.work.gd")
    print("Verification Code: 41845428")
    
    email = input("\nEnter Zoho email (e.g., hive@bakerstreetbandits.work.gd): ").strip()
    password = input("Enter Zoho app password: ").strip()
    
    if email and password:
        add_to_supabase_vault("MANTIS_EMAIL_ADDRESS", email, "Zoho Mail email address")
        add_to_supabase_vault("MANTIS_EMAIL_PASSWORD", password, "Zoho Mail app password")
        add_to_env("MANTIS_EMAIL_PROVIDER", "zoho")
        return True
    return False

def view_status():
    """View current configuration status."""
    print("\n" + "=" * 55)
    print("CURRENT CONFIGURATION STATUS")
    print("=" * 55)
    
    env_path = Path.home() / ".env"
    secrets = {
        "NGROK_AUTHTOKEN": "Not set",
        "LANGSMITH_API_KEY": "Not set",
        "OPENAI_API_KEY": "Not set",
        "ANTHROPIC_API_KEY": "Not set",
        "MANTIS_EMAIL_ADDRESS": "Not set",
        "MANTIS_EMAIL_PASSWORD": "Not set",
    }
    
    if env_path.exists():
        content = env_path.read_text()
        for key in secrets.keys():
            for line in content.split('\n'):
                if line.startswith(f"export {key}="):
                    value = line.split('=', 1)[1]
                    secrets[key] = f"{value[:10]}..." if len(value) > 10 else value
    
    print("\nSecrets in ~/.env:")
    for key, value in secrets.items():
        status = "✅ Set" if value != "Not set" else "❌ Not set"
        print(f"  {key:25s}: {status}")
    
    # Check Supabase
    if check_supabase():
        print("\n✅ Supabase project initialized")
    else:
        print("\n⚠️  Supabase project not initialized")
        print("   Run: supabase init")
    
    # Check ngrok
    success, _, _ = run_command("which ngrok")
    if success:
        print("✅ Ngrok CLI installed")
    else:
        print("❌ Ngrok CLI not installed")

def export_env():
    """Export all secrets to current shell."""
    env_path = Path.home() / ".env"
    if env_path.exists():
        print("\n📤 Loading environment variables...")
        # Source the file
        os.system(f"source {env_path}")
        print("✅ Environment loaded")
        print("\nTo load manually, run:")
        print(f"  source {env_path}")
    else:
        print("❌ No .env file found")

def main():
    """Main interactive menu."""
    print("""
╔════════════════════════════════════════════════════════════════╗
║     🐝 HIVE 999 - Unified Secrets Manager                       ║
╚════════════════════════════════════════════════════════════════╝
""")
    
    while True:
        print("\n" + "=" * 55)
        print("MAIN MENU")
        print("=" * 55)
        print("\n  1. Complete Setup (Ngrok + LangSmith + OpenAI + Zoho)")
        print("  2. Setup Ngrok (for Zoho verification)")
        print("  3. Setup LangSmith")
        print("  4. Setup OpenAI")
        print("  5. Setup Zoho Mail")
        print("  6. View Status")
        print("  7. Export .env to current shell")
        print("  8. Start Zoho verification server")
        print("  9. Exit")
        print("")
        
        choice = input("Select option (1-9): ").strip()
        
        if choice == "1":
            setup_ngrok()
            setup_langsmith()
            setup_openai()
            setup_zoho()
            print("\n✅ Complete setup finished!")
            print("Run: source ~/.env")
            
        elif choice == "2":
            setup_ngrok()
            
        elif choice == "3":
            setup_langsmith()
            
        elif choice == "4":
            setup_openai()
            
        elif choice == "5":
            setup_zoho()
            
        elif choice == "6":
            view_status()
            
        elif choice == "7":
            export_env()
            
        elif choice == "8":
            print("\n🚀 Starting Zoho verification with ngrok...")
            os.system("./scripts/ngrok_zoho_verify.sh")
            
        elif choice == "9":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("\n❌ Invalid option")

if __name__ == "__main__":
    main()
