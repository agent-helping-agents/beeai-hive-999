# AI Jobs Automation - Browser Automation Tests

import unittest
from unittest.mock import patch, MagicMock
from automation.browser import ScaleAIAutomation, DataAnnotationAutomation

class TestScaleAIAutomation(unittest.TestCase):
    """Test Scale AI automation functionality"""
    
    @patch('automation.browser.webdriver.Chrome')
    def test_initialization(self, mock_chrome):
        """Test initialization of ScaleAIAutomation"""
        # Setup mock
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        # Test initialization
        automation = ScaleAIAutomation(headless=True)
        
        # Verify driver was initialized
        self.assertIsNotNone(automation.driver)
        self.assertIsNotNone(automation.wait)
        
        # Verify headless option was set
        args, kwargs = mock_chrome.call_args
        self.assertTrue(any('--headless' in arg for arg in kwargs['options'].arguments))
        
        # Cleanup
        automation.close()
    
    @patch('automation.browser.webdriver.Chrome')
    def test_navigate_to_application(self, mock_chrome):
        """Test navigation to application page"""
        # Setup mock
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        # Test navigation
        automation = ScaleAIAutomation()
        
        with patch('builtins.input', return_value=''):
            automation.navigate_to_application("https://test.com")
        
        # Verify navigation
        mock_driver.get.assert_called_once_with("https://test.com")
        
        # Cleanup
        automation.close()
    
    @patch('automation.browser.webdriver.Chrome')
    def test_fill_basic_info(self, mock_chrome):
        """Test filling basic information"""
        # Setup mock
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        # Mock elements
        mock_email_field = MagicMock()
        mock_first_name_field = MagicMock()
        mock_last_name_field = MagicMock()
        
        mock_driver.find_element.side_effect = [
            mock_email_field,
            mock_first_name_field,
            mock_last_name_field
        ]
        
        # Test filling info
        automation = ScaleAIAutomation()
        
        with patch('builtins.input', return_value=''):
            result = automation.fill_basic_info(
                "test@example.com", 
                "Test", 
                "User"
            )
        
        # Verify fields were filled
        mock_email_field.send_keys.assert_called_once_with("test@example.com")
        mock_first_name_field.send_keys.assert_called_once_with("Test")
        mock_last_name_field.send_keys.assert_called_once_with("User")
        
        # Verify result
        self.assertTrue(result)
        
        # Cleanup
        automation.close()

class TestDataAnnotationAutomation(unittest.TestCase):
    """Test DataAnnotation automation functionality"""
    
    @patch('automation.browser.webdriver.Chrome')
    def test_initialization(self, mock_chrome):
        """Test initialization of DataAnnotationAutomation"""
        # Setup mock
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        # Test initialization
        automation = DataAnnotationAutomation()
        
        # Verify driver was initialized
        self.assertIsNotNone(automation.driver)
        self.assertIsNotNone(automation.wait)
        
        # Cleanup
        automation.close()
    
    @patch('automation.browser.webdriver.Chrome')
    def test_apply_to_position(self, mock_chrome):
        """Test applying to position"""
        # Setup mock
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        # Test application
        automation = DataAnnotationAutomation()
        
        with patch('builtins.input', return_value=''):
            result = automation.apply_to_position("https://test.com")
        
        # Verify navigation
        mock_driver.get.assert_called_once_with("https://test.com")
        
        # Verify result
        self.assertTrue(result)
        
        # Cleanup
        automation.close()

if __name__ == '__main__':
    unittest.main()

# WATERMARK: PRIMAX-AI-BSP-2025
© 2025 Bakery Street Project