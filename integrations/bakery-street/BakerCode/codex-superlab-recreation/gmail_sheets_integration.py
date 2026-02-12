#!/usr/bin/env python3
"""
Codex-SuperLab Gmail & Google Sheets Integration
Based on original 12.3K LOC implementation
Real-time task dashboard and automation
"""

import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials
import logging
from typing import Dict, List, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GmailAutomation:
    def __init__(self, email: str, app_password: str):
        self.email = email
        self.app_password = app_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_email(self, to_email: str, subject: str, body: str, html_body: str = None):
        """Send email via Gmail SMTP"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add plain text part
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.app_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def send_daily_digest(self, user_data: Dict[str, Any]):
        """Send daily progress digest"""
        subject = f"📊 Daily Progress Digest - {datetime.now().strftime('%Y-%m-%d')}"
        
        # Generate progress summary
        total_tasks = len(user_data.get('tasks', {}))
        completed_tasks = sum(1 for task in user_data.get('tasks', {}).values() if task.get('status') == 'completed')
        in_progress_tasks = sum(1 for task in user_data.get('tasks', {}).values() if task.get('status') == 'in_progress')
        
        # Plain text body
        body = f"""
Daily Progress Summary
======================

📈 Overall Progress:
• Total Tasks: {total_tasks}
• Completed: {completed_tasks}
• In Progress: {in_progress_tasks}
• Pending: {total_tasks - completed_tasks - in_progress_tasks}

🎯 Today's Highlights:
"""
        
        # Add recent task updates
        for task_name, task_data in user_data.get('tasks', {}).items():
            if task_data.get('checks'):
                latest_check = task_data['checks'][-1]
                if datetime.fromisoformat(latest_check['timestamp']).date() == datetime.now().date():
                    body += f"• {task_name}: {latest_check['progress']}% ({task_data['status']})\n"
        
        body += f"""
🚀 Keep up the great work!

---
Codex-SuperLab Automation System
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # HTML body
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2 style="color: #2c3e50;">📊 Daily Progress Digest</h2>
    <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
    
    <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
        <h3 style="color: #495057;">📈 Overall Progress</h3>
        <ul>
            <li><strong>Total Tasks:</strong> {total_tasks}</li>
            <li><strong>Completed:</strong> <span style="color: #28a745;">{completed_tasks}</span></li>
            <li><strong>In Progress:</strong> <span style="color: #ffc107;">{in_progress_tasks}</span></li>
            <li><strong>Pending:</strong> <span style="color: #6c757d;">{total_tasks - completed_tasks - in_progress_tasks}</span></li>
        </ul>
    </div>
    
    <h3 style="color: #495057;">🎯 Today's Highlights</h3>
    <ul>
"""
        
        # Add recent updates to HTML
        for task_name, task_data in user_data.get('tasks', {}).items():
            if task_data.get('checks'):
                latest_check = task_data['checks'][-1]
                if datetime.fromisoformat(latest_check['timestamp']).date() == datetime.now().date():
                    status_color = "#28a745" if task_data['status'] == 'completed' else "#ffc107" if task_data['status'] == 'in_progress' else "#6c757d"
                    html_body += f'<li><strong>{task_name}:</strong> {latest_check["progress"]}% <span style="color: {status_color};">({task_data["status"]})</span></li>'
        
        html_body += """
    </ul>
    
    <div style="margin-top: 30px; padding: 15px; background: #e3f2fd; border-radius: 5px;">
        <p style="margin: 0; color: #1976d2;"><strong>🚀 Keep up the great work!</strong></p>
    </div>
    
    <hr style="margin: 30px 0; border: none; border-top: 1px solid #dee2e6;">
    <p style="font-size: 12px; color: #6c757d;">
        Codex-SuperLab Automation System<br>
        Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """
    </p>
</body>
</html>
"""
        
        return self.send_email(user_data.get('email', ''), subject, body, html_body)

class GoogleSheetsIntegration:
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path
        self.client = None
        self.setup_client()
    
    def setup_client(self):
        """Setup Google Sheets client"""
        try:
            # Define the scope
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Load credentials
            creds = Credentials.from_service_account_file(self.credentials_path, scopes=scope)
            self.client = gspread.authorize(creds)
            logger.info("Google Sheets client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to setup Google Sheets client: {e}")
    
    def create_dashboard_sheet(self, sheet_name: str):
        """Create a new dashboard sheet"""
        try:
            sheet = self.client.create(sheet_name)
            worksheet = sheet.sheet1
            
            # Setup headers
            headers = [
                'Task Name', 'Status', 'Progress %', 'Created Date', 
                'Last Updated', 'Description', 'Total Checks', 'Latest Check'
            ]
            worksheet.append_row(headers)
            
            # Format headers
            worksheet.format('A1:H1', {
                'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 0.9},
                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
            })
            
            logger.info(f"Dashboard sheet '{sheet_name}' created successfully")
            return sheet.url
            
        except Exception as e:
            logger.error(f"Failed to create dashboard sheet: {e}")
            return None
    
    def update_dashboard(self, sheet_url: str, user_data: Dict[str, Any]):
        """Update dashboard with latest task data"""
        try:
            sheet = self.client.open_by_url(sheet_url)
            worksheet = sheet.sheet1
            
            # Clear existing data (except headers)
            worksheet.clear()
            
            # Re-add headers
            headers = [
                'Task Name', 'Status', 'Progress %', 'Created Date', 
                'Last Updated', 'Description', 'Total Checks', 'Latest Check'
            ]
            worksheet.append_row(headers)
            
            # Add task data
            for task_name, task_data in user_data.get('tasks', {}).items():
                latest_check = task_data.get('checks', [{}])[-1] if task_data.get('checks') else {}
                
                row = [
                    task_name,
                    task_data.get('status', 'pending').title(),
                    f"{task_data.get('progress', 0)}%",
                    task_data.get('created', '')[:10],  # Date only
                    latest_check.get('timestamp', '')[:19] if latest_check else '',  # DateTime
                    task_data.get('description', ''),
                    len(task_data.get('checks', [])),
                    f"{latest_check.get('progress', 0)}%" if latest_check else '0%'
                ]
                worksheet.append_row(row)
            
            # Format the sheet
            self.format_dashboard(worksheet, len(user_data.get('tasks', {})) + 1)
            
            logger.info(f"Dashboard updated successfully with {len(user_data.get('tasks', {}))} tasks")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update dashboard: {e}")
            return False
    
    def format_dashboard(self, worksheet, num_rows: int):
        """Apply formatting to dashboard"""
        try:
            # Format headers
            worksheet.format('A1:H1', {
                'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 0.9},
                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
            })
            
            # Format status column with conditional colors
            if num_rows > 1:
                # This would need more complex conditional formatting
                # For now, just apply basic formatting
                worksheet.format(f'A2:H{num_rows}', {
                    'borders': {
                        'top': {'style': 'SOLID', 'width': 1},
                        'bottom': {'style': 'SOLID', 'width': 1},
                        'left': {'style': 'SOLID', 'width': 1},
                        'right': {'style': 'SOLID', 'width': 1}
                    }
                })
            
        except Exception as e:
            logger.error(f"Failed to format dashboard: {e}")

class ProgressAutomation:
    def __init__(self, gmail_email: str, gmail_password: str, sheets_credentials: str):
        self.gmail = GmailAutomation(gmail_email, gmail_password)
        self.sheets = GoogleSheetsIntegration(sheets_credentials)
        self.user_data = {}
        self.load_user_data()
    
    def load_user_data(self):
        """Load user data from storage"""
        try:
            if os.path.exists('user_data.json'):
                with open('user_data.json', 'r') as f:
                    self.user_data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load user data: {e}")
    
    def save_user_data(self):
        """Save user data to storage"""
        try:
            with open('user_data.json', 'w') as f:
                json.dump(self.user_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save user data: {e}")
    
    def register_user(self, user_id: str, email: str, sheet_name: str = None):
        """Register a new user for automation"""
        if not sheet_name:
            sheet_name = f"Codex-Dashboard-{user_id}"
        
        # Create dashboard sheet
        sheet_url = self.sheets.create_dashboard_sheet(sheet_name)
        
        if sheet_url:
            self.user_data[user_id] = {
                'email': email,
                'sheet_url': sheet_url,
                'sheet_name': sheet_name,
                'tasks': {},
                'settings': {
                    'daily_digest': True,
                    'instant_updates': True,
                    'digest_time': '09:00'
                },
                'registered': datetime.now().isoformat()
            }
            self.save_user_data()
            logger.info(f"User {user_id} registered successfully")
            return sheet_url
        
        return None
    
    def sync_task_data(self, user_id: str, tasks_data: Dict[str, Any]):
        """Sync task data from Discord bot"""
        if user_id in self.user_data:
            self.user_data[user_id]['tasks'] = tasks_data
            self.save_user_data()
            
            # Update Google Sheets dashboard
            if self.user_data[user_id].get('sheet_url'):
                self.sheets.update_dashboard(
                    self.user_data[user_id]['sheet_url'],
                    self.user_data[user_id]
                )
            
            # Send instant update if enabled
            if self.user_data[user_id]['settings'].get('instant_updates'):
                self.send_progress_update(user_id)
    
    def send_progress_update(self, user_id: str):
        """Send progress update email"""
        if user_id not in self.user_data:
            return False
        
        user_info = self.user_data[user_id]
        subject = f"📈 Progress Update - {datetime.now().strftime('%H:%M')}"
        
        # Find recent updates (last hour)
        recent_updates = []
        cutoff_time = datetime.now() - timedelta(hours=1)
        
        for task_name, task_data in user_info.get('tasks', {}).items():
            if task_data.get('checks'):
                latest_check = task_data['checks'][-1]
                check_time = datetime.fromisoformat(latest_check['timestamp'])
                if check_time > cutoff_time:
                    recent_updates.append((task_name, task_data, latest_check))
        
        if recent_updates:
            body = "Recent Progress Updates:\n\n"
            for task_name, task_data, check in recent_updates:
                body += f"• {task_name}: {check['progress']}% ({task_data['status']})\n"
            
            body += f"\n📊 View full dashboard: {user_info.get('sheet_url', 'N/A')}"
            
            return self.gmail.send_email(user_info['email'], subject, body)
        
        return True
    
    def send_daily_digests(self):
        """Send daily digests to all users"""
        for user_id, user_info in self.user_data.items():
            if user_info['settings'].get('daily_digest', True):
                try:
                    self.gmail.send_daily_digest(user_info)
                    logger.info(f"Daily digest sent to user {user_id}")
                except Exception as e:
                    logger.error(f"Failed to send daily digest to user {user_id}: {e}")

# Example usage and testing
if __name__ == "__main__":
    # This would be configured with actual credentials
    print("Gmail & Sheets Integration Module")
    print("Configure with environment variables:")
    print("- GMAIL_EMAIL")
    print("- GMAIL_APP_PASSWORD") 
    print("- GOOGLE_SHEETS_CREDENTIALS_PATH")
    
    # Example initialization (commented out for security)
    # automation = ProgressAutomation(
    #     gmail_email=os.getenv('GMAIL_EMAIL'),
    #     gmail_password=os.getenv('GMAIL_APP_PASSWORD'),
    #     sheets_credentials=os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
    # )