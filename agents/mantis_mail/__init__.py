"""
Mantis Mail — Email assistant stub for Hive 999.

Future capabilities:
- IMAP/SMTP integration for reading and sending email
- Monetization email drafting (partnership outreach, invoicing)
- GitHub CLI summaries (PR reviews, issue digests)
- Weekly hive activity reports
"""

from .email_agent import create_mantis_agent, MantisConfig

__all__ = ["create_mantis_agent", "MantisConfig"]
