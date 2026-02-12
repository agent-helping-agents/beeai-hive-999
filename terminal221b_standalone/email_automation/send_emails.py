#!/usr/bin/env python3
"""
Email Automation Script - Send bounty partnership emails
Usage: python3 send_emails.py --config email_config.yaml
"""

import smtplib
import yaml
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
import os
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.expanduser('~/terminal221b/logs/email_sender.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self, config_file):
        """Initialize email sender with config"""
        with open(os.path.expanduser(config_file), 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.provider = self.config['email']['provider']
        self.sent_emails = []
        
    def send_gmail(self, to_email, subject, body, attachments=None):
        """Send email via Gmail SMTP"""
        try:
            gmail_config = self.config['email']['gmail']
            
            # Gmail SMTP settings
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = gmail_config['email_address']
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Send
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(gmail_config['email_address'], gmail_config['app_password'])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"✅ Email sent to {to_email}")
            self.sent_emails.append({
                'to': to_email,
                'subject': subject,
                'timestamp': datetime.now().isoformat()
            })
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send to {to_email}: {str(e)}")
            return False
    
    def send_augment_email(self):
        """Send Augment collaboration email"""
        subject = "Terminal 221B x Context Engine MCP - Production Integration"
        
        with open(os.path.expanduser('~/emails_ready_to_send/01_AUGMENT_EMAIL.txt'), 'r') as f:
            body = f.read()
        
        return self.send_gmail(
            self.config['recipients']['augment'],
            subject,
            body
        )
    
    def send_gemini_email(self):
        """Send Gemini collaboration email"""
        subject = "Deep Research Integration for Autonomous AI Multi-Agent Crypto System"
        
        with open(os.path.expanduser('~/emails_ready_to_send/02_GEMINI_EMAIL.txt'), 'r') as f:
            body = f.read()
        
        return self.send_gmail(
            self.config['recipients']['gemini'],
            subject,
            body
        )
    
    def send_openai_email(self):
        """Send OpenAI collaboration email"""
        subject = "GPT-4 Integration for Multi-Agent Autonomous AI System"
        
        with open(os.path.expanduser('~/emails_ready_to_send/03_OPENAI_EMAIL.txt'), 'r') as f:
            body = f.read()
        
        return self.send_gmail(
            self.config['recipients']['openai'],
            subject,
            body
        )
    
    def send_all(self):
        """Send all partnership emails"""
        logger.info("Starting email campaign...")
        
        results = {
            'augment': self.send_augment_email(),
            'gemini': self.send_gemini_email(),
            'openai': self.send_openai_email()
        }
        
        logger.info(f"Email campaign complete: {sum(results.values())}/3 sent")
        return results

if __name__ == '__main__':
    config_file = '~/terminal221b/email_automation/email_config.yaml'
    
    if len(sys.argv) > 1 and sys.argv[1] == '--config':
        config_file = sys.argv[2]
    
    sender = EmailSender(config_file)
    results = sender.send_all()
    
    # Print results
    print("\n" + "="*60)
    print("EMAIL SENDING RESULTS")
    print("="*60)
    for recipient, success in results.items():
        status = "✅ Sent" if success else "❌ Failed"
        print(f"{recipient.upper()}: {status}")
    print("="*60)
