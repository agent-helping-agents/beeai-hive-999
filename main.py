#!/usr/bin/env python3
"""
Hive 999 — CLI/REPL entrypoint.

Usage:
    python main.py              # Interactive TUI
    python main.py --repl       # Simple REPL (no TUI)
    python main.py --non-interactive   # For systemd (reads stdin)
    python main.py --query "..."       # Single query, then exit
    python main.py --platform openrouter  # Specify inference platform
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from backend.inference_router import InferencePlatform


async def repl_mode(platform: Optional[InferencePlatform] = None) -> None:
    """Simple line-based REPL without TUI."""
    from agents.queen_bee.orchestrator import create_queen_bee

    print("🐝 Hive 999 — Queen Bee REPL")
    print("   Type 'exit' to quit.\n")

    queen = create_queen_bee(platform)

    while True:
        try:
            query = input("👑 > ")
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye from the Hive!")
            break

        query = query.strip()
        if not query:
            continue
        if query.lower() in ("exit", "quit", ":q"):
            print("👋 Goodbye from the Hive!")
            break

        try:
            result = await queen.run(query)
            print(f"\n{result.result.text}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")


async def single_query(
    query: str, platform: Optional[InferencePlatform] = None
) -> None:
    """Run a single query and exit."""
    from agents.queen_bee.orchestrator import create_queen_bee

    queen = create_queen_bee(platform)
    result = await queen.run(query)
    print(result.output_structured.response)


async def non_interactive_mode(platform: Optional[InferencePlatform] = None) -> None:
    """Read queries from stdin, one per line. For systemd usage."""
    from agents.queen_bee.orchestrator import create_queen_bee

    queen = create_queen_bee(platform)
    print("🐝 Hive 999 — non-interactive mode (reading stdin)")

    for line in sys.stdin:
        query = line.strip()
        if not query:
            continue
        try:
            result = await queen.run(query)
            print(f"RESULT: {result.result.text}", flush=True)
        except Exception as e:
            print(f"ERROR: {e}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Hive 999 — BeeAI Multi-Agent System")
    parser.add_argument("--repl", action="store_true", help="Simple REPL mode")
    parser.add_argument(
        "--non-interactive", action="store_true", help="Stdin mode for systemd"
    )
    parser.add_argument("--query", type=str, help="Single query, then exit")
    parser.add_argument(
        "--platform",
        type=str,
        default=None,
        help="Inference platform to use (openrouter, chutes, render, fortytwo, ollama)",
    )
    args = parser.parse_args()

    # Parse platform argument
    platform = None
    if args.platform:
        try:
            platform = InferencePlatform(args.platform.lower())
        except ValueError:
            print(f"❌ Invalid platform: {args.platform}")
            print("Available platforms: openrouter, chutes, render, fortytwo, ollama")
            sys.exit(1)

    if args.query:
        asyncio.run(single_query(args.query, platform))
    elif args.non_interactive:
        asyncio.run(non_interactive_mode(platform))
    elif args.repl:
        asyncio.run(repl_mode(platform))
    else:
        # Full TUI
        from tui import main as tui_main

        tui_main(platform=platform)


if __name__ == "__main__":
    main()
