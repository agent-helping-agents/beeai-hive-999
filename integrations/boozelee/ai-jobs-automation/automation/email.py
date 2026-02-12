# AI Jobs Automation - Email Management
# Legal and ethical email organization for job applications

import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os

class EmailManager:
    """
    Email management for job application tracking
    
    This class helps organize and track job application emails
    while maintaining compliance with email service Terms of Service.
    """
    
    def __init__(self):
        """Initialize email manager"""
        load_dotenv()
        
        # Load credentials from environment
        self.email_server = os.getenv('EMAIL_SERVER', 'imap.your-email.com')
        self.email_username = os.getenv('EMAIL_USERNAME', 'your_email@example.com')
        self.email_password = os.getenv('EMAIL_PASSWORD', 'your_password')
        
        # Connect to email server
        self.mail = imaplib.IMAP4_SSL(self.email_server)
        self.mail.login(self.email_username, self.email_password)
        print(f"✅ Connected to email: {self.email_username}")
    
    def get_job_emails(self, platforms=None):
        """
        Get job-related emails from specified platforms
        
        Args:
            platforms: List of platforms to search for (e.g., ['scale.com', 'dataannotation.tech'])
        
        Returns:
            List of email dictionaries with subject, from, date, and body
        """
        if platforms is None:
            platforms = ['scale.com', 'dataannotation.tech', 'appen.com', 'lionbridge.com']
        
        # Create search query
        search_query = ' OR '.join([f'FROM "@{platform}"' for platform in platforms])
        
        # Select inbox
        self.mail.select('inbox')
        
        # Search for emails
        status, messages = self.mail.search(None, f'({search_query})')
        
        if status != 'OK':
            print(f"❌ Error searching emails: {status}")
            return []
        
        emails = []
        
        for num in messages[0].split():
            # Fetch email
            status, data = self.mail.fetch(num, '(RFC822)')
            
            if status != 'OK':
                continue
            
            # Parse email
            msg = email.message_from_bytes(data[0][1])
            
            # Decode subject
            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')
            
            # Decode from
            from_email, encoding = decode_header(msg.get('From', ''))[0]
            if isinstance(from_email, bytes):
                from_email = from_email.decode(encoding if encoding else 'utf-8')
            
            # Get date
            date = msg.get('Date', 'Unknown')
            
            # Get body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == 'text/plain':
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            body = str(part.get_payload())
            else:
                try:
                    body = msg.get_payload(decode=True).decode()
                except:
                    body = str(msg.get_payload())
            
            emails.append({
                'subject': subject,
                'from': from_email,
                'date': date,
                'body': body[:200] + '...' if len(body) > 200 else body
            })
        
        print(f"✅ Found {len(emails)} job-related emails")
        return emails
    
    def close(self):
        """Close email connection"""
        self.mail.close()
        self.mail.logout()
        print("🔄 Email connection closed")

class ApplicationTracker:
    """
    Track application status and updates
    """
    
    def __init__(self, tracker_file="~/AI_JOBS_TRACKER.md"):
        """Initialize application tracker"""
        self.tracker_file = os.path.expanduser(tracker_file)
        
        # Create tracker file if it doesn't exist
        if not os.path.exists(self.tracker_file):
            with open(self.tracker_file, 'w') as f:
                f.write("# AI Jobs Application Tracker\n\n## Applications\n\n| Platform | Status | Date | Notes |\n|----------|--------|------|-------|\n")
            print(f"✅ Created new tracker file: {self.tracker_file}")
    
    def update_status(self, platform, status, date=None, notes=""):
        """
        Update application status in tracker
        
        Args:
            platform: Platform name
            status: Application status
            date: Date of update
            notes: Additional notes
        """
        # Read current tracker
        with open(self.tracker_file, 'r') as f:
            lines = f.readlines()
        
        # Find and update platform line
        updated = False
        for i, line in enumerate(lines):
            if platform.lower() in line.lower() and '|' in line:
                # Update the status column (assuming it's the 3rd column)
                parts = line.split('|')
                if len(parts) >= 3:
                    parts[2] = f' {status} '
                    lines[i] = '|'.join(parts)
                    updated = True
                    break
        
        # If platform not found, add new entry
        if not updated:
            date_str = date if date else "Today"
            new_line = f"| {platform} | Pending | {date_str} | {notes} |\n"
            lines.insert(-1, new_line)
        
        # Write updated tracker
        with open(self.tracker_file, 'w') as f:
            f.writelines(lines)
        
        print(f"✅ Updated {platform} status to: {status}")
        return True

# Legal compliance reminder
print("📧 EMAIL MANAGEMENT COMPLIANCE:")
print("✅ Only access your own email accounts")
print("✅ Respect email service Terms of Service")
print("✅ Use only for personal organization")
print("✅ Do not automate email sending without permission")
print()

# WATERMARK: PRIMAX-AI-BSP-2025
© 2025 Bakery Street Project