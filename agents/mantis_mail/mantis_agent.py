"""
Mantis Mail Agent — The Hive's Email Communication Specialist

The Mantis is not a bee—it's a solitary predator that waits patiently
for the right moment to strike. In the Hive 999 ecosystem, the Mantis
manages external communications via Zoho Mail.

Zoho Mail Configuration:
- Domain: bakerstreetbandits.work.gd
- IMAP: imappro.zoho.com:993
- SMTP: smtp.zoho.com:587 (TLS)
"""

import asyncio
import os
import sys
import smtplib
import imaplib
import email
from datetime import datetime
from typing import Optional, List, Dict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.backend import ChatModel
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.tools import StringToolOutput, tool

# Zoho Configuration
from agents.mantis_mail.zoho_config import ZOHO_CONFIG, get_zoho_credentials


# ============================================================================
# ZOHO MAIL TOOLS
# ============================================================================

@tool
def send_email_zoho(to: str, subject: str, body: str, html: bool = False) -> StringToolOutput:
    """
    Send an email via Zoho Mail SMTP.
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body content
        html: Whether body is HTML (default: plain text)
    
    Returns:
        Send status report
    """
    email_addr, password = get_zoho_credentials()
    
    if not email_addr or not password:
        return StringToolOutput(
            result="❌ Zoho Mail not configured. Set MANTIS_EMAIL_ADDRESS and MANTIS_EMAIL_PASSWORD"
        )
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = email_addr
        msg['To'] = to
        msg['Subject'] = subject
        msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
        
        # Add signature
        body_with_sig = body + f"""

---
🐝 BeeAI Hive 999 | Automated Communication
Domain: {ZOHO_CONFIG['domain']}
Matrix: 9×9×9 | 729 Nodes | Digital Root 9
"""
        
        # Attach body
        content_type = 'html' if html else 'plain'
        msg.attach(MIMEText(body_with_sig, content_type))
        
        # Connect to Zoho SMTP
        server = smtplib.SMTP(ZOHO_CONFIG['smtp_server'], ZOHO_CONFIG['smtp_port'])
        server.starttls()
        server.login(email_addr, password)
        
        # Send email
        server.sendmail(email_addr, to, msg.as_string())
        server.quit()
        
        return StringToolOutput(
            result=f"✅ Email sent successfully via Zoho Mail\nFrom: {email_addr}\nTo: {to}\nSubject: {subject}"
        )
        
    except Exception as e:
        return StringToolOutput(result=f"❌ Failed to send email: {str(e)}")


@tool
def check_inbox_zoho(folder: str = "INBOX", limit: int = 5) -> StringToolOutput:
    """
    Check Zoho Mail inbox via IMAP.
    
    Args:
        folder: IMAP folder to check (default: INBOX)
        limit: Maximum number of emails to fetch
    
    Returns:
        List of recent emails
    """
    email_addr, password = get_zoho_credentials()
    
    if not email_addr or not password:
        return StringToolOutput(
            result="❌ Zoho Mail not configured. Set MANTIS_EMAIL_ADDRESS and MANTIS_EMAIL_PASSWORD"
        )
    
    try:
        # Connect to Zoho IMAP
        mail = imaplib.IMAP4_SSL(ZOHO_CONFIG['imap_server'])
        mail.login(email_addr, password)
        mail.select(folder)
        
        # Search for all emails
        _, data = mail.search(None, 'ALL')
        email_ids = data[0].split()
        
        # Get recent emails
        recent_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
        
        results = []
        for e_id in reversed(recent_ids):
            _, msg_data = mail.fetch(e_id, '(RFC822)')
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            subject = msg['subject'] or '(No Subject)'
            sender = msg['from'] or 'Unknown'
            date = msg['date'] or 'Unknown'
            
            results.append(f"[{date}] From: {sender}\nSubject: {subject}\n")
        
        mail.close()
        mail.logout()
        
        return StringToolOutput(
            result=f"📬 Zoho Mail Inbox ({len(recent_ids)} messages):\n\n" + "\n".join(results)
        )
        
    except Exception as e:
        return StringToolOutput(result=f"❌ Failed to check inbox: {str(e)}")


@tool
def draft_email(recipient: str, subject: str, purpose: str, tone: str = "professional") -> StringToolOutput:
    """
    Draft an email for review before sending.
    
    Args:
        recipient: Who the email is for (e.g., "investors", "team", "stakeholders")
        subject: Email subject line
        purpose: What the email should accomplish
        tone: Tone of voice (professional, casual, formal, urgent)
    
    Returns:
        Drafted email content
    """
    template = f"""=== EMAIL DRAFT ===

To: {recipient}
Subject: {subject}
Tone: {tone}
Purpose: {purpose}

---

Dear {recipient.title()},

[I will draft content based on the purpose once you confirm the approach]

This email will:
- Address: {purpose}
- Use tone: {tone}
- Include Hive 999 signature block

Would you like me to:
1. Generate the full draft now
2. Adjust the tone/topic first

---

🐝 BeeAI Hive 999
Domain: {ZOHO_CONFIG['domain']}
"""
    
    return StringToolOutput(result=template)


@tool
def get_email_config() -> StringToolOutput:
    """Get current Zoho Mail configuration status."""
    from agents.mantis_mail.zoho_config import verify_setup
    
    config = verify_setup()
    lines = ["📧 Zoho Mail Configuration", "=" * 40]
    
    for key, value in config.items():
        lines.append(f"{key:20s}: {value}")
    
    lines.extend([
        "=" * 40,
        "",
        "To use Zoho Mail:",
        "1. Complete domain verification at Zoho",
        "2. Set MANTIS_EMAIL_ADDRESS=hive@bakerstreetbandits.work.gd",
        "3. Set MANTIS_EMAIL_PASSWORD=your_app_password",
        "4. Test with :mantis agent in TUI",
    ])
    
    return StringToolOutput(result="\n".join(lines))


# ============================================================================
# MANTIS AGENT FACTORY
# ============================================================================

async def create_mantis_agent() -> RequirementAgent:
    """
    Create the Mantis Mail Agent with Zoho Mail integration.
    """
    llm = ChatModel.from_name("ollama:llama3.1:8b")
    
    email_addr, _ = get_zoho_credentials()
    
    instructions = f"""You are the Mantis, the Hive 999's email communication specialist.

=== YOUR DOMAIN ===
Zoho Mail Domain: {ZOHO_CONFIG['domain']}
Email Address: {email_addr or "(Not configured - set MANTIS_EMAIL_ADDRESS)"}
IMAP: {ZOHO_CONFIG['imap_server']}:{ZOHO_CONFIG['imap_port']}
SMTP: {ZOHO_CONFIG['smtp_server']}:{ZOHO_CONFIG['smtp_port']}

=== YOUR CAPABILITIES ===
1. send_email_zoho - Send emails via Zoho SMTP
2. check_inbox_zoho - Check incoming mail via IMAP
3. draft_email - Create drafts for review
4. get_email_config - Show current configuration

=== YOUR PERSONALITY ===
The Mantis is:
- Patient and precise - waits for the right moment
- Formal in communication
- Protective of hive security
- Never sends without explicit confirmation

=== WORKFLOW ===
1. When asked to send email, first draft it for review
2. Get explicit confirmation before sending
3. Always include Hive 999 signature block
4. Log all communications

=== SECURITY ===
- Never expose passwords or API keys
- Confirm recipient addresses
- Use professional tone for external communications
"""
    
    mantis = RequirementAgent(
        llm=llm,
        tools=[
            send_email_zoho,
            check_inbox_zoho,
            draft_email,
            get_email_config,
        ],
        memory=UnconstrainedMemory(),
        instructions=instructions,
    )
    
    return mantis


# ============================================================================
# TEST FUNCTIONS
# ============================================================================

async def test_zoho_connection():
    """Test Zoho Mail connection."""
    print("Testing Zoho Mail configuration...")
    print()
    
    # Show config
    config_result = get_email_config()
    print(config_result.result)
    print()
    
    email_addr, password = get_zoho_credentials()
    
    if not email_addr or not password:
        print("❌ Credentials not set. Cannot test connection.")
        return
    
    # Test SMTP
    print("Testing SMTP connection...")
    try:
        server = smtplib.SMTP(ZOHO_CONFIG['smtp_server'], ZOHO_CONFIG['smtp_port'])
        server.starttls()
        server.login(email_addr, password)
        server.quit()
        print("✅ SMTP connection successful")
    except Exception as e:
        print(f"❌ SMTP failed: {e}")
    
    # Test IMAP
    print("\nTesting IMAP connection...")
    try:
        mail = imaplib.IMAP4_SSL(ZOHO_CONFIG['imap_server'])
        mail.login(email_addr, password)
        mail.select('INBOX')
        mail.close()
        mail.logout()
        print("✅ IMAP connection successful")
    except Exception as e:
        print(f"❌ IMAP failed: {e}")


# ============================================================================
# STANDALONE TEST
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Test configuration
        asyncio.run(test_zoho_connection())
    else:
        # Interactive test
        async def interactive_test():
            print("Testing Mantis Agent with Zoho Mail...")
            mantis = await create_mantis_agent()
            
            result = await mantis.run("Show me the email configuration")
            print(result.last_message.text)
        
        asyncio.run(interactive_test())
