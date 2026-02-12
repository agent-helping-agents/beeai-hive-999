#!/usr/bin/env python3
"""
Zoho Mail CLI - Unofficial command-line interface for Zoho Mail
Uses Zoho Mail Admin API and IMAP/SMTP for management
"""

import os
import sys
import argparse
import imaplib
import smtplib
import getpass
from email.mime.text import MIMEText
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.mantis_mail.zoho_config import ZOHO_CONFIG


class ZohoMailCLI:
    """CLI for Zoho Mail operations."""
    
    def __init__(self):
        self.email = os.getenv("MANTIS_EMAIL_ADDRESS")
        self.password = os.getenv("MANTIS_EMAIL_PASSWORD")
        
    def check_config(self):
        """Check if credentials are configured."""
        if not self.email or not self.password:
            print("❌ Zoho Mail not configured")
            print("Set environment variables:")
            print("  export MANTIS_EMAIL_ADDRESS=hive@bakerstreetbandits.work.gd")
            print("  export MANTIS_EMAIL_PASSWORD=your_app_password")
            return False
        return True
    
    def verify_setup(self):
        """Verify Zoho Mail configuration."""
        print("🔍 Zoho Mail Configuration")
        print("=" * 50)
        print(f"Domain: {ZOHO_CONFIG['domain']}")
        print(f"Verification Code: {ZOHO_CONFIG['verification_code']}")
        print(f"IMAP: {ZOHO_CONFIG['imap_server']}:{ZOHO_CONFIG['imap_port']}")
        print(f"SMTP: {ZOHO_CONFIG['smtp_server']}:{ZOHO_CONFIG['smtp_port']}")
        print()
        print(f"Email: {self.email or 'NOT SET'}")
        print(f"Password: {'SET' if self.password else 'NOT SET'}")
        
        if self.email and self.password:
            print()
            print("Testing connections...")
            self.test_imap()
            self.test_smtp()
    
    def test_imap(self):
        """Test IMAP connection."""
        try:
            mail = imaplib.IMAP4_SSL(ZOHO_CONFIG['imap_server'])
            mail.login(self.email, self.password)
            mail.select('INBOX')
            mail.close()
            mail.logout()
            print("✅ IMAP connection successful")
            return True
        except Exception as e:
            print(f"❌ IMAP failed: {e}")
            return False
    
    def test_smtp(self):
        """Test SMTP connection."""
        try:
            server = smtplib.SMTP(ZOHO_CONFIG['smtp_server'], ZOHO_CONFIG['smtp_port'])
            server.starttls()
            server.login(self.email, self.password)
            server.quit()
            print("✅ SMTP connection successful")
            return True
        except Exception as e:
            print(f"❌ SMTP failed: {e}")
            return False
    
    def list_inbox(self, limit=10):
        """List recent emails from inbox."""
        if not self.check_config():
            return
        
        try:
            mail = imaplib.IMAP4_SSL(ZOHO_CONFIG['imap_server'])
            mail.login(self.email, self.password)
            mail.select('INBOX')
            
            _, data = mail.search(None, 'ALL')
            email_ids = data[0].split()
            
            # Get recent emails
            recent_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
            
            print(f"📬 Recent {len(recent_ids)} emails:")
            print("=" * 60)
            
            for e_id in reversed(recent_ids):
                _, msg_data = mail.fetch(e_id, '(RFC822)')
                raw_email = msg_data[0][1]
                import email
                msg = email.message_from_bytes(raw_email)
                
                subject = msg['subject'] or '(No Subject)'
                sender = msg['from'] or 'Unknown'
                date = msg['date'] or 'Unknown'
                
                print(f"\nFrom: {sender}")
                print(f"Subject: {subject}")
                print(f"Date: {date}")
                print("-" * 60)
            
            mail.close()
            mail.logout()
            
        except Exception as e:
            print(f"❌ Failed to list emails: {e}")
    
    def send_email(self, to, subject, body):
        """Send an email."""
        if not self.check_config():
            return
        
        try:
            msg = MIMEText(body)
            msg['From'] = self.email
            msg['To'] = to
            msg['Subject'] = subject
            
            server = smtplib.SMTP(ZOHO_CONFIG['smtp_server'], ZOHO_CONFIG['smtp_port'])
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, to, msg.as_string())
            server.quit()
            
            print(f"✅ Email sent to {to}")
            
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
    
    def setup_credentials(self):
        """Interactive setup for Zoho credentials."""
        print("🔧 Zoho Mail Credentials Setup")
        print("=" * 50)
        print(f"Domain: {ZOHO_CONFIG['domain']}")
        print(f"Verification Code: {ZOHO_CONFIG['verification_code']}")
        print()
        
        email = input(f"Enter email [hive@{ZOHO_CONFIG['domain']}]: ").strip()
        if not email:
            email = f"hive@{ZOHO_CONFIG['domain']}"
        
        password = getpass.getpass("Enter app password: ").strip()
        
        if email and password:
            # Test connection
            self.email = email
            self.password = password
            
            print()
            print("Testing connection...")
            if self.test_imap() and self.test_smtp():
                # Save to .env
                env_file = Path.home() / ".env"
                with open(env_file, "a") as f:
                    f.write(f"\n# Zoho Mail Configuration\n")
                    f.write(f"export MANTIS_EMAIL_ADDRESS={email}\n")
                    f.write(f"export MANTIS_EMAIL_PASSWORD={password}\n")
                    f.write(f"export MANTIS_EMAIL_PROVIDER=zoho\n")
                
                print()
                print(f"✅ Credentials saved to {env_file}")
                print("Load with: source ~/.env")
            else:
                print()
                print("❌ Connection test failed. Credentials not saved.")
        else:
            print("❌ Email and password are required")
    
    def domain_status(self):
        """Show domain verification status."""
        print("🌐 Domain Verification Status")
        print("=" * 50)
        print(f"Domain: {ZOHO_CONFIG['domain']}")
        print(f"Verification Code: {ZOHO_CONFIG['verification_code']}")
        print()
        print("Verification File:")
        verify_file = Path.home() / "zohoverify" / "verifyforzoho.html"
        if verify_file.exists():
            print(f"  ✓ Found: {verify_file}")
            print(f"  Content: {verify_file.read_text().strip()}")
        else:
            print(f"  ✗ Not found: {verify_file}")
        print()
        print("Next steps:")
        print("  1. Host verification file publicly")
        print("  2. Access: http://YOUR_DOMAIN/zohoverify/verifyforzoho.html")
        print("  3. Verify in Zoho Mail Admin")


def main():
    parser = argparse.ArgumentParser(
        description="Zoho Mail CLI for Hive 999",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s verify           # Check configuration
  %(prog)s setup            # Interactive credential setup
  %(prog)s inbox            # List inbox emails
  %(prog)s send -t to@email.com -s "Subject" -b "Body"
        """
    )
    
    parser.add_argument(
        "command",
        choices=["verify", "setup", "inbox", "send", "domain", "test"],
        help="Command to execute"
    )
    
    # Send email options
    parser.add_argument("-t", "--to", help="Recipient email")
    parser.add_argument("-s", "--subject", help="Email subject")
    parser.add_argument("-b", "--body", help="Email body")
    
    args = parser.parse_args()
    
    cli = ZohoMailCLI()
    
    if args.command == "verify":
        cli.verify_setup()
    
    elif args.command == "setup":
        cli.setup_credentials()
    
    elif args.command == "inbox":
        cli.list_inbox()
    
    elif args.command == "send":
        if not args.to or not args.subject:
            print("❌ Usage: zoho_cli.py send -t to@email.com -s 'Subject' -b 'Body'")
            sys.exit(1)
        cli.send_email(args.to, args.subject, args.body or "")
    
    elif args.command == "domain":
        cli.domain_status()
    
    elif args.command == "test":
        if cli.check_config():
            cli.test_imap()
            cli.test_smtp()


if __name__ == "__main__":
    main()
