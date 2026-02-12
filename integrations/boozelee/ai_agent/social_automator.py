#!/usr/bin/env python3
"""
Social Automation Bot
---------------------
Intelligent GitHub social engagement using Claude:
  1. Smart replies to issue/PR comments
  2. Daily community engagement
  3. Mention tracking and responses
  4. Automated PR reviews
  5. Weekly summaries
"""

import subprocess
import json
import os
import argparse
from datetime import datetime, timedelta

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


def run_cmd(command):
    """Run shell command, return stdout."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and result.stderr:
        print(f"  [cmd error] {result.stderr[:200]}")
    return result.stdout.strip()


class SocialBot:
    """AI-powered social engagement bot."""

    def __init__(self):
        if not ANTHROPIC_AVAILABLE or not os.getenv("ANTHROPIC_API_KEY"):
            raise RuntimeError("Anthropic API key required")
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.repo = os.getenv("GITHUB_REPOSITORY", "owner/repo")

    def generate_response(self, context, prompt):
        """Generate contextual response using Claude."""
        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            system=(
                "You are a helpful GitHub bot assistant. "
                "Provide friendly, professional, and technical responses. "
                "Be concise but helpful. Use markdown formatting. "
                "Sign off with: *- Automated by AI Social Bot*"
            ),
            messages=[
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nPrompt:\n{prompt}"
                }
            ]
        )
        return response.content[0].text

    def get_recent_issues(self, days=7):
        """Get recent issues."""
        since = (datetime.now() - timedelta(days=days)).isoformat()
        cmd = f'gh issue list --repo {self.repo} --json number,title,body,createdAt,comments --limit 50'
        output = run_cmd(cmd)
        if not output:
            return []
        try:
            issues = json.loads(output)
            return [i for i in issues if i.get('createdAt', '') >= since]
        except json.JSONDecodeError:
            return []

    def get_comment(self, comment_id):
        """Get comment details."""
        # Note: gh CLI doesn't have direct comment lookup, need to implement
        # For now, return placeholder
        return {"body": "Comment content here", "author": "user"}

    def reply_to_mention(self, comment_id, issue_number):
        """Smart reply to a mention."""
        # Get issue context
        cmd = f'gh issue view {issue_number} --repo {self.repo} --json title,body,comments'
        output = run_cmd(cmd)
        if not output:
            print("  Could not fetch issue")
            return

        try:
            issue = json.loads(output)
        except json.JSONDecodeError:
            print("  Failed to parse issue")
            return

        context = f"""
        Issue: {issue.get('title', '')}
        Description: {issue.get('body', '')}
        Recent comments: {len(issue.get('comments', []))} total
        """

        prompt = "Generate a helpful reply acknowledging the mention and offering assistance."

        response = self.generate_response(context, prompt)

        # Post comment
        cmd = f'gh issue comment {issue_number} --repo {self.repo} --body "{response}"'
        run_cmd(cmd)
        print(f"  ✓ Replied to mention on issue #{issue_number}")

    def engage_daily(self):
        """Daily community engagement."""
        print("\n=== DAILY COMMUNITY ENGAGEMENT ===")

        # Get issues needing attention
        cmd = f'gh issue list --repo {self.repo} --label "help wanted" --json number,title --limit 10'
        output = run_cmd(cmd)
        if not output:
            print("  No issues found")
            return

        try:
            issues = json.loads(output)
        except json.JSONDecodeError:
            print("  Failed to parse issues")
            return

        for issue in issues[:3]:  # Engage with top 3
            number = issue['number']
            title = issue['title']

            context = f"Issue #{number}: {title}"
            prompt = "Generate an encouraging comment offering help or asking clarifying questions."

            response = self.generate_response(context, prompt)

            cmd = f'gh issue comment {number} --repo {self.repo} --body "{response}"'
            run_cmd(cmd)
            print(f"  ✓ Engaged with issue #{number}")

    def generate_weekly_summary(self):
        """Generate weekly activity summary."""
        print("\n=== WEEKLY SUMMARY ===")

        # Get issues from past week
        issues = self.get_recent_issues(days=7)

        summary_parts = [
            "## 📊 Weekly Activity Summary",
            f"**Period:** {(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}",
            f"\n### Issues ({len(issues)} total)",
        ]

        opened = [i for i in issues if 'createdAt' in i]
        summary_parts.append(f"- Opened: {len(opened)}")

        # Generate AI summary
        context = f"Issues opened this week: {len(opened)}\n"
        prompt = "Generate a brief weekly summary highlighting key activities and trends."

        ai_summary = self.generate_response(context, prompt)
        summary_parts.append(f"\n### Highlights\n{ai_summary}")

        summary = "\n".join(summary_parts)
        print(summary)

        return summary


def main():
    parser = argparse.ArgumentParser(description="Social Automation Bot")
    parser.add_argument("--mode", choices=["reply", "engage", "summary"], required=True)
    parser.add_argument("--comment-id", help="Comment ID for reply mode")
    parser.add_argument("--issue-number", type=int, help="Issue number")
    parser.add_argument("--daily", action="store_true", help="Run daily engagement")

    args = parser.parse_args()

    bot = SocialBot()

    if args.mode == "reply":
        if not args.comment_id or not args.issue_number:
            print("Error: --comment-id and --issue-number required")
            return
        bot.reply_to_mention(args.comment_id, args.issue_number)

    elif args.mode == "engage":
        if args.daily:
            bot.engage_daily()
        else:
            print("Use --daily flag for daily engagement")

    elif args.mode == "summary":
        summary = bot.generate_weekly_summary()
        # Optionally post as issue
        if os.getenv("POST_ISSUE"):
            cmd = f'gh issue create --repo {bot.repo} --title "Weekly Summary {datetime.now().strftime("%Y-%m-%d")}" --body "{summary}"'
            run_cmd(cmd)


if __name__ == "__main__":
    main()
