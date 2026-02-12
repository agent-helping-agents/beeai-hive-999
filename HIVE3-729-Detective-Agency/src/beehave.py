#!/usr/bin/env python3
"""
BeeHave - Terminal 221b Detective Mode Command

A standalone command to launch Terminal 221b detective mode in the TUI.
"""

import sys
import os
import asyncio
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from terminal_221b.integration.hive_bridge import (
    register_with_tui,
    handle_221b_command,
    handle_detective_command,
    handle_investigate_command,
    handle_simulate_command,
    on_alt_d,
)
from terminal_221b.integration.hive_bridge import DetectiveMode, _detective_state


async def test_221b_commands():
    """Test Terminal 221b commands."""
    print("🕵️  BeeHave - Testing Terminal 221b Integration")
    print("=" * 50)
    print()

    # Check if Solana CLI is available
    solana_available = False
    try:
        result = await asyncio.create_subprocess_shell(
            "solana --version",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await result.communicate()
        solana_available = result.returncode == 0
    except:
        solana_available = False

    print(
        f"🔍 Solana CLI: {'✅ Available' if solana_available else '❌ Not available'}"
    )
    if not solana_available:
        print("⚠️  Solana CLI not found. Run 'python beehave.py install' to install.")
        print()

    # Create a mock state object for testing
    class MockState:
        def __init__(self):
            self.current_agent_name = "Queen Bee"
            self.current_model = "granite3.3:8b"
            self.mode = "queen"
            self.art_content = ""
            self.messages = []
            self.notifications = []

        def add_message(self, sender, content, agent_type=None):
            self.messages.append(
                {"sender": sender, "content": content, "agent_type": agent_type}
            )
            print(f"📨 {sender}: {content}")

        def add_notification(self, message, level):
            self.notifications.append({"message": message, "level": level})
            print(f"🔔 {level.upper()}: {message}")

        def set_art(self, art):
            self.art_content = art

    state = MockState()

    print()
    print("🔍 Testing command registration...")
    try:
        registration = await register_with_tui(state)
        print(f"✅ Success: {len(registration['commands'])} commands registered")
        print(f"   Keybindings: {list(registration['keybindings'].keys())}")
        print(f"   Art entries: {list(registration['art_entries'].keys())}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    print()
    print("🔍 Testing :221b status command...")
    try:
        result = await handle_221b_command("status", state)
        print("✅ Success:")
        print(result)
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    print()
    print("🔍 Testing :221b help command...")
    try:
        result = await handle_221b_command("help", state)
        print("✅ Success:")
        print(result)
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    if solana_available:
        print()
        print("🔍 Testing :detective command (Holmes)...")
        try:
            result = await handle_detective_command("holmes", state)
            print("✅ Success:")
            print(result)
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

        print()
        print("🔍 Testing :detective command (Watson)...")
        try:
            result = await handle_detective_command("watson", state)
            print("✅ Success:")
            print(result)
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

        print()
        print("🔍 Testing :221b mode command...")
        try:
            result = await handle_221b_command("mode mycroft", state)
            print("✅ Success:")
            print(result)
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    else:
        print()
        print(
            "⚠️  Skipping detective personality tests - Solana validator not available"
        )
        print(
            "   To run full detective tests, install Solana CLI: https://docs.solana.com/cli/install-solana-cli-tools"
        )

    print()
    print("🎯 Terminal 221b integration test completed!")
    print()
    print("To launch the full TUI with Terminal 221b integration, run:")
    print("  $ ./run.sh")
    print()
    print("Terminal 221b keybindings:")
    print("  Alt+D      - Switch to Detective Mode")
    print("  Alt+Shift+D - Cycle Detective Personalities")
    print()
    print("Terminal 221b commands:")
    print("  :221b status      - Show detective status")
    print("  :221b mode <p>    - Switch personality (holmes/watson/mycroft/irene)")
    print("  :detective <p>    - Switch detective personality")
    print("  :investigate <q>  - Start investigation")
    print("  :simulate <tx>    - Simulate transaction")

    return True


async def launch_221b_tui():
    """Launch the TUI directly into Terminal 221b mode."""
    print("🚀 Launching Terminal 221b Detective Mode...")
    print()

    from tui import main as tui_main
    import subprocess

    # Check if we're in a terminal
    if os.isatty(sys.stdin.fileno()):
        try:
            # Launch TUI with Terminal 221b integration
            print("📦 Starting BeeAI Hive 999 TUI...")
            print("⏳ Please wait while the agents initialize...")
            print()

            # Run the TUI
            await tui_main()

        except KeyboardInterrupt:
            print("\n👋 Goodbye from Terminal 221b!")
            return True
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback

            print(traceback.format_exc())
            return False
    else:
        print("❌ Error: TUI requires a terminal environment")
        print("Try running in a regular terminal window")
        return False


async def install_solana_cli():
    """Install Solana CLI."""
    print("📦 Installing Solana CLI...")
    print()

    # Check OS
    if sys.platform.startswith("linux"):
        print("🔍 Detecting Linux system...")
        print(
            'Running: sh -c "$(curl -sSfL https://release.solana.com/v1.18.15/install)"'
        )
        try:
            result = await asyncio.create_subprocess_shell(
                'sh -c "$(curl -sSfL https://release.solana.com/v1.18.15/install)"',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await result.communicate()

            if result.returncode == 0:
                print("✅ Solana CLI installed successfully!")
                print()
                print("⚠️  Please add Solana to your PATH:")
                print(
                    '   export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"'
                )
                print()
                print("Then verify installation with:")
                print("   solana --version")
                return True
            else:
                print(f"❌ Error: {stderr.decode()}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    elif sys.platform == "darwin":
        print("🍎 Detecting macOS...")
        print("Please install Solana CLI using one of these methods:")
        print()
        print("1. Using Homebrew:")
        print("   $ brew install solana")
        print()
        print("2. Using curl:")
        print('   $ sh -c "$(curl -sSfL https://release.solana.com/v1.18.15/install)"')
        print()
        print("3. From https://docs.solana.com/cli/install-solana-cli-tools")
        return False
    elif sys.platform == "win32":
        print("🪟 Detecting Windows...")
        print("Please install Solana CLI from:")
        print("   https://docs.solana.com/cli/install-solana-cli-tools#windows")
        return False
    else:
        print(f"❌ Unsupported OS: {sys.platform}")
        print("Please install Solana CLI manually from:")
        print("   https://docs.solana.com/cli/install-solana-cli-tools")
        return False


async def main():
    """Main entry point for BeeHave command."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            await test_221b_commands()
        elif sys.argv[1] == "install":
            await install_solana_cli()
        elif sys.argv[1] == "tui":
            await launch_221b_tui()
        elif sys.argv[1] == "help":
            print("Usage: python beehave.py [command]")
            print()
            print("Commands:")
            print("  test          - Test Terminal 221b commands")
            print("  install       - Install Solana CLI")
            print("  tui           - Launch TUI with Terminal 221b integration")
            print("  help          - Show this help message")
            print()
            print("Examples:")
            print("  $ python beehave.py test       # Test commands")
            print("  $ python beehave.py install    # Install Solana CLI")
            print("  $ python beehave.py tui        # Launch TUI")
        else:
            print(f"❌ Unknown command: {sys.argv[1]}")
            print("Try 'python beehave.py help' for available commands")
    else:
        await launch_221b_tui()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye from BeeHave!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        print(traceback.format_exc())
        sys.exit(1)
