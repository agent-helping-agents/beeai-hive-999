# Baker Street Laboratory - Complete GitHub Setup Guide

This guide provides both **automated** and **manual** methods to complete the GitHub repository configuration.

## 🤖 **Automated Setup (Recommended)**

### Prerequisites
- GitHub CLI (`gh`) installed ✅
- Repository access permissions
- Internet connection

### Quick Start
```bash
# 1. Authenticate with GitHub
gh auth login --web

# 2. Run complete automated setup
./scripts/setup-github-complete.sh
```

### Individual Scripts
```bash
# Configure repository features and discussions
./scripts/configure-github.sh

# Enable GitHub Pages
./scripts/enable-github-pages.sh

# Validate all integrations
./scripts/validate-integration.sh
```

---

## 📋 **Manual Setup (If Automation Fails)**

### 1. **Enable Repository Features**

**Navigate to:** https://github.com/BoozeLee/Baker-Street-Laboratory/settings

**General Settings:**
- ✅ Issues
- ✅ Projects  
- ✅ Wiki
- ✅ Discussions
- ✅ Sponsorships

### 2. **Configure Repository Metadata**

**Click the ⚙️ gear icon next to "About":**

**Description:**
```
AI-Augmented Research Framework for Systematic Knowledge Discovery with Multi-Agent Pipeline
```

**Website:**
```
https://boozelee.github.io/Baker-Street-Laboratory
```

**Topics:**
```
ai-research, machine-learning, research-framework, multi-agent-system, python, automation, reproducible-research, data-science, github-actions, artificial-intelligence, research-tools, knowledge-discovery, scientific-computing, open-science, collaboration
```

### 3. **Enable GitHub Discussions**

**Navigate to:** Settings → General → Features
- ✅ Enable Discussions

**Create Categories:**
1. **General** (Discussion format) - "General discussions about Baker Street Laboratory"
2. **Research Questions** (Q&A format) - "Ask questions about research methodologies"
3. **Feature Requests** (Discussion format) - "Suggest new features and improvements"
4. **Show and Tell** (Discussion format) - "Share your research results and success stories"
5. **Research Collaboration** (Discussion format) - "Find collaborators and discuss joint research"
6. **Technical Support** (Q&A format) - "Get help with installation and troubleshooting"

### 4. **Configure Branch Protection**

**Navigate to:** Settings → Branches → Add rule

**Branch name pattern:** `main`

**Settings:**
- ✅ Require a pull request before merging
  - Required approvals: **1**
  - ✅ Dismiss stale reviews when new commits are pushed
  - ✅ Require review from code owners
- ✅ Require status checks to pass before merging
  - ✅ Require branches to be up to date before merging
- ✅ Include administrators

### 5. **Enable Security Features**

**Navigate to:** Settings → Security & analysis

**Enable:**
- ✅ Dependency graph
- ✅ Dependabot alerts
- ✅ Dependabot security updates
- ✅ Code scanning alerts
- ✅ Secret scanning alerts

### 6. **Configure GitHub Pages**

**Navigate to:** Settings → Pages

**Configuration:**
- Source: **Deploy from a branch**
- Branch: **main**
- Folder: **/ (root)**
- ✅ Enforce HTTPS

**Result:** https://boozelee.github.io/Baker-Street-Laboratory

---

## 🔍 **Verification Checklist**

### Repository Features
- [ ] Issues enabled and accessible
- [ ] Projects enabled and accessible
- [ ] Wiki enabled and accessible
- [ ] Discussions enabled with 6 categories
- [ ] Sponsorships enabled (sponsor button visible)

### Security & Protection
- [ ] Branch protection active on main branch
- [ ] Dependabot alerts enabled
- [ ] Security scanning enabled
- [ ] SECURITY.md file present
- [ ] CODEOWNERS file present

### Documentation & Pages
- [ ] GitHub Pages deployed and accessible
- [ ] README.md renders correctly as landing page
- [ ] All internal links work properly
- [ ] Sponsor badges display correctly

### Community Features
- [ ] Discussion categories created
- [ ] Issue templates working
- [ ] Pull request template working
- [ ] FUNDING.yml processed (sponsor button visible)

---

## 🌐 **Expected URLs After Setup**

| Feature | URL |
|---------|-----|
| Repository | https://github.com/BoozeLee/Baker-Street-Laboratory |
| GitHub Pages | https://boozelee.github.io/Baker-Street-Laboratory |
| Discussions | https://github.com/BoozeLee/Baker-Street-Laboratory/discussions |
| Issues | https://github.com/BoozeLee/Baker-Street-Laboratory/issues |
| Projects | https://github.com/BoozeLee/Baker-Street-Laboratory/projects |
| Wiki | https://github.com/BoozeLee/Baker-Street-Laboratory/wiki |
| Actions | https://github.com/BoozeLee/Baker-Street-Laboratory/actions |
| Security | https://github.com/BoozeLee/Baker-Street-Laboratory/security |

---

## 🚨 **Troubleshooting**

### Common Issues

**1. GitHub CLI Authentication**
```bash
# If authentication fails
gh auth logout
gh auth login --web
```

**2. Permission Errors**
- Ensure you have admin access to the repository
- Check if organization policies restrict certain features

**3. GitHub Pages Not Deploying**
- Wait 5-10 minutes for initial deployment
- Check Actions tab for deployment status
- Verify main branch has content

**4. Discussions Not Enabling**
- Some organization accounts may have restrictions
- Try enabling manually through web interface

**5. Branch Protection Conflicts**
- If you can't push to main, temporarily disable protection
- Re-enable after configuration is complete

### Getting Help

**Repository Issues:** https://github.com/BoozeLee/Baker-Street-Laboratory/issues
**Discussions:** https://github.com/BoozeLee/Baker-Street-Laboratory/discussions
**GitHub Support:** https://support.github.com/

---

## 📊 **Automation Script Details**

### `configure-github.sh`
- Enables repository features (Issues, Projects, Wiki, Discussions)
- Creates 6 discussion categories with proper formatting
- Configures security features (vulnerability alerts, Dependabot)
- Sets up branch protection rules
- Updates repository metadata and topics

### `enable-github-pages.sh`
- Enables GitHub Pages from main branch
- Configures deployment settings
- Verifies Pages configuration

### `validate-integration.sh`
- Tests all repository URLs for accessibility
- Validates feature enablement
- Checks security configuration
- Generates comprehensive status report

### `setup-github-complete.sh`
- Master script that runs all configuration steps
- Includes prerequisite checking
- Provides comprehensive setup logging

---

## 🎯 **Next Steps After Setup**

1. **Create First Discussion Post**
   - Welcome the community
   - Explain the research framework
   - Invite collaboration

2. **Set Up Project Boards**
   - Create research pipeline projects
   - Organize ongoing research tasks
   - Track research progress

3. **Invite Collaborators**
   - Add team members with appropriate permissions
   - Set up research groups
   - Configure notification preferences

4. **Promote Repository**
   - Share with research community
   - Submit to relevant directories
   - Engage with potential users

5. **Monitor Analytics**
   - Track repository engagement
   - Monitor sponsor conversions
   - Analyze community growth

---

**🔬 Your Baker Street Laboratory is ready for world-class AI research! 🚀**
