# AI Jobs Automation - API Integration
# Legal and ethical API usage for job platforms

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import time

class ScaleAIAPI:
    """
    Scale AI API integration
    
    IMPORTANT: Only use official, documented APIs after manual account creation
    and explicit approval from the platform.
    """
    
    def __init__(self):
        """Initialize Scale AI API client"""
        load_dotenv()
        
        # API configuration
        self.api_key = os.getenv('SCALE_AI_API_KEY')
        self.base_url = "https://api.scale.com/v1"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Rate limiting
        self.rate_limit = 10  # requests per minute
        self.last_request_time = 0
    
    def _check_rate_limit(self):
        """Check and enforce rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < 6:  # 6 seconds between requests
            time.sleep(6 - time_since_last)
        
        self.last_request_time = time.time()
    
    def get_available_tasks(self):
        """
        Get available tasks from Scale AI
        
        Returns:
            List of available tasks or None if error
        """
        if not self.api_key:
            print("❌ Scale AI API key not configured")
            print("📝 Please add SCALE_AI_API_KEY to your .env file")
            print("📝 Obtain API key from Scale AI dashboard after manual signup")
            return None
        
        self._check_rate_limit()
        
        try:
            url = f"{self.base_url}/tasks"
            auth = HTTPBasicAuth(self.api_key, '')
            
            response = requests.get(url, headers=self.headers, auth=auth)
            
            if response.status_code == 200:
                tasks = response.json()
                print(f"✅ Found {len(tasks)} available tasks")
                return tasks
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ API Request Error: {e}")
            return None
    
    def get_task_details(self, task_id):
        """
        Get details for a specific task
        
        Args:
            task_id: Task ID to get details for
        
        Returns:
            Task details or None if error
        """
        if not self.api_key:
            return None
            
        self._check_rate_limit()
        
        try:
            url = f"{self.base_url}/tasks/{task_id}"
            auth = HTTPBasicAuth(self.api_key, '')
            
            response = requests.get(url, headers=self.headers, auth=auth)
            
            if response.status_code == 200:
                task_details = response.json()
                print(f"✅ Retrieved task details for {task_id}")
                return task_details
            else:
                print(f"❌ API Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ API Request Error: {e}")
            return None

class DataAnnotationAPI:
    """
    DataAnnotation.tech API integration
    """
    
    def __init__(self):
        """Initialize DataAnnotation API client"""
        load_dotenv()
        
        self.api_key = os.getenv('DATAANNOTATION_API_KEY')
        self.base_url = "https://api.dataannotation.tech/v1"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def get_projects(self):
        """
        Get available projects
        
        Returns:
            List of projects or None if error
        """
        if not self.api_key:
            print("❌ DataAnnotation API key not configured")
            return None
            
        try:
            url = f"{self.base_url}/projects"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                projects = response.json()
                print(f"✅ Found {len(projects)} projects")
                return projects
            else:
                print(f"❌ API Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ API Request Error: {e}")
            return None

class APIManager:
    """
    Unified API manager for all platforms
    """
    
    def __init__(self):
        """Initialize API manager"""
        self.scale_ai = ScaleAIAPI()
        self.dataannotation = DataAnnotationAPI()
    
    def check_api_availability(self):
        """
        Check which APIs are available based on configuration
        
        Returns:
            Dictionary of available APIs
        """
        available = {
            'scale_ai': bool(os.getenv('SCALE_AI_API_KEY')),
            'dataannotation': bool(os.getenv('DATAANNOTATION_API_KEY')),
            'appen': bool(os.getenv('APPEN_API_KEY'))
        }
        
        print("🔑 API Availability:")
        for platform, available_status in available.items():
            status = "✅ Available" if available_status else "❌ Not configured"
            print(f"   {platform}: {status}")
        
        return available

# Legal compliance reminder
print("🔑 API COMPLIANCE REMINDER:")
print("✅ Only use official, documented APIs")
print("✅ Obtain API keys through manual account creation")
print("✅ Respect platform rate limits")
print("✅ Follow platform API Terms of Service")
print("✅ Use only for approved purposes")
print()

# WATERMARK: PRIMAX-AI-BSP-2025
© 2025 Bakery Street Project