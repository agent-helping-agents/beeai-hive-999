#!/usr/bin/env python3
"""
Bakery Street Project - Organization Test Suite
Comprehensive testing for organization profile and project validation
"""

import os
import sys
import json
import unittest
from pathlib import Path

class TestOrganizationProfile(unittest.TestCase):
    """Test organization profile completeness and accuracy"""
    
    def setUp(self):
        """Set up test environment"""
        self.base_path = Path(__file__).parent.parent
        self.readme_path = self.base_path / "README.md"
        self.logo_path = self.base_path / "image.jpg"
        
    def test_readme_exists(self):
        """Test that README.md exists and is readable"""
        self.assertTrue(self.readme_path.exists(), "README.md should exist")
        self.assertTrue(self.readme_path.is_file(), "README.md should be a file")
        
    def test_readme_content(self):
        """Test README content for essential sections"""
        if not self.readme_path.exists():
            self.skipTest("README.md not found")
            
        content = self.readme_path.read_text(encoding='utf-8')
        
        # Check for essential sections
        essential_sections = [
            "Bakery Street Project",
            "Mission",
            "Vision", 
            "Featured Projects",
            "Technology Stack",
            "Contact",
            "Services"
        ]
        
        for section in essential_sections:
            with self.subTest(section=section):
                self.assertIn(section, content, f"README should contain '{section}' section")
    
    def test_logo_exists(self):
        """Test that organization logo exists"""
        self.assertTrue(self.logo_path.exists(), "Organization logo should exist")
        self.assertTrue(self.logo_path.is_file(), "Organization logo should be a file")
        
    def test_readme_has_projects(self):
        """Test that README mentions key projects"""
        if not self.readme_path.exists():
            self.skipTest("README.md not found")
            
        content = self.readme_path.read_text(encoding='utf-8')
        
        key_projects = [
            "Poly-AI Framework",
            "DYADS",
            "Voidshatter",
            "PeakyBlenders"
        ]
        
        for project in key_projects:
            with self.subTest(project=project):
                self.assertIn(project, content, f"README should mention '{project}' project")
    
    def test_readme_has_tech_stack(self):
        """Test that README includes technology stack"""
        if not self.readme_path.exists():
            self.skipTest("README.md not found")
            
        content = self.readme_path.read_text(encoding='utf-8')
        
        tech_keywords = [
            "Python",
            "JavaScript",
            "AI/ML",
            "Docker",
            "Kubernetes"
        ]
        
        found_tech = sum(1 for tech in tech_keywords if tech in content)
        self.assertGreaterEqual(found_tech, 3, "README should mention at least 3 technology keywords")
    
    def test_readme_has_contact_info(self):
        """Test that README includes contact information"""
        if not self.readme_path.exists():
            self.skipTest("README.md not found")
            
        content = self.readme_path.read_text(encoding='utf-8')
        
        contact_indicators = [
            "Contact",
            "Email",
            "LinkedIn",
            "GitHub",
            "Website"
        ]
        
        found_contact = sum(1 for indicator in contact_indicators if indicator in content)
        self.assertGreaterEqual(found_contact, 2, "README should include contact information")

class TestProjectStructure(unittest.TestCase):
    """Test project structure and organization"""
    
    def setUp(self):
        """Set up test environment"""
        self.base_path = Path(__file__).parent.parent
        
    def test_requirements_file(self):
        """Test that requirements.txt exists and has content"""
        req_path = self.base_path / "requirements.txt"
        self.assertTrue(req_path.exists(), "requirements.txt should exist")
        
        if req_path.exists():
            content = req_path.read_text(encoding='utf-8')
            self.assertGreater(len(content.strip()), 100, "requirements.txt should have substantial content")
    
    def test_git_repository(self):
        """Test that this is a valid git repository"""
        git_path = self.base_path / ".git"
        self.assertTrue(git_path.exists(), "Should be a git repository")
        self.assertTrue(git_path.is_dir(), ".git should be a directory")
    
    def test_file_structure(self):
        """Test basic file structure"""
        required_files = [
            "README.md",
            "requirements.txt",
            "image.jpg"
        ]
        
        for file_name in required_files:
            with self.subTest(file=file_name):
                file_path = self.base_path / file_name
                self.assertTrue(file_path.exists(), f"{file_name} should exist")

class TestOrganizationMetrics(unittest.TestCase):
    """Test organization metrics and statistics"""
    
    def setUp(self):
        """Set up test environment"""
        self.base_path = Path(__file__).parent.parent
        self.readme_path = self.base_path / "README.md"
        
    def test_metrics_mentioned(self):
        """Test that key metrics are mentioned in README"""
        if not self.readme_path.exists():
            self.skipTest("README.md not found")
            
        content = self.readme_path.read_text(encoding='utf-8')
        
        # Look for business metrics
        metric_indicators = [
            "$2.5M",
            "ROI",
            "customers",
            "projects",
            "repositories"
        ]
        
        found_metrics = sum(1 for metric in metric_indicators if metric in content)
        self.assertGreaterEqual(found_metrics, 2, "README should mention business metrics")

def run_tests():
    """Run all tests and return results"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestOrganizationProfile,
        TestProjectStructure,
        TestOrganizationMetrics
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return results
    return {
        'tests_run': result.testsRun,
        'failures': len(result.failures),
        'errors': len(result.errors),
        'success': result.wasSuccessful()
    }

if __name__ == '__main__':
    print("🧪 Bakery Street Project - Organization Test Suite")
    print("=" * 60)
    
    results = run_tests()
    
    print("\n📊 Test Results Summary")
    print("-" * 30)
    print(f"Tests Run: {results['tests_run']}")
    print(f"Failures: {results['failures']}")
    print(f"Errors: {results['errors']}")
    print(f"Success: {'✅' if results['success'] else '❌'}")
    
    if results['success']:
        print("\n🎉 All tests passed! Organization profile is complete.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the output above.")
        sys.exit(1)
