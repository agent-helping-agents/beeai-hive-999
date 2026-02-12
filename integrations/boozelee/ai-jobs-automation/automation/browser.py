# AI Jobs Automation - Browser Automation
# Legal and ethical browser automation for job applications

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

class ScaleAIAutomation:
    """
    Browser automation for Scale AI job applications
    
    IMPORTANT: This class provides automation assistance but requires
    manual review and submission to comply with platform Terms of Service.
    """
    
    def __init__(self, headless=False):
        """Initialize browser automation"""
        load_dotenv()
        
        # Browser options
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Initialize driver
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 30)
    
    def navigate_to_application(self, url="https://scale.com/careers"):
        """Navigate to Scale AI careers page"""
        self.driver.get(url)
        print(f"✅ Navigated to: {url}")
        
        # Wait for page to load
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        
        # Manual review point
        print("📝 Please review the page and confirm you want to proceed")
        input("Press Enter to continue with form filling...")
    
    def fill_basic_info(self, email, first_name, last_name):
        """Fill basic application information"""
        try:
            # Find and fill email field
            email_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, 'email'))
            )
            email_field.send_keys(email)
            print(f"✅ Filled email: {email}")
            
            # Find and fill first name
            first_name_field = self.driver.find_element(By.NAME, 'first_name')
            first_name_field.send_keys(first_name)
            print(f"✅ Filled first name: {first_name}")
            
            # Find and fill last name
            last_name_field = self.driver.find_element(By.NAME, 'last_name')
            last_name_field.send_keys(last_name)
            print(f"✅ Filled last name: {last_name}")
            
            # Manual review before submission
            print("📝 Basic information filled")
            print("🔍 Please review all fields carefully")
            input("Press Enter after you've reviewed and are ready to submit...")
            
            return True
            
        except Exception as e:
            print(f"❌ Error filling form: {e}")
            return False
    
    def manual_submission_required(self):
        """Require manual submission to comply with Terms of Service"""
        print("🚨 MANUAL SUBMISSION REQUIRED")
        print("📋 Please complete the following steps:")
        print("1. Review all form fields for accuracy")
        print("2. Complete any platform-specific questions")
        print("3. Verify all information is correct")
        print("4. Click the submit button manually")
        print("5. Wait for confirmation from the platform")
        
        input("Press Enter after you've completed manual submission...")
        
        return True
    
    def close(self):
        """Close browser and cleanup"""
        self.driver.quit()
        print("🔄 Browser closed")

class DataAnnotationAutomation:
    """
    Browser automation for DataAnnotation.tech applications
    """
    
    def __init__(self, headless=False):
        """Initialize browser automation"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 30)
    
    def apply_to_position(self, url="https://weworkremotely.com/remote-jobs/dataannotation-tech-ft-pt-remote-ai-prompt-engineering-evaluation-will-train"):
        """Apply to DataAnnotation.tech position"""
        self.driver.get(url)
        print(f"✅ Navigated to DataAnnotation application")
        
        # Manual review required
        print("📝 Please review the job posting")
        input("Press Enter to continue...")
        
        return True
    
    def close(self):
        """Close browser"""
        self.driver.quit()

# Legal compliance reminder
print("🚨 LEGAL COMPLIANCE REMINDER:")
print("✅ Manual account creation required")
print("✅ Manual review before submission")
print("✅ Follow platform Terms of Service")
print("✅ Use only for personal productivity")
print()

# WATERMARK: PRIMAX-AI-BSP-2025
© 2025 Bakery Street Project