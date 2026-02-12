"""
Zoho Mail Configuration for Mantis Agent

Domain: bakerstreetbandits.work.gd
Verification Code: 41845428
"""

import os

# Zoho Mail Settings
ZOHO_CONFIG = {
    "domain": "bakerstreetbandits.work.gd",
    "verification_code": "41845428",
    "verification_url": "http://bakerstreetbandits.work.gd/zohoverify/verifyforzoho.html",
    
    # IMAP Settings (for receiving)
    "imap_server": "imappro.zoho.com",
    "imap_port": 993,
    "imap_ssl": True,
    
    # SMTP Settings (for sending)
    "smtp_server": "smtp.zoho.com",
    "smtp_port": 587,  # TLS
    "smtp_ssl": False,
    "smtp_tls": True,
    
    # Alternative SMTP ports
    "smtp_port_ssl": 465,  # SSL
}

def get_zoho_credentials():
    """
    Get Zoho Mail credentials from environment.
    
    Required environment variables:
    - MANTIS_EMAIL_ADDRESS: Full email (e.g., hive@bakerstreetbandits.work.gd)
    - MANTIS_EMAIL_PASSWORD: Zoho Mail app password
    
    Returns:
        tuple: (email, password) or (None, None) if not set
    """
    email = os.getenv("MANTIS_EMAIL_ADDRESS")
    password = os.getenv("MANTIS_EMAIL_PASSWORD")
    return email, password

def verify_setup():
    """Verify Zoho Mail configuration is complete."""
    email, password = get_zoho_credentials()
    
    checks = {
        "Domain": ZOHO_CONFIG["domain"],
        "Verification Code": ZOHO_CONFIG["verification_code"],
        "Email Address": email if email else "NOT SET (set MANTIS_EMAIL_ADDRESS)",
        "App Password": "SET" if password else "NOT SET (set MANTIS_EMAIL_PASSWORD)",
        "IMAP Server": ZOHO_CONFIG["imap_server"],
        "SMTP Server": ZOHO_CONFIG["smtp_server"],
    }
    
    return checks

if __name__ == "__main__":
    print("=" * 50)
    print("Zoho Mail Configuration for Mantis Agent")
    print("=" * 50)
    
    for key, value in verify_setup().items():
        print(f"{key:20s}: {value}")
    
    print("=" * 50)
    print("\nTo complete setup:")
    print("1. Ensure domain verification is complete at Zoho")
    print("2. Set environment variables:")
    print("   export MANTIS_EMAIL_ADDRESS=hive@bakerstreetbandits.work.gd")
    print("   export MANTIS_EMAIL_PASSWORD=your_app_password")
    print("3. Test with: python agents/mantis_mail/mantis_agent.py")
