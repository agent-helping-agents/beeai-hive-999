"""
Git Guard Plugin
-----------------
Checks for sensitive files before committing.
Scans for .env, credentials, API keys in staged files.
"""

import subprocess
import re

SENSITIVE_PATTERNS = [
    r'(?i)(api[_-]?key|secret|password|token)\s*[=:]\s*["\']?.+',
    r'(?i)AKIA[0-9A-Z]{16}',  # AWS access key
    r'ghp_[a-zA-Z0-9]{36}',   # GitHub PAT
    r'sk-[a-zA-Z0-9]{48}',    # OpenAI key
]

SENSITIVE_FILES = [".env", "credentials.json", ".secrets", "id_rsa", ".pem"]


def run(args=None):
    """Scan staged files for secrets before committing."""
    print("  [Git Guard] Scanning staged files for secrets...")

    staged = subprocess.getoutput("git diff --cached --name-only").strip().split("\n")
    staged = [f for f in staged if f]

    if not staged:
        print("  [Git Guard] No staged files.")
        return {"clean": True, "issues": []}

    issues = []

    for filename in staged:
        # Check filename
        for sf in SENSITIVE_FILES:
            if filename.endswith(sf) or sf in filename:
                issues.append(f"BLOCKED: Sensitive file staged: {filename}")

        # Check content
        try:
            content = subprocess.getoutput(f'git show ":{filename}" 2>/dev/null')
            for pattern in SENSITIVE_PATTERNS:
                matches = re.findall(pattern, content)
                if matches:
                    issues.append(f"WARNING: Possible secret in {filename}: pattern matched")
        except Exception:
            pass

    if issues:
        print("  [Git Guard] Issues found:")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print("  [Git Guard] All clear.")

    return {"clean": len(issues) == 0, "issues": issues}
