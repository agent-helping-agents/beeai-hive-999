"""Integration bridge between Terminal 221b and BeeAI Hive 999."""

from terminal_221b.integration.hive_bridge import (
    register_with_tui,
    DetectiveMode,
    handle_221b_command,
)

__all__ = [
    "register_with_tui",
    "DetectiveMode",
    "handle_221b_command",
]
