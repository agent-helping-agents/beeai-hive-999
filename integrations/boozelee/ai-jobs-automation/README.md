# AI Jobs Automation Project

**Project Status:** Active Development
**License:** MIT
**Version:** 0.1.0

## 🎯 Project Overview

This project provides **legal and ethical** automation tools for AI job applications. It helps streamline the application process while ensuring compliance with platform Terms of Service.

## 🚨 Important Legal Notice

❌ **DO NOT:**
- Create accounts programmatically without permission
- Bypass CAPTCHAs or security measures
- Use automation to spam applications
- Share or sell account credentials
- Violate platform Terms of Service

✅ **DO:**
- Use automation for personal productivity
- Follow each platform's rules
- Only automate repetitive, manual tasks
- Respect rate limits and guidelines
- Use official APIs when available

## 📋 Features

### 1. Browser Automation
- Selenium-based form filling for faster applications
- Manual review required before submission
- Platform-specific automation scripts

### 2. Email Management
- IMAP-based email organization
- Job application tracking
- Follow-up reminders

### 3. Application Tracking
- Automatic status updates
- Earnings tracking
- Platform comparison tools

### 4. API Integration
- Official API support for approved platforms
- Secure credential management
- Rate-limited requests

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-jobs-automation.git
cd ai-jobs-automation

# Install dependencies
pip install -r requirements.txt

# Set up credentials
cp .env.example .env
nano .env
```

## 🚀 Usage

### Basic Setup

```bash
# Initialize the project
python setup.py install

# Run the main application
python main.py
```

### Browser Automation

```python
from automation.browser import ScaleAIAutomation

# Create automation instance
automation = ScaleAIAutomation()

# Fill application form (requires manual review)
automation.fill_application(
    email="your_email@example.com",
    first_name="Your",
    last_name="Name"
)
```

### Email Management

```python
from automation.email import EmailManager

# Initialize email manager
email_manager = EmailManager(
    imap_server="imap.your-email.com",
    username="your_email@example.com",
    password="your_password"
)

# Get job-related emails
emails = email_manager.get_job_emails()
for email in emails:
    print(f"Subject: {email['subject']}")
    print(f"From: {email['from']}")
```

## 📂 Project Structure

```
ai-jobs-automation/
├── automation/
│   ├── browser.py          # Browser automation scripts
│   ├── email.py            # Email management
│   ├── tracker.py          # Application tracking
│   └── api.py              # API integrations
├── config/
│   ├── platforms/          # Platform-specific configurations
│   └── credentials.example # Example credentials file
├── docs/
│   ├── guides/             # User guides
│   └── api/                # API documentation
├── scripts/
│   ├── setup.py            # Setup script
│   └── utils.py            # Utility functions
├── tests/
│   ├── test_browser.py     # Browser automation tests
│   └── test_email.py       # Email management tests
├── .env.example            # Example environment file
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

## 🔑 Credentials Management

Create a `.env` file in the project root:

```env
# Email credentials
EMAIL_SERVER=imap.your-email.com
EMAIL_USERNAME=your_email@example.com
EMAIL_PASSWORD=your_password

# API keys (after manual account creation and approval)
SCALE_AI_API_KEY=your_approved_key_here
DATAANNOTATION_API_KEY=your_approved_key_here
APPEN_API_KEY=your_approved_key_here

# Browser automation settings
SELENIUM_DRIVER=chrome
HEADLESS_MODE=False
```

## 📊 Automation Safety Checklist

- [ ] **Manual Account Creation First** - Never automate account creation
- [ ] **Official APIs Only** - Only use documented, public APIs
- [ ] **Rate Limiting** - Respect platform rate limits
- [ ] **Manual Review** - Always review before final submission
- [ ] **Error Handling** - Handle errors gracefully
- [ ] **Logging** - Keep logs of automation activities
- [ ] **Compliance** - Follow all platform rules

## 🎯 Supported Platforms

### Priority Platforms
- **Scale AI / Remotasks** - Highest pay ($20-$125/hr)
- **DataAnnotation.tech** - Quick approval ($20-$30/hr)
- **Outlier AI** - Specialist roles ($15-$50/hr)

### Secondary Platforms
- **Appen / Crowdgen** - Flexible work ($15-$36/hr)
- **Lionbridge / Aurora AI** - Established platform ($14+/hr)
- **TELUS International** - Global opportunities ($14+/hr)

## 📚 Documentation

- [Application Guide](docs/guides/APPLICATION_GUIDE.md)
- [Automation Guide](docs/guides/AUTOMATION_GUIDE.md)
- [API Documentation](docs/api/API_DOCS.md)
- [Legal Compliance](docs/guides/LEGAL_COMPLIANCE.md)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Open a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Resources

- **Selenium Documentation**: https://www.selenium.dev/documentation/
- **Requests Library**: https://docs.python-requests.org/
- **IMAP with Python**: https://docs.python.org/3/library/imaplib.html
- **Scale AI API Docs**: https://docs.scale.com/
- **Ethical Web Scraping**: https://www.scrapingbee.com/blog/ethical-web-scraping/

**💡 Remember:** Automation should enhance your productivity, not replace your judgment. Always prioritize quality work and platform compliance.

**WATERMARK: PRIMAX-AI-BSP-2025**
© 2025 Bakery Street Project