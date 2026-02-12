#!/usr/bin/env python3
"""
Bounty Finder - Find claimable bounties across GitHub
"""

import subprocess
import json
from datetime import datetime

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

# Popular repos with bounties
BOUNTY_REPOS = [
    "ethereum/go-ethereum",
    "bitcoin/bitcoin",
    "microsoft/vscode",
    "tensorflow/tensorflow",
    "pytorch/pytorch",
    "langchain-ai/langchain",
    "anthropics/anthropic-sdk-python",
    "openai/openai-python",
    "huggingface/transformers",
    "vercel/next.js",
]

print("🎯 BOUNTY FINDER")
print("=" * 60)
print(f"Scanning {len(BOUNTY_REPOS)} repositories...\n")

total_found = 0

for repo in BOUNTY_REPOS:
    # Search for bounty issues
    cmd = f'gh search issues "repo:{repo} is:open label:bounty,bug-bounty,reward,help-wanted" --limit 5 --json number,title,labels,url,updatedAt 2>&1'
    output = run_cmd(cmd)

    try:
        issues = json.loads(output) if output and output != '[]' else []

        if issues:
            print(f"\n📦 {repo}")
            print("-" * 60)
            for issue in issues:
                num = issue.get('number', 'N/A')
                title = issue.get('title', 'No title')[:60]
                labels = [l['name'] for l in issue.get('labels', [])]
                url = issue.get('url', '')

                # Check for bounty indicators
                has_bounty = any(l in ['bounty', 'bug-bounty', 'reward'] for l in labels)
                indicator = "💰" if has_bounty else "🎯"

                print(f"  {indicator} #{num}: {title}")
                print(f"     Labels: {', '.join(labels[:3])}")
                print(f"     {url}")
                total_found += 1
    except json.JSONDecodeError:
        pass

print(f"\n{'=' * 60}")
print(f"✅ Found {total_found} potential bounties!")
print("\nNext steps:")
print("  1. Pick an issue from above")
print("  2. python bounty_hunter.py --mode analyze --repo REPO --issue NUM")
print("  3. python bounty_hunter.py --mode propose --repo REPO --issue NUM --auto-comment")
