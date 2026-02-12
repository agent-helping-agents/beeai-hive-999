# AI Jobs Automation - Main Application

import os
from automation.browser import ScaleAIAutomation, DataAnnotationAutomation
from automation.email import EmailManager, ApplicationTracker
from automation.api import APIManager
from dotenv import load_dotenv

def main_menu():
    """Display main menu"""
    print("🎯 AI JOBS AUTOMATION SYSTEM")
    print("=" * 40)
    print("1. Scale AI Application Automation")
    print("2. DataAnnotation.tech Automation")
    print("3. Email Management")
    print("4. Application Tracking")
    print("5. API Integration")
    print("6. Exit")
    print()

def scale_ai_automation():
    """Scale AI application automation workflow"""
    print("🚀 SCALE AI APPLICATION AUTOMATION")
    print("=" * 40)
    
    # Get user information
    email = input("Enter your email: ")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    
    # Initialize automation
    automation = ScaleAIAutomation(headless=False)
    
    try:
        # Navigate to application
        automation.navigate_to_application()
        
        # Fill basic information
        automation.fill_basic_info(email, first_name, last_name)
        
        # Manual submission required
        automation.manual_submission_required()
        
        print("✅ Scale AI application process initiated")
        print("📝 Remember to complete manual submission")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        automation.close()

def dataannotation_automation():
    """DataAnnotation.tech automation workflow"""
    print("📝 DATAANNOTATION.TECH AUTOMATION")
    print("=" * 40)
    
    automation = DataAnnotationAutomation(headless=False)
    
    try:
        automation.apply_to_position()
        print("✅ DataAnnotation.tech application page opened")
        print("📝 Please complete the application manually")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        automation.close()

def email_management():
    """Email management workflow"""
    print("📧 EMAIL MANAGEMENT")
    print("=" * 40)
    
    email_manager = EmailManager()
    
    try:
        # Get job-related emails
        emails = email_manager.get_job_emails()
        
        if emails:
            print(f"\n📩 Found {len(emails)} job-related emails:")
            print("-" * 50)
            
            for i, email_data in enumerate(emails, 1):
                print(f"\n{i}. FROM: {email_data['from']}")
                print(f"   SUBJECT: {email_data['subject']}")
                print(f"   DATE: {email_data['date']}")
                print(f"   PREVIEW: {email_data['body'][:100]}...")
                print("-" * 50)
        else:
            print("📭 No job-related emails found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        email_manager.close()

def application_tracking():
    """Application tracking workflow"""
    print("📊 APPLICATION TRACKING")
    print("=" * 40)
    
    tracker = ApplicationTracker()
    
    try:
        # Show current status
        print("\n📋 Current Application Status:")
        with open(tracker.tracker_file, 'r') as f:
            content = f.read()
            # Show only the applications table
            lines = content.split('\n')
            in_table = False
            for line in lines:
                if '| Platform' in line:
                    in_table = True
                if in_table:
                    print(line)
                    if line.strip() == '' and '|' not in line:
                        break
        
        # Update status
        print("\n🔄 Update Application Status:")
        platform = input("Enter platform name: ")
        status = input("Enter new status: ")
        notes = input("Enter notes (optional): ")
        
        tracker.update_status(platform, status, notes=notes)
        print(f"✅ Updated {platform} to {status}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def api_integration():
    """API integration workflow"""
    print("🔑 API INTEGRATION")
    print("=" * 40)
    
    api_manager = APIManager()
    
    try:
        # Check API availability
        available_apis = api_manager.check_api_availability()
        
        if not any(available_apis.values()):
            print("\n📝 No APIs configured yet")
            print("📋 To configure APIs:")
            print("1. Create accounts manually on each platform")
            print("2. Request API access through platform dashboards")
            print("3. Add API keys to your .env file")
            print("4. Follow each platform's API documentation")
            return
        
        # API selection
        print("\n🎯 Available API Operations:")
        print("1. Get Scale AI Tasks")
        print("2. Get DataAnnotation Projects")
        print("3. Check API Status")
        print("4. Back to Main Menu")
        
        api_choice = input("Enter your choice (1-4): ")
        
        if api_choice == '1' and available_apis['scale_ai']:
            tasks = api_manager.scale_ai.get_available_tasks()
            if tasks:
                print(f"\n📋 Available Scale AI Tasks:")
                for i, task in enumerate(tasks[:5], 1):  # Show first 5 tasks
                    print(f"{i}. {task.get('title', 'Untitled Task')}")
        
        elif api_choice == '2' and available_apis['dataannotation']:
            projects = api_manager.dataannotation.get_projects()
            if projects:
                print(f"\n📋 Available DataAnnotation Projects:")
                for i, project in enumerate(projects[:5], 1):  # Show first 5 projects
                    print(f"{i}. {project.get('name', 'Unnamed Project')}")
        
        elif api_choice == '3':
            print("\n🔍 API Status:")
            for platform, available in available_apis.items():
                status = "✅ Configured" if available else "❌ Not configured"
                print(f"   {platform}: {status}")
        
        elif api_choice == '4':
            return
        
        else:
            print("❌ Invalid choice or API not available")
            
    except Exception as e:
        print(f"❌ API Error: {e}")

def main():
    """Main application entry point"""
    load_dotenv()
    
    print("🚨 LEGAL COMPLIANCE REMINDER:")
    print("✅ Manual account creation required")
    print("✅ Manual review before submission")
    print("✅ Follow platform Terms of Service")
    print("✅ Use only for personal productivity")
    print()
    
    while True:
        main_menu()
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            scale_ai_automation()
        elif choice == '2':
            dataannotation_automation()
        elif choice == '3':
            email_management()
        elif choice == '4':
            application_tracking()
        elif choice == '5':
            api_integration()
        elif choice == '6':
            print("👋 Thank you for using AI Jobs Automation")
            print("📝 Remember to complete all manual steps")
            break
        else:
            print("❌ Invalid choice. Please try again.")
        
        print()

if __name__ == "__main__":
    main()

# WATERMARK: PRIMAX-AI-BSP-2025
© 2025 Bakery Street Project