# Baker Street Laboratory - Automation Scripts

This directory contains automated scripts for configuring the GitHub repository with all necessary features and integrations.

## 🚀 **Quick Start**

### Complete Automated Setup
```bash
# Authenticate with GitHub (one-time setup)
gh auth login --web

# Run complete automation
./scripts/setup-github-complete.sh
```

## 📜 **Available Scripts**

### `setup-github-complete.sh` - Master Setup Script
**Purpose:** Runs all configuration scripts in the correct order
**Usage:** `./scripts/setup-github-complete.sh`
**Features:**
- Prerequisites checking
- Complete repository configuration
- GitHub Pages setup
- Integration validation
- Comprehensive reporting

### `configure-github.sh` - Repository Configuration
**Purpose:** Configures core repository features and community settings
**Usage:** `./scripts/configure-github.sh`
**Features:**
- Enables Issues, Projects, Wiki, Discussions
- Creates 6 discussion categories
- Configures security features (Dependabot, vulnerability alerts)
- Sets up branch protection rules
- Updates repository metadata and topics

### `enable-github-pages.sh` - GitHub Pages Setup
**Purpose:** Enables and configures GitHub Pages for documentation
**Usage:** `./scripts/enable-github-pages.sh`
**Features:**
- Enables Pages deployment from main branch
- Configures HTTPS enforcement
- Verifies deployment status
- Provides deployment URL

### `validate-integration.sh` - Integration Testing
**Purpose:** Validates all GitHub integrations and features
**Usage:** `./scripts/validate-integration.sh`
**Features:**
- Tests repository feature enablement
- Validates discussion categories
- Checks security configuration
- Tests URL accessibility
- Generates comprehensive status report

## 🔧 **Prerequisites**

### Required Tools
- **GitHub CLI (`gh`)** - For API interactions ✅ Installed
- **jq** - For JSON processing (auto-installed if missing)
- **curl** - For URL testing (usually pre-installed)

### Authentication
```bash
# Login to GitHub CLI (required for all scripts)
gh auth login --web

# Verify authentication
gh auth status
```

### Permissions
- Repository admin access
- Ability to modify repository settings
- Permission to enable organization features (if applicable)

## 📊 **Script Outputs**

### Success Indicators
- ✅ Green checkmarks for successful operations
- 🎉 Completion messages with URLs
- 📊 Status reports with feature verification

### Warning Indicators
- ⚠️ Yellow warnings for non-critical issues
- 💡 Information messages for manual steps
- 🔄 Progress indicators for long operations

### Error Indicators
- ❌ Red errors for failed operations
- 🚨 Critical issues requiring attention
- 📋 Troubleshooting guidance

## 🔍 **Troubleshooting**

### Common Issues

**Authentication Errors**
```bash
# Solution: Re-authenticate
gh auth logout
gh auth login --web
```

**Permission Denied**
- Verify repository admin access
- Check organization policies
- Ensure feature availability for account type

**API Rate Limits**
- Wait for rate limit reset (usually 1 hour)
- Use personal access token with higher limits
- Run scripts during off-peak hours

**Network Issues**
- Check internet connectivity
- Verify GitHub API accessibility
- Try running scripts with verbose output

### Debug Mode
```bash
# Run scripts with debug output
bash -x ./scripts/configure-github.sh
```

### Manual Fallback
If automation fails, follow the manual setup guide:
- See `docs/GITHUB_SETUP.md` for step-by-step instructions
- Use GitHub web interface for configuration
- Validate setup with `./scripts/validate-integration.sh`

## 📋 **Configuration Details**

### Repository Features Enabled
- **Issues:** Bug reports and feature requests
- **Projects:** Research pipeline management
- **Wiki:** Extended documentation
- **Discussions:** Community engagement
- **Sponsorships:** Funding integration

### Discussion Categories Created
1. **General** (Discussion) - General discussions
2. **Research Questions** (Q&A) - Research methodology questions
3. **Feature Requests** (Discussion) - New feature suggestions
4. **Show and Tell** (Discussion) - Research results sharing
5. **Research Collaboration** (Discussion) - Collaboration opportunities
6. **Technical Support** (Q&A) - Installation and troubleshooting

### Security Features Configured
- **Dependabot Alerts** - Vulnerability notifications
- **Automated Security Fixes** - Automatic dependency updates
- **Code Scanning** - Static analysis security scanning
- **Secret Scanning** - Credential leak detection
- **Branch Protection** - Main branch protection rules

### Metadata Configuration
- **Description:** AI-Augmented Research Framework for Systematic Knowledge Discovery
- **Topics:** 15 relevant tags for discoverability
- **Homepage:** GitHub Pages URL
- **License:** MIT License
- **Funding:** Multiple sponsorship platforms

## 🌐 **Expected Results**

After successful execution, your repository will have:

### Professional Presentation
- 🏆 Complete repository metadata
- 🔒 Security-first configuration
- 💖 Multiple sponsorship options
- 📊 Rich discoverability tags

### Community Features
- 💬 Active discussion categories
- 🐛 Professional issue templates
- 🔍 Code review requirements
- 📋 Project management capabilities

### Documentation
- 📄 Live GitHub Pages site
- 📚 Comprehensive README
- 🔐 Security policy
- 🤝 Contribution guidelines

### Integration Status
- ✅ All features enabled and tested
- 🔗 All URLs accessible
- 🛡️ Security scanning active
- 📊 Analytics and insights enabled

## 🎯 **Next Steps**

After running the automation scripts:

1. **Verify Setup**
   ```bash
   ./scripts/validate-integration.sh
   ```

2. **Visit Your Repository**
   - https://github.com/BoozeLee/Baker-Street-Laboratory
   - Test all features and links

3. **Create Initial Content**
   - First discussion post
   - Project board setup
   - Wiki page creation

4. **Invite Collaborators**
   - Add team members
   - Set permissions
   - Configure notifications

5. **Promote Repository**
   - Share with community
   - Submit to directories
   - Engage with users

---

**🔬 Happy Researching with Baker Street Laboratory! 🚀**
