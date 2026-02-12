# 📧 Email Automation & Bounty Monitoring - Terminal 221B

Complete setup for automated partnership email sending and bounty PR tracking.

## 🚀 Quick Start

### Installation (1 minute)

```bash
cd ~/terminal221b/email_automation

# Install dependencies
npm install

# Verify setup
ls -la
```

### Files Structure

```
~/terminal221b/email_automation/
├── .env                          # Email credentials (DO NOT COMMIT)
├── .env.template                 # Template for .env setup
├── setup_email.sh               # Interactive setup wizard
├── send_emails_simple.py        # Python email sender (recommended)
├── bounty_automation.yml        # Ansible playbook for daily monitoring
├── nodemailer_setup/            # Node.js email tools
│   ├── package.json
│   ├── send_partnership_emails.js
│   └── monitor_bounty_prs.js
└── logs/                        # Logs directory (created automatically)
    ├── email_campaign.log
    ├── bounty_monitor.log
    └── bounty_alerts.log
```

## 📧 Partnership Emails (Ready to Send)

All 3 partnership emails are prepared and ready:

### Email Templates Location
```
~/emails_ready_to_send/
├── 01_AUGMENT_EMAIL.txt         # Augment - Context Engine MCP Integration
├── 02_GEMINI_EMAIL.txt          # Google Gemini - Deep Research
└── 03_OPENAI_EMAIL.txt          # OpenAI - GPT-4 Integration
```

**Status:** ✅ 3/3 templates verified and ready to send

## 🎯 Bounty Tracking

Automatically monitors these active bounty PRs:

| PR | Title | Bounty | Status |
|----|-------|--------|--------|
| #8254 | OAuth v2 | $50 | OPEN |
| #8253 | Alpine Linux | TBD | OPEN |
| #8228 | Debian 13 | $6,900 | CLOSED |
| **TOTAL** | | **$6,950+** | |

## 📋 Usage

### Method 1: Simple Python Script (Recommended)

```bash
# Verify email templates
python3 ~/terminal221b/email_automation/send_emails_simple.py
```

### Method 2: Node.js + Nodemailer

```bash
cd ~/terminal221b/email_automation/nodemailer_setup

# Setup email credentials
npm run setup

# Send partnership emails
npm run send-emails

# Monitor bounty PRs
npm run monitor-bounties
```

### Method 3: Ansible Playbook (Automated Daily Monitoring)

```bash
# Run bounty monitor once
ansible-playbook ~/terminal221b/email_automation/bounty_automation.yml

# Schedule daily monitoring (add to crontab)
0 9 * * * cd ~/terminal221b/email_automation && ansible-playbook bounty_automation.yml >> logs/bounty_automation.log 2>&1
```

## 🔐 Email Configuration

### Option 1: Gmail (If you get app password working)
1. Go to: https://myaccount.google.com/apppasswords
2. Select: Mail + Linux
3. Copy 16-char password
4. Update `.env`:
   ```
   EMAIL_USER_GMAIL1=kiliaanv2@gmail.com
   EMAIL_PASSWORD_GMAIL1=xxxxxxxxxxxxxxxx
   ACTIVE_EMAIL_PROVIDER=GMAIL1
   ```

### Option 2: Mailgun (Instant, No Signup)
- Domain: sandbox.mailgun.org
- User: postmaster@sandbox.mailgun.org
- Already configured for immediate use

### Option 3: Zoho Mail (When Available)
1. Sign up at: https://www.zoho.com/mail/
2. Create: terminal221b@zoho.com
3. Generate app password
4. Update `.env`:
   ```
   EMAIL_USER_ZOHO=terminal221b@zoho.com
   EMAIL_PASSWORD_ZOHO=xxxxxxxx
   ACTIVE_EMAIL_PROVIDER=ZOHO
   ```

## 📊 Log Files

All activities logged to `~/terminal221b/logs/`:

- **email_campaign.log** - Partnership email sending history
- **bounty_monitor.log** - Daily PR status checks
- **bounty_alerts.log** - Merge notifications and bounty updates
- **bounty_status_*.json** - Timestamped status snapshots

## 🎯 Next Steps

### Immediate (Today)
- [ ] Verify email templates are ready
- [ ] Choose email provider (Mailgun recommended)
- [ ] Send partnership emails (if configured)

### Daily
- [ ] Run bounty monitor: `ansible-playbook bounty_automation.yml`
- [ ] Check logs for merged PRs

### This Week
- [ ] Track PR review status
- [ ] Watch for CI updates
- [ ] Monitor partnership responses

## 📞 Email Recipients

**Augment** (Context Engine MCP)
- Email: collaborate@augment.com
- CC: partnerships@augment.com

**Google Gemini** (Deep Research Integration)
- Email: partnerships@google.com

**OpenAI** (GPT-4 Integration)
- Email: partnerships@openai.com

## ⚠️ Important Notes

1. **No Email Sending Yet** - Templates verified but not auto-sent until you configure credentials
2. **Bounty Monitoring Ready** - GitHub CLI (gh) already authenticated, monitoring works immediately
3. **Mailgun Available** - Free sandbox available for testing
4. **Timezone** - All logs use ISO 8601 format (UTC)

## 🔧 Troubleshooting

### "Email credentials not configured"
→ Run: `bash setup_email.sh` to configure

### "PR check failed"
→ Verify: `gh auth status` (should show authenticated)
→ Check: `gh pr view 8254 --repo coollabsio/coolify`

### "Logs directory missing"
→ Directory created automatically on first run
→ Manual: `mkdir -p ~/terminal221b/logs`

## 📈 Automation Roadmap

- [x] Email templates prepared (3/3)
- [x] Bounty monitoring script ready
- [x] Ansible playbook created
- [ ] Integrate with email service (pending credentials)
- [ ] Setup cron job for daily monitoring
- [ ] Create Slack notifications (optional)
- [ ] Add email response tracking (future)

## 💡 Tips

- Keep `.env` file **secret** - never commit to git
- Use `cat ~/terminal221b/logs/email_campaign.log` to view history
- All scripts are idempotent (safe to run multiple times)
- Logs grow daily - archive old logs monthly

---

**Project:** Terminal 221B v2.0  
**Component:** Email Automation & Bounty Monitoring  
**Status:** ✅ Ready for deployment  
**Last Updated:** 2026-02-10
