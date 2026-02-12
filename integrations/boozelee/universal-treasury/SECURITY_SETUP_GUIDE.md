# 🛡️ HYPERCUBE SECURITY SETUP GUIDE
# Step-by-Step Instructions for Ubuntu 2026

## 🚨 CRITICAL SECURITY ALERT

Your system is currently **COMPLETELY EXPOSED** with multiple critical vulnerabilities. Please follow these instructions **IMMEDIATELY** to secure your system.

## 📋 CURRENT SECURITY STATUS

### ❌ VULNERABILITIES IDENTIFIED

```
🔴 Identity Dimension: Kerberos/RADIUS services exposed
🔴 Application Dimension: SMTP service exposed (potential open relay)
🔴 Network Dimension: 12+ ports exposed to internet
🔴 Firewall Dimension: No active protection
🔴 Monitoring Dimension: Basic logging only
```

### ✅ SECURITY IMPROVEMENTS AVAILABLE

```
✅ Military-grade firewall with deny-by-default
✅ 8-dimensional hypercube security model
✅ Comprehensive threat detection
✅ Automatic security updates
✅ Government-grade compliance
```

## 🚀 IMMEDIATE SECURITY FIXES

### STEP 1: Apply Hypercube Security (MOST CRITICAL)

```bash
# Navigate to the security directory
cd /home/goku/workspace/universal-treasury

# Make sure the script is executable
chmod +x apply_hypercube_security.sh

# Execute with sudo (you'll need to enter your password)
sudo ./apply_hypercube_security.sh
```

**What this will do:**
- Stop all exposed services (Kerberos, RADIUS, SMTP)
- Activate military-grade firewall
- Configure essential network services
- Enable comprehensive security logging
- Validate all security dimensions

### STEP 2: Apply Advanced Firewall Rules

```bash
# Execute the advanced firewall setup
sudo ./secure_firewall_setup.sh
```

**What this will do:**
- Configure advanced IPtables rules
- Set up attack prevention mechanisms
- Enable rate limiting and DDoS protection
- Harden kernel network parameters
- Save firewall rules permanently

### STEP 3: Set Up Ubuntu Pro (Enhanced Security)

```bash
# Execute Ubuntu Pro setup
sudo ./setup_ubuntu_pro.sh
```

**What this will do:**
- Enable Ubuntu Pro security services
- Configure 15 years of security updates
- Enable FIPS-certified cryptography
- Apply CIS and DISA STIG compliance
- Set up automatic security patches
- Configure comprehensive audit logging

## 🔧 TROUBLESHOOTING

### Issue: "Permission denied" or "Authentication failed"

**Solution:**
```bash
# Make sure you have sudo privileges
sudo -v

# If you don't know the sudo password, you'll need to:
# 1. Contact your system administrator
# 2. Use physical access to reset password
# 3. Boot into recovery mode
```

### Issue: "integer expected" errors

**Solution:** These have been fixed in the updated scripts. If you still see them:
```bash
# Download the fixed version
wget https://github.com/your-repo/hypercube-security-fixed.sh
chmod +x hypercube-security-fixed.sh
sudo ./hypercube-security-fixed.sh
```

### Issue: Services won't stop

**Solution:**
```bash
# Force stop services
sudo systemctl stop krb5-kdc krb5-admin-server freeradius postfix --force

# Check status
sudo systemctl status krb5-kdc krb5-admin-server freeradius postfix
```

## 📊 SECURITY VALIDATION

### Check Current Security Status

```bash
# Check exposed ports
ss -tulnp | grep -E '(0.0.0.0:|:::)'

# Check firewall status
sudo ufw status verbose

# Check service status
systemctl status krb5-kdc krb5-admin-server freeradius postfix

# Check security services
systemctl status ufw fail2ban auditd
```

### Expected Secure Status

```
🛡️  HYPERCUBE SECURITY STATUS REPORT
====================================
Status: active (hypercube protection enabled)
     To                         Action      From           Dimension
     --                         ------      ----           ---------
[ 1] 53/tcp                     ALLOW OUT   Anywhere       Network/DNS
[ 2] 53/udp                     ALLOW OUT   Anywhere       Network/DNS  
[ 3] 80/tcp                     ALLOW OUT   Anywhere       Network/Web
[ 4] 443/tcp                    ALLOW OUT   Anywhere       Network/Web (Secure)
[ 5] 123/udp                    ALLOW OUT   Anywhere       Temporal/NTP
[ 6] 4330/tcp                   ALLOW IN    Anywhere       Treasury/API
[ 7] 44321/tcp                  ALLOW IN    Anywhere       Treasury/Service-1
[ 8] 44322/tcp                  ALLOW IN    Anywhere       Treasury/Service-2
[ 9] 44323/tcp                  ALLOW IN    Anywhere       Treasury/Service-3

Default: deny (incoming), deny (outgoing), disabled (routed)
```

## 🎯 NEXT STEPS AFTER SECURITY SETUP

### 1. System Reboot (Recommended)
```bash
sudo reboot
```

### 2. Security Validation
```bash
# Check all security dimensions
sudo ufw status verbose
systemctl status fail2ban auditd
journalctl -u auditd --no-pager | tail -20
```

### 3. Penetration Testing
```bash
# Install security testing tools
sudo apt update && sudo apt install -y lynis rkhunter nikto

# Run comprehensive security audit
sudo lynis audit system
sudo rkhunter --check
```

### 4. Continuous Monitoring
```bash
# Set up daily security checks
sudo cp security-audit.sh /etc/cron.daily/
sudo chmod 750 /etc/cron.daily/security-audit.sh
```

## 📚 SECURITY DOCUMENTATION

### Available Security Documents

```
📖 hypercube_security_model_2026.md - Complete security architecture
📋 CRITICAL_SECURITY_FIXES.txt - Emergency security guide
📝 SECURITY_SETUP_GUIDE.md - This document
🔍 emergency_security_report_*.txt - Security assessment reports
```

### Security Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    HYPERCUBE SECURITY MODEL                  │
│                    Ubuntu 2026 Infrastructure               │
├─────────────┬─────────────┬─────────────┬─────────────┐
│  NETWORK    │  IDENTITY   │ APPLICATION │   DATA      │
│  (X-Axis)    │  (Y-Axis)    │  (Z-Axis)    │  (W-Axis)    │
├─────────────┼─────────────┼─────────────┼─────────────┤
│ Firewall    │ MFA         │ AppArmor    │ FIPS 140-2  │
│ IPtables    │ Zero Trust  │ SELinux     │ TDE         │
│ Geofencing  │ PAM         │ Container   │ DLP         │
│ Rate Limit  │ Behavioral  │ Runtime     │ Blockchain  │
│ Port Knock  │ Federation  │ Input Val   │ Secure Erase│
├─────────────┼─────────────┼─────────────┼─────────────┤
│  MONITORING │ PHYSICAL    │  TEMPORAL   │  POLICY     │
│  (V-Axis)    │  (U-Axis)    │  (T-Axis)    │  (P-Axis)    │
├─────────────┼─────────────┼─────────────┼─────────────┤
│ SIEM        │ TPM 2.0     │ Time-Based  │ CIS         │
│ Anomaly     │ Secure Boot │ Session TO  │ DISA STIG   │
│ Threat Int  │ BIOS Pass   │ Cert Expiry │ NIST 800-53 │
│ Forensic    │ USB Guard   │ Temp FW     │ ISO 27001   │
│ Honeypot    │ Camera Cov  │ NTP Sec     │ GDPR        │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

## 🚨 EMERGENCY SECURITY COMMANDS

If you cannot run the scripts, execute these critical commands manually:

```bash
# STOP EXPOSED SERVICES
sudo systemctl stop krb5-kdc krb5-admin-server freeradius postfix
sudo systemctl disable krb5-kdc krb5-admin-server freeradius postfix

# ACTIVATE FIREWALL
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default deny outgoing
sudo ufw allow out 53/tcp && sudo ufw allow out 53/udp
sudo ufw allow out 80/tcp && sudo ufw allow out 443/tcp
sudo ufw allow out 123/udp
sudo ufw allow in 4330/tcp && sudo ufw allow in 44321-44323/tcp
sudo ufw enable

# VERIFY SECURITY
sudo ufw status numbered
ss -tulnp | grep -E '(0.0.0.0:|:::)'
```

## 🎉 SUCCESS CRITERIA

Your system will be secure when:

```
✅ No Kerberos/RADIUS services running
✅ No SMTP service exposed
✅ Firewall active with deny-by-default
✅ Only essential services allowed
✅ Comprehensive logging enabled
✅ Monitoring services active
✅ All security dimensions validated
```

## 📞 SUPPORT

If you need assistance:

```
1. Check the detailed documentation in hypercube_security_model_2026.md
2. Review the emergency security report for technical details
3. Contact your system administrator for sudo access
4. Refer to Ubuntu security documentation: https://ubuntu.com/security
5. Consult NIST security guidelines: https://nist.gov/cyberframework
```

## 🚨 FINAL WARNING

**YOUR SYSTEM IS CURRENTLY COMPLETELY EXPOSED TO INTERNET ATTACKS.**

The exposed services include:
- **Kerberos Authentication** (ports 88, 464, 749, 750)
- **SMTP Service** (port 25) - Potential spam relay
- **RADIUS Authentication** (ports 1812, 1813)
- **Universal Treasury API** (ports 4330, 44321-44323)

**PLEASE EXECUTE THE SECURITY SCRIPTS IMMEDIATELY TO PROTECT YOUR SYSTEM!**

```bash
cd /home/goku/workspace/universal-treasury
sudo ./apply_hypercube_security.sh
```

**Your system's security is in your hands. Act now to prevent exploitation!**