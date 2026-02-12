"""
Repo Scanner Plugin
--------------------
Uses gh CLI to scan a repo for useful info:
  - Open issues, PRs, recent activity
  - README summary
"""

import subprocess
import json


def run(args=None):
    """Scan a GitHub repo for key info."""
    repo = (args or {}).get("repo", "")
    if not repo:
        print("  [Repo Scanner] No repo specified. Pass {'repo': 'owner/name'}")
        return {}

    print(f"  [Repo Scanner] Scanning {repo}...")
    results = {}

    # Open issues count
    issues_raw = subprocess.getoutput(
        f'gh issue list --repo {repo} --state open --json number --limit 100'
    )
    try:
        issues = json.loads(issues_raw)
        results["open_issues"] = len(issues)
        print(f"    Open issues: {len(issues)}")
    except json.JSONDecodeError:
        results["open_issues"] = "error"

    # Open PRs
    prs_raw = subprocess.getoutput(
        f'gh pr list --repo {repo} --state open --json number --limit 100'
    )
    try:
        prs = json.loads(prs_raw)
        results["open_prs"] = len(prs)
        print(f"    Open PRs: {len(prs)}")
    except json.JSONDecodeError:
        results["open_prs"] = "error"

    # Recent releases
    releases_raw = subprocess.getoutput(
        f'gh release list --repo {repo} --limit 3 --json tagName,publishedAt 2>/dev/null'
    )
    try:
        releases = json.loads(releases_raw)
        results["recent_releases"] = releases
        for r in releases:
            print(f"    Release: {r.get('tagName')} ({r.get('publishedAt', '')[:10]})")
    except json.JSONDecodeError:
        results["recent_releases"] = []

    return results
