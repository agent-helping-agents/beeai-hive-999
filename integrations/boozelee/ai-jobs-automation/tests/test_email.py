# AI Jobs Automation - Email Management Tests

import unittest
from unittest.mock import patch, MagicMock
from automation.email import EmailManager, ApplicationTracker
import os

class TestEmailManager(unittest.TestCase):
    """Test EmailManager functionality"""
    
    @patch('automation.email.imaplib.IMAP4_SSL')
    def test_initialization(self, mock_imap):
        """Test EmailManager initialization"""
        # Setup mock
        mock_mail = MagicMock()
        mock_imap.return_value = mock_mail
        
        # Set environment variables
        os.environ['EMAIL_SERVER'] = 'test.server.com'
        os.environ['EMAIL_USERNAME'] = 'test@example.com'
        os.environ['EMAIL_PASSWORD'] = 'test_password'
        
        # Test initialization
        email_manager = EmailManager()
        
        # Verify IMAP connection
        mock_imap.assert_called_once_with('test.server.com')
        mock_mail.login.assert_called_once_with('test@example.com', 'test_password')
        
        # Cleanup
        email_manager.close()
    
    @patch('automation.email.imaplib.IMAP4_SSL')
    def test_get_job_emails(self, mock_imap):
        """Test getting job-related emails"""
        # Setup mock
        mock_mail = MagicMock()
        mock_imap.return_value = mock_mail
        
        # Mock search results
        mock_mail.search.return_value = ('OK', [b'1 2 3'])
        
        # Mock email data
        mock_email_data = MagicMock()
        mock_email_data.get_payload.return_value = b'Test email content'
        
        # Mock message_from_bytes
        with patch('automation.email.email.message_from_bytes') as mock_message_from_bytes:
            mock_message_from_bytes.return_value = mock_email_data
            
            # Test getting emails
            email_manager = EmailManager()
            emails = email_manager.get_job_emails()
            
            # Verify search was called
            mock_mail.search.assert_called_once()
            
            # Verify emails were processed
            self.assertEqual(len(emails), 3)
            
            # Cleanup
            email_manager.close()

class TestApplicationTracker(unittest.TestCase):
    """Test ApplicationTracker functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a temporary tracker file
        self.test_file = 'test_tracker.md'
        with open(self.test_file, 'w') as f:
            f.write("# Test Tracker\n\n| Platform | Status | Date | Notes |\n|----------|--------|------|-------|\n")
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_initialization(self):
        """Test ApplicationTracker initialization"""
        # Test initialization with custom file
        tracker = ApplicationTracker(self.test_file)
        
        # Verify tracker file path
        self.assertEqual(tracker.tracker_file, self.test_file)
    
    def test_update_status_new_platform(self):
        """Test updating status for new platform"""
        tracker = ApplicationTracker(self.test_file)
        
        # Update status for new platform
        result = tracker.update_status("Test Platform", "Applied", "2026-01-17", "Test notes")
        
        # Verify result
        self.assertTrue(result)
        
        # Verify file was updated
        with open(self.test_file, 'r') as f:
            content = f.read()
            self.assertIn("Test Platform", content)
            self.assertIn("Applied", content)
    
    def test_update_status_existing_platform(self):
        """Test updating status for existing platform"""
        # Add initial content with existing platform
        with open(self.test_file, 'w') as f:
            f.write("# Test Tracker\n\n| Platform | Status | Date | Notes |\n|----------|--------|------|-------|\n| Existing Platform | Pending | 2026-01-16 | Initial |\n")
        
        tracker = ApplicationTracker(self.test_file)
        
        # Update status for existing platform
        result = tracker.update_status("Existing Platform", "Approved", "2026-01-17", "Updated")
        
        # Verify result
        self.assertTrue(result)
        
        # Verify file was updated
        with open(self.test_file, 'r') as f:
            content = f.read()
            self.assertIn("Approved", content)

if __name__ == '__main__':
    unittest.main()

# WATERMARK: PRIMAX-AI-BSP-2025
© 2025 Bakery Street Project