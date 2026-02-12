#!/usr/bin/env python3
"""
Baker Street Laboratory - API Client Example
Demonstrates how to interact with the Baker Street Laboratory API.
"""

import requests
import json
import time
from typing import Dict, Any, Optional

class BakerStreetClient:
    """Client for interacting with Baker Street Laboratory API."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'BakerStreetClient/1.0'
        })
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information."""
        response = self.session.get(f"{self.api_url}/system/info")
        response.raise_for_status()
        return response.json()
    
    def check_health(self) -> Dict[str, Any]:
        """Check system health."""
        response = self.session.get(f"{self.api_url}/system/health")
        response.raise_for_status()
        return response.json()
    
    def conduct_research(self, query: str, output_dir: str = "research/api_output") -> Dict[str, Any]:
        """
        Conduct a research session.
        
        Args:
            query: Research question or topic
            output_dir: Directory to store results
            
        Returns:
            Research results dictionary
        """
        data = {
            "query": query,
            "output_dir": output_dir
        }
        
        response = self.session.post(f"{self.api_url}/research/conduct", json=data)
        response.raise_for_status()
        return response.json()
    
    def get_research_status(self, session_id: str) -> Dict[str, Any]:
        """
        Get research session status.
        
        Args:
            session_id: Research session ID
            
        Returns:
            Status information
        """
        response = self.session.get(f"{self.api_url}/research/status/{session_id}")
        response.raise_for_status()
        return response.json()
    
    def list_reports(self) -> Dict[str, Any]:
        """List all available research reports."""
        response = self.session.get(f"{self.api_url}/reports/list")
        response.raise_for_status()
        return response.json()
    
    def get_report(self, report_id: str) -> Dict[str, Any]:
        """
        Get a specific research report.
        
        Args:
            report_id: Report ID
            
        Returns:
            Report content and metadata
        """
        response = self.session.get(f"{self.api_url}/reports/{report_id}")
        response.raise_for_status()
        return response.json()

def main():
    """Demonstrate API client usage."""
    print("🔬 Baker Street Laboratory - API Client Demo")
    print("=" * 50)
    
    # Initialize client
    client = BakerStreetClient()
    
    try:
        # 1. Check system health
        print("\n1. Checking system health...")
        health = client.check_health()
        print(f"   Status: {health['status']}")
        print(f"   Timestamp: {health['timestamp']}")
        
        # 2. Get system info
        print("\n2. Getting system information...")
        info = client.get_system_info()
        print(f"   Name: {info['name']}")
        print(f"   Version: {info['version']}")
        
        # 3. Conduct research
        print("\n3. Conducting research...")
        query = "What are the key principles of detective work?"
        print(f"   Query: {query}")
        
        research_result = client.conduct_research(query)
        session_id = research_result['session_id']
        
        print(f"   Session ID: {session_id}")
        print(f"   Status: {research_result['status']}")
        print(f"   Summary: {research_result.get('summary', 'N/A')}")
        
        # 4. Get research status
        print("\n4. Getting research status...")
        status = client.get_research_status(session_id)
        print(f"   Session: {status['session_id']}")
        print(f"   Status: {status['status']}")
        
        # 5. List reports
        print("\n5. Listing available reports...")
        reports = client.list_reports()
        print(f"   Total reports: {reports['count']}")
        
        if reports['reports']:
            latest_report = reports['reports'][0]
            print(f"   Latest: {latest_report['filename']}")
            
            # 6. Get specific report
            print("\n6. Getting latest report content...")
            report_id = latest_report['filename'].replace('research_report_', '').replace('.md', '')
            report = client.get_report(report_id)
            
            print(f"   Report ID: {report['report_id']}")
            print(f"   Size: {report['size']} characters")
            print(f"   Preview: {report['content'][:200]}...")
        
        print("\n✅ API client demo completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server.")
        print("   Make sure the API server is running: ./api/start_api.sh")
        
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ HTTP Error: {e}")
        print(f"   Response: {e.response.text}")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
