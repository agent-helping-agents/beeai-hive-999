"""
Mantis Mail Agent — Stub implementation.

This module defines the interface for the Mantis email assistant.
Full implementation will add IMAP/SMTP connectivity, email parsing,
and automated report generation.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


@dataclass
class MantisConfig:
    """Configuration for the Mantis Mail agent."""
    imap_host: str = ""
    imap_port: int = 993
    smtp_host: str = ""
    smtp_port: int = 587
    email_address: str = ""
    # Credentials should come from environment variables
    use_tls: bool = True
    check_interval_minutes: int = 15
    # Templates
    monetization_template: str = "templates/monetization_email.md"
    weekly_report_template: str = "templates/weekly_report.md"
    github_repos: list[str] = field(default_factory=list)


class MantisMailAgent:
    """
    Stub Mantis Mail agent.

    Planned tools:
    - draft_monetization_email(partner, proposal) -> email draft
    - github_summary(repo, days=7) -> markdown summary
    - weekly_report() -> hive activity digest
    - send_email(to, subject, body) -> sent confirmation
    - check_inbox(filter) -> list of relevant emails
    """

    def __init__(self, config: MantisConfig | None = None) -> None:
        self.config = config or MantisConfig()
        self._connected = False

    async def connect(self) -> None:
        """Connect to IMAP/SMTP servers. (Stub)"""
        # TODO: Implement IMAP/SMTP connection
        self._connected = True

    async def draft_monetization_email(
        self, partner: str, proposal: str
    ) -> str:
        """Draft a monetization/partnership outreach email. (Stub)"""
        return (
            f"Subject: Partnership Opportunity — Hive 999 × {partner}\n\n"
            f"Dear {partner} team,\n\n"
            f"{proposal}\n\n"
            "Looking forward to exploring synergies.\n\n"
            "Best regards,\nThe Hive 999 Collective"
        )

    async def github_summary(self, repo: str, days: int = 7) -> str:
        """Generate a GitHub activity summary. (Stub)"""
        return f"[Stub] GitHub summary for {repo} (last {days} days): No data yet."

    async def weekly_report(self) -> str:
        """Generate a weekly hive activity report. (Stub)"""
        return (
            "# Hive 999 — Weekly Report\n\n"
            "- Queries processed: [pending integration]\n"
            "- Active agents: Queen + 27 specialists\n"
            "- Matrix coverage: 729/729 nodes indexed\n"
        )

    async def run(self, query: str) -> str:
        """Process a Mantis Mail command. (Stub)"""
        if "draft" in query.lower():
            return await self.draft_monetization_email("Partner", query)
        if "github" in query.lower():
            return await self.github_summary("beeai-hive-999")
        if "report" in query.lower():
            return await self.weekly_report()
        return (
            "🦗 Mantis Mail is a stub. Available commands:\n"
            "  - draft <proposal>\n"
            "  - github <repo>\n"
            "  - report\n"
        )


def create_mantis_agent(config: MantisConfig | None = None) -> MantisMailAgent:
    """Factory function for the Mantis Mail agent."""
    return MantisMailAgent(config)
