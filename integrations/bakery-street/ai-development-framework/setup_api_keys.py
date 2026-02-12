#!/usr/bin/env python3
"""
API Key Configuration Script for AIOS Orchestrator
Helps you set up the necessary API keys for production deployment
"""

import os
import getpass
from pathlib import Path

def setup_api_keys():
    """Interactive setup for API keys"""
    
    print("🔑 AIOS Orchestrator API Key Configuration")
    print("=" * 60)
    print("This script will help you configure your API keys for production deployment.")
    print("You'll need API keys for the AI services you want to use.\n")
    
    # Check if .env.production exists
    env_file = ".env.production"
    if not os.path.exists(env_file):
        print("❌ .env.production file not found!")
        return False
    
    # Read current configuration
    with open(env_file, 'r') as f:
        current_config = f.read()
    
    print("📋 Current Configuration:")
    print("-" * 40)
    
    # Parse and display current values
    config_lines = current_config.strip().split('\n')
    config_dict = {}
    
    for line in config_lines:
        if '=' in line:
            key, value = line.split('=', 1)
            config_dict[key] = value
            if 'API_KEY' in key or 'SECRET_KEY' in key:
                if 'your_' in value:
                    print(f"   {key}: [NOT SET]")
                else:
                    print(f"   {key}: [SET]")
            else:
                print(f"   {key}: {value}")
    
    print("\n🔑 API Key Configuration Options:")
    print("1. OpenAI API Key (for GPT models)")
    print("2. Anthropic API Key (for Claude models)")
    print("3. Google API Key (for PaLM/Gemini models)")
    print("4. Custom AIOS API Key")
    print("5. Skip API key setup for now")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == '5':
        print("✅ Skipping API key setup. You can configure them manually later.")
        return True
    
    # Update configuration based on choice
    if choice == '1':
        print("\n🔑 OpenAI API Key Setup:")
        print("Get your API key from: https://platform.openai.com/api-keys")
        api_key = getpass.getpass("Enter your OpenAI API key: ")
        if api_key:
            config_dict['CREWAI_OPENAI_API_KEY'] = api_key
            print("✅ OpenAI API key configured!")
    
    elif choice == '2':
        print("\n🔑 Anthropic API Key Setup:")
        print("Get your API key from: https://console.anthropic.com/")
        api_key = getpass.getpass("Enter your Anthropic API key: ")
        if api_key:
            config_dict['CREWAI_ANTHROPIC_API_KEY'] = api_key
            print("✅ Anthropic API key configured!")
    
    elif choice == '3':
        print("\n🔑 Google API Key Setup:")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        api_key = getpass.getpass("Enter your Google API key: ")
        if api_key:
            config_dict['CREWAI_GOOGLE_API_KEY'] = api_key
            print("✅ Google API key configured!")
    
    elif choice == '4':
        print("\n🔑 AIOS API Key Setup:")
        print("This is for your custom AIOS system authentication")
        api_key = getpass.getpass("Enter your AIOS API key: ")
        secret_key = getpass.getpass("Enter your AIOS secret key: ")
        if api_key:
            config_dict['AIOS_API_KEY'] = api_key
        if secret_key:
            config_dict['AIOS_SECRET_KEY'] = secret_key
        print("✅ AIOS API keys configured!")
    
    # Generate new configuration
    new_config = ""
    for key, value in config_dict.items():
        new_config += f"{key}={value}\n"
    
    # Write updated configuration
    with open(env_file, 'w') as f:
        f.write(new_config)
    
    print(f"\n✅ Configuration updated in {env_file}")
    
    # Show what's configured
    print("\n📋 Updated Configuration Status:")
    print("-" * 40)
    for key, value in config_dict.items():
        if 'API_KEY' in key or 'SECRET_KEY' in key:
            if 'your_' in value:
                print(f"   {key}: [NOT SET]")
            else:
                print(f"   {key}: [SET]")
        else:
            print(f"   {key}: {value}")
    
    return True

def show_next_steps():
    """Show next steps after API key configuration"""
    
    print("\n🚀 Next Steps:")
    print("=" * 60)
    print("1. ✅ API Keys configured")
    print("2. 🔄 Set up databases (PostgreSQL + Redis)")
    print("3. 🐳 Deploy with Docker")
    print("4. 🧠 Start building your AI system!")
    
    print("\n📚 Helpful Commands:")
    print("-" * 30)
    print("• Check Docker: docker --version")
    print("• Start services: docker-compose up -d")
    print("• View logs: docker-compose logs -f")
    print("• Stop services: docker-compose down")
    
    print("\n🌐 Access Points (after deployment):")
    print("-" * 40)
    print("• AIOS Orchestrator: http://localhost:8000")
    print("• Grafana Dashboard: http://localhost:3000")
    print("• Prometheus Metrics: http://localhost:9090")

def main():
    """Main configuration function"""
    
    try:
        success = setup_api_keys()
        if success:
            show_next_steps()
            print("\n🎉 API Key configuration completed!")
            print("🚀 You're ready to deploy your AI system!")
        else:
            print("\n💥 API Key configuration failed!")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Configuration interrupted by user")
        print("You can run this script again later to configure API keys")
    except Exception as e:
        print(f"\n❌ Configuration failed: {e}")

if __name__ == "__main__":
    main()
