#!/usr/bin/env python3
"""
Super Claude - Main Launcher
------------------------------
Central hub for the Watcher Council, Bounty Hunter, and Plugins.

Usage:
  python3 super_claude.py               # Interactive menu
  python3 super_claude.py council       # Start watcher council
  python3 super_claude.py bounty        # Bounty hunter mode
  python3 super_claude.py plugin <name> # Run a plugin
  python3 super_claude.py plugins       # List plugins
"""

import sys
import os

# Ensure we can import from the project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def show_menu():
    print()
    print("=" * 50)
    print("       SUPER CLAUDE COMMAND CENTER")
    print("=" * 50)
    print()
    print("  1) Start Watcher Council (auto-sync)")
    print("  2) Bounty Hunter (scan/solve issues)")
    print("  3) Code Review (review current diff)")
    print("  4) Git Guard (scan for secrets)")
    print("  5) Repo Scanner (scan a GitHub repo)")
    print("  6) List all plugins")
    print("  7) Run a plugin by name")
    print("  q) Quit")
    print()
    return input("  Choose> ").strip()


def main():
    # Direct command mode
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "council":
            from council_setup import council_loop
            council_loop()

        elif cmd == "bounty":
            from bounty_hunter import main as bounty_main
            # Pass remaining args
            sys.argv = sys.argv[1:]
            bounty_main()

        elif cmd == "plugin" and len(sys.argv) > 2:
            from plugins import run_plugin
            plugin_name = sys.argv[2]
            plugin_args = {}
            # Simple key=value parsing
            for arg in sys.argv[3:]:
                if "=" in arg:
                    k, v = arg.split("=", 1)
                    plugin_args[k] = v
            run_plugin(plugin_name, plugin_args)

        elif cmd == "plugins":
            from plugins import list_plugins
            print("\n  Available plugins:")
            for p in list_plugins():
                print(f"    - {p}")
            print()

        else:
            print(f"  Unknown command: {cmd}")
            print("  Try: council, bounty, plugin, plugins")
        return

    # Interactive menu mode
    while True:
        choice = show_menu()

        if choice == "1":
            from council_setup import council_loop
            council_loop()

        elif choice == "2":
            repo = input("  Repo (owner/name): ").strip()
            action = input("  Action (scan/solve/comments): ").strip()
            if action == "scan":
                from bounty_hunter import scan_repos
                scan_repos([repo])
            elif action in ("solve", "comments"):
                issue = input("  Issue #: ").strip()
                if action == "solve":
                    from bounty_hunter import solve_bounty
                    solve_bounty(repo, int(issue))
                else:
                    from bounty_hunter import get_issue_details
                    details = get_issue_details(repo, int(issue))
                    if details:
                        for i, c in enumerate(details.get("comments", [])):
                            author = c.get("author", {}).get("login", "?")
                            print(f"\n  --- @{author} ---")
                            print(f"  {c.get('body', '')[:500]}")

        elif choice == "3":
            from plugins import run_plugin
            run_plugin("code_reviewer")

        elif choice == "4":
            from plugins import run_plugin
            run_plugin("git_guard")

        elif choice == "5":
            repo = input("  Repo (owner/name): ").strip()
            from plugins import run_plugin
            run_plugin("repo_scanner", {"repo": repo})

        elif choice == "6":
            from plugins import list_plugins
            print("\n  Available plugins:")
            for p in list_plugins():
                print(f"    - {p}")

        elif choice == "7":
            name = input("  Plugin name: ").strip()
            from plugins import run_plugin
            run_plugin(name)

        elif choice in ("q", "Q", "quit", "exit"):
            print("  Goodbye.")
            break

        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    main()
