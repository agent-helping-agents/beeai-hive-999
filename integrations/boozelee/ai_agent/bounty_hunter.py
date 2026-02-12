#!/usr/bin/env python3
"""
Bounty Hunter Agent - Enhanced
-------------------------------
Multi-mode bounty hunter with Claude/Gemini integration:
  1. Scan repos for bounty issues
  2. Analyze issue complexity and requirements
  3. Generate solution proposals
  4. Auto-comment on issues
  5. Track bounty earnings
"""

import subprocess
import sys
import json
import os
import argparse
from datetime import datetime

try:
    from camel.agents import ChatAgent
    from camel.models import ModelFactory
    CAMEL_AVAILABLE = True
except ImportError:
    CAMEL_AVAILABLE = False

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


def create_solver(use_claude=False):
    """Create bounty solver agent using Claude or Gemini."""
    if use_claude and ANTHROPIC_AVAILABLE and os.getenv("ANTHROPIC_API_KEY"):
        return ClaudeSolver()
    elif CAMEL_AVAILABLE:
        model = ModelFactory.create(
            model_platform="google",
            model_type="gemini-1.5-flash",
        )
        return ChatAgent(
            system_message=(
                "You are a bounty solver. Given a GitHub issue with its comments, "
                "analyze the problem and produce:\n"
                "1. A clear summary of the bug/feature\n"
                "2. Root cause analysis\n"
                "3. A concrete code fix or implementation plan\n"
                "4. Files that likely need changes\n"
                "Keep responses actionable and specific."
            ),
            model=model,
        )
    else:
        raise RuntimeError("No AI backend available. Install camel-ai or anthropic.")


class ClaudeSolver:
    """Claude-powered bounty solver."""

    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def step(self, prompt):
        """Analyze and solve bounty issue."""
        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4096,
            system=(
                "You are an expert bounty hunter analyzing GitHub issues. "
                "Provide actionable solutions with:\n"
                "1. Problem summary\n"
                "2. Root cause analysis\n"
                "3. Implementation plan\n"
                "4. Estimated complexity (easy/medium/hard)\n"
                "5. Required skills/technologies\n"
                "Be specific and technical."
            ),
            messages=[{"role": "user", "content": prompt}]
        )

        class Response:
            def __init__(self, content):
                self.content = content

            class Msg:
                def __init__(self, content):
                    self.content = content

            @property
            def msg(self):
                return self.Msg(self.content)

        return Response(response.content[0].text)


def list_bounty_issues(repo, labels=None):
    """List open issues from a repo, optionally filtered by labels."""
    label_flag = ""
    if labels:
        label_flag = " ".join(f'--label "{l}"' for l in labels)
    cmd = f'gh issue list --repo {repo} --state open {label_flag} --json number,title,labels,url --limit 20'
    output = run_cmd(cmd)
    if not output:
        return []
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        print(f"  Failed to parse issues: {output[:200]}")
        return []


def get_issue_details(repo, issue_number):
    """Get full issue body and comments."""
    # Get issue body
    body_cmd = f'gh issue view {issue_number} --repo {repo} --json title,body,labels,comments'
    output = run_cmd(body_cmd)
    if not output:
        return None
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        print(f"  Failed to parse issue #{issue_number}")
        return None


def solve_bounty(repo, issue_number):
    """Read an issue + comments and generate a solution."""
    print(f"\n{'=' * 50}")
    print(f"  BOUNTY HUNTER - {repo} #{issue_number}")
    print(f"{'=' * 50}")

    issue = get_issue_details(repo, issue_number)
    if not issue:
        print("  Could not fetch issue details.")
        return None

    print(f"  Title: {issue.get('title', 'N/A')}")

    labels = [l.get("name", "") for l in issue.get("labels", [])]
    print(f"  Labels: {', '.join(labels)}")

    comments = issue.get("comments", [])
    print(f"  Comments: {len(comments)}")

    # Build context for the solver
    context_parts = [
        f"## Issue #{issue_number}: {issue.get('title', '')}",
        f"Labels: {', '.join(labels)}",
        f"\n### Description\n{issue.get('body', 'No description')}",
    ]
    for i, comment in enumerate(comments):
        author = comment.get("author", {}).get("login", "unknown")
        body = comment.get("body", "")
        context_parts.append(f"\n### Comment {i+1} by @{author}\n{body}")

    full_context = "\n".join(context_parts)

    # Truncate if massive
    if len(full_context) > 8000:
        full_context = full_context[:8000] + "\n\n[...truncated...]"

    print("\n  Sending to solver agent...")
    solver = create_solver()
    try:
        response = solver.step(
            f"Analyze this GitHub bounty issue and provide a solution:\n\n{full_context}"
        )
        solution = response.msg.content
        print(f"\n{'=' * 50}")
        print("  SOLUTION")
        print(f"{'=' * 50}")
        print(solution)
        return solution
    except Exception as e:
        print(f"  Solver error: {e}")
        return None


def scan_repos(repos, labels=None):
    """Scan multiple repos for bounty issues."""
    if labels is None:
        labels = ["bounty", "reward", "bug-bounty", "help wanted", "good first issue"]

    print("\n  Scanning for bounty issues...")
    for repo in repos:
        print(f"\n  Repo: {repo}")
        issues = list_bounty_issues(repo, labels)
        if not issues:
            print("    No matching issues found.")
            continue
        for issue in issues:
            print(f"    #{issue['number']}: {issue['title']}")
            issue_labels = [l.get("name", "") for l in issue.get("labels", [])]
            print(f"      Labels: {', '.join(issue_labels)}")


def analyze_complexity(issue_data):
    """Analyze bounty complexity using AI."""
    solver = create_solver(use_claude=True)

    context = f"""
    Issue: {issue_data.get('title', '')}
    Labels: {', '.join([l.get('name', '') for l in issue_data.get('labels', [])])}
    Description: {issue_data.get('body', '')}

    Rate this issue's complexity (easy/medium/hard) and list required skills.
    """

    response = solver.step(context)
    return response.msg.content


def post_comment(repo, issue_number, comment_body):
    """Post a comment on a GitHub issue."""
    cmd = f'gh issue comment {issue_number} --repo {repo} --body "{comment_body}"'
    output = run_cmd(cmd)
    return output


def main():
    parser = argparse.ArgumentParser(description="Bounty Hunter Agent")
    parser.add_argument("--mode", choices=["scan", "analyze", "propose", "solve"], required=True)
    parser.add_argument("--issue", type=int, help="Issue number")
    parser.add_argument("--repo", help="Repository (owner/name)")
    parser.add_argument("--repos", nargs="+", help="Multiple repositories to scan")
    parser.add_argument("--auto-comment", action="store_true", help="Auto-comment on issues")

    args = parser.parse_args()

    if args.mode == "scan":
        repos = args.repos or ["anthropics/anthropic-sdk-python", "langchain-ai/langchain"]
        scan_repos(repos)

    elif args.mode == "analyze":
        if not args.issue:
            print("Error: --issue required for analyze mode")
            return
        repo = args.repo or os.getenv("GITHUB_REPOSITORY", "owner/repo")
        issue = get_issue_details(repo, args.issue)
        if issue:
            analysis = analyze_complexity(issue)
            print(f"\n=== COMPLEXITY ANALYSIS ===\n{analysis}")

            if args.auto_comment:
                comment = f"## 🤖 AI Bounty Analysis\n\n{analysis}\n\n*Analyzed by BountyHunter Bot*"
                post_comment(repo, args.issue, comment)

    elif args.mode == "propose":
        if not args.issue:
            print("Error: --issue required for propose mode")
            return
        repo = args.repo or os.getenv("GITHUB_REPOSITORY")
        solution = solve_bounty(repo, args.issue)

        if solution and args.auto_comment:
            comment = f"## 💡 Solution Proposal\n\n{solution}\n\n*Generated by BountyHunter Bot*"
            post_comment(repo, args.issue, comment)

    elif args.mode == "solve":
        if not args.issue or not args.repo:
            print("Error: --issue and --repo required for solve mode")
            return
        solve_bounty(args.repo, args.issue)


if __name__ == "__main__":
    main()
