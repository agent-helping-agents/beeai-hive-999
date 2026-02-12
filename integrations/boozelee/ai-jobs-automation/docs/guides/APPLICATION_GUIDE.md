# AI Jobs Application Guide

**Last Updated:** 2026-01-17
**Project:** AI Jobs Automation System

## 🎯 Overview

This guide provides step-by-step instructions for using the AI Jobs Automation System to streamline your job applications while maintaining full compliance with platform Terms of Service.

## 📋 Getting Started

### Prerequisites

- Python 3.8+
- Chrome browser installed
- Valid email account
- Manual accounts created on target platforms

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-jobs-automation.git
cd ai-jobs-automation

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
nano .env
```

### Configuration

Edit your `.env` file:

```env
# Email Configuration
EMAIL_SERVER=imap.your-email.com
EMAIL_USERNAME=your_email@example.com
EMAIL_PASSWORD=your_app_specific_password

# Browser Automation
SELENIUM_DRIVER=chrome
HEADLESS_MODE=False
```

**Important:** Use an app-specific password for your email account for security.

## 🚀 Using the System

### Main Menu

```bash
python main.py
```

The main menu provides access to all features:

1. **Scale AI Application Automation** - Automate Scale AI applications
2. **DataAnnotation.tech Automation** - Automate DataAnnotation applications
3. **Email Management** - Organize job-related emails
4. **Application Tracking** - Track application status
5. **API Integration** - Use official platform APIs
6. **Exit** - Close the application

### Scale AI Automation

1. Select option 1 from the main menu
2. Enter your email, first name, and last name
3. The system will navigate to Scale AI careers page
4. **Manual Review Required:**
   - Review all pre-filled information
   - Complete any platform-specific questions
   - Verify all information is accurate
   - Click submit manually
5. The system will confirm completion

### DataAnnotation.tech Automation

1. Select option 2 from the main menu
2. The system will navigate to the job posting
3. **Manual Review Required:**
   - Complete the application form manually
   - Follow all platform instructions
   - Submit the application manually

### Email Management

1. Select option 3 from the main menu
2. The system will connect to your email
3. It will search for emails from:
   - scale.com
   - dataannotation.tech
   - appen.com
   - lionbridge.com
4. Results will be displayed with:
   - Sender information
   - Subject line
   - Date received
   - Message preview

### Application Tracking

1. Select option 4 from the main menu
2. View current application status table
3. Update status:
   - Enter platform name
   - Enter new status (e.g., "Applied", "Assessment Received", "Approved")
   - Add optional notes
4. The system will update your tracker file

### API Integration

1. Select option 5 from the main menu
2. The system will check which APIs are configured
3. Available operations:
   - Get Scale AI Tasks (if API key configured)
   - Get DataAnnotation Projects (if API key configured)
   - Check API Status
4. **Important:** API keys must be obtained manually through each platform

## 📊 Application Strategy

### Priority Platforms

Apply in this order for best results:

1. **Scale AI / Remotasks** - Highest pay ($20-$125/hr)
2. **DataAnnotation.tech** - Quick approval ($20-$30/hr)
3. **Outlier AI** - Specialist roles ($15-$50/hr)

### Daily Checklist

**Day 1:**
- [ ] Apply to Scale AI / Remotasks
- [ ] Apply to DataAnnotation.tech
- [ ] Apply to Outlier AI
- [ ] Start Appen/Crowdgen signup

**Day 2:**
- [ ] Complete remaining applications
- [ ] Search and apply to 5 Indeed postings
- [ ] Check email for assessment tests

**Day 3-5:**
- [ ] Complete assessment tests
- [ ] Follow up on applications
- [ ] Start first assignments

## 🎯 Success Metrics

### Week 1 Goals:
- 5+ applications submitted
- 2+ assessment tests completed
- 1+ platform approved
- First work assignment received

### Month 1 Goals:
- 3+ platforms approved
- 100+ hours of work completed
- $2,000+ earned
- 4.5+ average rating

## 📝 Best Practices

### Legal Compliance
- ✅ Manual account creation first
- ✅ Manual review before submission
- ✅ Follow platform Terms of Service
- ✅ Respect rate limits
- ✅ Use only official APIs

### Quality Assurance
- ✅ Complete profiles thoroughly
- ✅ Follow instructions precisely
- ✅ Maintain high quality work
- ✅ Meet all deadlines
- ✅ Build good ratings first

### Security
- ✅ Use app-specific passwords
- ✅ Keep API keys secure
- ✅ Never share credentials
- ✅ Use HTTPS connections
- ✅ Keep software updated

## 🚨 Troubleshooting

### Common Issues

**Browser Automation Errors:**
- Ensure Chrome is installed
- Check Selenium driver compatibility
- Run in non-headless mode for debugging
- Update browser and drivers

**Email Connection Issues:**
- Verify IMAP is enabled for your email
- Check firewall settings
- Use correct server address
- Test with app-specific password

**API Errors:**
- Verify API keys are correct
- Check rate limits
- Review platform API documentation
- Test with platform API tools first

## 📚 Resources

### Platform Links
- Scale AI: https://scale.com/careers
- DataAnnotation: https://dataannotation.tech
- Indeed Search: https://www.indeed.com/q-data-annotation-l-remote-jobs.html

### Documentation
- Selenium: https://www.selenium.dev/documentation/
- IMAP with Python: https://docs.python.org/3/library/imaplib.html
- Scale AI API: https://docs.scale.com/

### Support
- GitHub Issues: https://github.com/yourusername/ai-jobs-automation/issues
- Email: support@bakery-street-project.com

## 🔑 Legal Compliance Checklist

Before using this system, ensure you:

- [ ] Have manually created accounts on all platforms
- [ ] Have read and understood each platform's Terms of Service
- [ ] Will manually review all applications before submission
- [ ] Will not automate account creation
- [ ] Will not bypass security measures
- [ ] Will respect all rate limits and guidelines
- [ ] Will use the system only for personal productivity

## 📋 Changelog

**v0.1.0 (2026-01-17):**
- Initial release
- Browser automation for Scale AI and DataAnnotation
- Email management system
- Application tracking
- API integration framework

**WATERMARK: PRIMAX-AI-BSP-2025**
© 2025 Bakery Street Project