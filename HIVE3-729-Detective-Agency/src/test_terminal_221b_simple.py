#!/usr/bin/env python3
"""Test script to verify Terminal 221b integration without Solana validator."""

import asyncio
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from terminal_221b.integration.hive_bridge import (
    register_with_tui,
    handle_221b_command,
)


class MockState:
    """Mock TUI state for testing."""

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

    def add_notification(self, message, level):
        self.notifications.append({"message": message, "level": level})

    def set_art(self, art):
        self.art_content = art


async def test_221b_commands():
    """Test Terminal 221b commands that don't require Solana validator."""
    print("Testing Terminal 221b integration...\n")

    state = MockState()

    print("1. Testing register_with_tui...")
    registration = await register_with_tui(state)
    print(f"✅ Success: {len(registration['commands'])} commands registered")
    print(f"   Keybindings: {list(registration['keybindings'].keys())}")

    print("\n2. Testing handle_221b_command (status)...")
    result = await handle_221b_command("status", state)
    if "TERMINAL 221b STATUS" in result:
        print("✅ Success")
    else:
        print(f"❌ Failed: {result}")

    print("\n3. Testing handle_221b_command (help)...")
    result = await handle_221b_command("help", state)
    if "TERMINAL 221b - CONTROL CENTER" in result:
        print("✅ Success")
    else:
        print(f"❌ Failed: {result}")

    print("\n4. Testing handle_221b_command (invalid)...")
    result = await handle_221b_command("invalid", state)
    if "Unknown 221b command" in result:
        print("✅ Success")
    else:
        print(f"❌ Failed: {result}")

    print("\n✅ Terminal 221b integration test completed!")


async def main():
    await test_221b_commands()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
