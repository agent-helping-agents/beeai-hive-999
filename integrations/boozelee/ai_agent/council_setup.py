#!/usr/bin/env python3
"""
Super Claude Watcher Council
-----------------------------
Dual-agent system:
  - Scout (TinyLlama/Ollama): monitors git status locally
  - Engineer (Gemini): decides whether to push changes
Runs on a loop every 10 minutes.
"""

import subprocess
import time
import sys
import os

from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.messages import BaseMessage


def run_cmd(command):
    """Run a shell command and return output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip() + result.stderr.strip()


def create_scout():
    """Local scout agent using TinyLlama via Ollama."""
    model = ModelFactory.create(
        model_platform="ollama",
        model_type="tinyllama",
    )
    return ChatAgent(
        system_message=(
            "You are Scout, a local code monitor. "
            "When asked, report the current git status concisely. "
            "Focus on: new files, modified files, and deletions."
        ),
        model=model,
    )


def create_engineer():
    """Cloud engineer agent using Gemini."""
    model = ModelFactory.create(
        model_platform="google",
        model_type="gemini-1.5-flash",
    )
    return ChatAgent(
        system_message=(
            "You are Engineer, a senior developer. "
            "Given a git status report, decide the action:\n"
            "- Reply PUSH_NOW if changes should be committed and pushed.\n"
            "- Reply WAIT if changes are incomplete or risky.\n"
            "- Always explain your reasoning in one line."
        ),
        model=model,
    )


def council_loop(interval=600, one_shot=False):
    """Main watcher council loop."""
    print("=" * 50)
    print("  SUPER CLAUDE WATCHER COUNCIL")
    print("  Scout: TinyLlama (local)")
    print("  Engineer: Gemini (cloud)")
    print("=" * 50)

    scout = create_scout()
    engineer = create_engineer()

    while True:
        print(f"\n[{time.strftime('%H:%M:%S')}] Council convening...")

        # 1. Get actual git status
        git_status = run_cmd("git status --short")
        git_branch = run_cmd("git branch --show-current")

        if not git_status:
            print("  Clean working tree. Nothing to do.")
        else:
            print(f"  Branch: {git_branch}")
            print(f"  Changes detected:\n    {git_status.replace(chr(10), chr(10) + '    ')}")

            # 2. Scout analyzes
            scout_prompt = (
                f"Current branch: {git_branch}\n"
                f"Git status output:\n{git_status}\n"
                "Summarize what changed and if it looks ready to commit."
            )
            try:
                scout_response = scout.step(scout_prompt)
                scout_report = scout_response.msg.content
                print(f"  Scout says: {scout_report[:200]}")
            except Exception as e:
                scout_report = f"Scout offline: {e}. Raw status: {git_status}"
                print(f"  Scout error (using raw status): {e}")

            # 3. Engineer decides
            try:
                eng_prompt = f"Scout report: {scout_report}\nShould we push? Reply PUSH_NOW or WAIT."
                eng_response = engineer.step(eng_prompt)
                decision = eng_response.msg.content
                print(f"  Engineer says: {decision[:200]}")

                if "PUSH_NOW" in decision.upper():
                    print("  Executing: git add, commit, push...")
                    commit_msg = f"Auto-sync: {time.strftime('%Y-%m-%d %H:%M')}"
                    add_result = run_cmd("git add -A")
                    commit_result = run_cmd(f'git commit -m "{commit_msg}"')
                    push_result = run_cmd("git push")
                    print(f"  Commit: {commit_result[:100]}")
                    print(f"  Push: {push_result[:100]}")
                else:
                    print("  Engineer says WAIT. Skipping push.")
            except Exception as e:
                print(f"  Engineer error: {e}")

        if one_shot:
            break

        print(f"  Council sleeping {interval // 60} minutes...")
        time.sleep(interval)


if __name__ == "__main__":
    one_shot = "--once" in sys.argv
    interval = 600
    for arg in sys.argv[1:]:
        if arg.startswith("--interval="):
            interval = int(arg.split("=")[1])
    council_loop(interval=interval, one_shot=one_shot)
