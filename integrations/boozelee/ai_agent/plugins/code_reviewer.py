"""
Code Reviewer Plugin
---------------------
Sends a git diff to Gemini for a quick code review.
"""

import subprocess

from camel.agents import ChatAgent
from camel.models import ModelFactory


def run(args=None):
    """Review the current git diff using Gemini."""
    print("  [Code Reviewer] Getting diff...")

    diff = subprocess.getoutput("git diff")
    if not diff:
        diff = subprocess.getoutput("git diff --cached")
    if not diff:
        print("  [Code Reviewer] No changes to review.")
        return {"review": "No changes found."}

    # Truncate large diffs
    if len(diff) > 6000:
        diff = diff[:6000] + "\n\n[...truncated...]"

    model = ModelFactory.create(
        model_platform="google",
        model_type="gemini-1.5-flash",
    )
    reviewer = ChatAgent(
        system_message=(
            "You are a code reviewer. Given a git diff, provide:\n"
            "1. Summary of changes\n"
            "2. Potential bugs or issues\n"
            "3. Style suggestions\n"
            "Be concise and actionable."
        ),
        model=model,
    )

    try:
        response = reviewer.step(f"Review this diff:\n\n```\n{diff}\n```")
        review = response.msg.content
        print(f"\n  [Code Reviewer] Review:\n{review}")
        return {"review": review}
    except Exception as e:
        print(f"  [Code Reviewer] Error: {e}")
        return {"review": f"Error: {e}"}
