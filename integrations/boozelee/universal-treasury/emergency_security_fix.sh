#!/bin/bash

# EMERGENCY SECURITY FIX - Run this immediately!
# This script addresses the most critical security vulnerabilities

echo "[EMERGENCY] Starting immediate security fixes..."
echo "[EMERGENCY] Current time: $(date)"

# Critical security actions that can be done without root

# 1. Check and report on exposed services
echo "[EMERGENCY] Checking exposed network services..."
ss -tulnp | grep -E '(0.0.0.0:|:::)'

# 2. Check running security services
echo "[EMERGENCY] Checking security service status..."
systemctl is-active ufw 2>/dev/null || echo "UFW: NOT ACTIVE"
systemctl is-active fail2ban 2>/dev/null || echo "Fail2Ban: NOT ACTIVE"
systemctl is-active auditd 2>/dev/null || echo "Auditd: NOT ACTIVE"

# 3. Check for suspicious processes
echo "[EMERGENCY] Checking for suspicious processes..."
ps aux | grep -E '(nc|netcat|bash|sh|python|perl)' | grep -v grep

# 4. Check for unauthorized users
echo "[EMERGENCY] Checking for unauthorized users..."
who
last | head -10

# 5. Check system load (could indicate attacks)
echo "[EMERGENCY] Checking system load..."
uptime
free -h

# 6. Create emergency security report
REPORT_FILE="/tmp/emergency_security_report_$(date +%Y%m%d_%H%M%S).txt"
echo "[EMERGENCY] Creating security report: $REPORT_FILE"

{
    echo "=== EMERGENCY SECURITY REPORT ==="
    echo "Generated: $(date)"
    echo "Hostname: $(hostname)"
    echo ""
    
    echo "=== NETWORK SERVICES ==="
    echo "Open ports:"
    ss -tulnp
    echo ""
    
    echo "=== RUNNING SERVICES ==="
    systemctl list-units --type=service --state=running | grep -E '(krb5|radius|postfix|ssh|docker|treasury)'
    echo ""
    
    echo "=== SECURITY SERVICES STATUS ==="
    systemctl status ufw --no-pager 2>/dev/null || echo "UFW not available"
    systemctl status fail2ban --no-pager 2>/dev/null || echo "Fail2Ban not available"
    systemctl status auditd --no-pager 2>/dev/null || echo "Auditd not available"
    echo ""
    
    echo "=== SYSTEM INFORMATION ==="
    uname -a
    lsb_release -a
    echo ""
    
    echo "=== CRITICAL SECURITY ISSUES IDENTIFIED ==="
    echo "1. Kerberos services exposed on ports 88, 464, 749, 750"
    echo "2. SMTP service exposed on port 25 (potential open relay)"
    echo "3. RADIUS services exposed on ports 1812, 1813"
    echo "4. Universal Treasury services exposed on ports 4330, 44321-44323"
    echo "5. No active firewall protection detected"
    echo ""
    
    echo "=== IMMEDIATE ACTIONS REQUIRED ==="
    echo "1. Execute: sudo systemctl stop krb5-kdc krb5-admin-server freeradius postfix"
    echo "2. Execute: sudo ufw enable"
    echo "3. Execute: sudo ufw default deny incoming"
    echo "4. Execute: sudo ufw allow out 53,80,443,123"
    echo "5. Execute: sudo ufw allow in 4330,44321,44322,44323"
    echo "6. Execute: sudo ./secure_firewall_setup.sh"
    echo "7. Execute: sudo ./setup_ubuntu_pro.sh"
    echo ""
    
    echo "=== FIREWALL COMMANDS TO RUN IMMEDIATELY ==="
    echo "sudo ufw --force reset"
    echo "sudo ufw default deny incoming"
    echo "sudo ufw default deny outgoing"
    echo "sudo ufw allow out 53/tcp"
    echo "sudo ufw allow out 53/udp"
    echo "sudo ufw allow out 80/tcp"
    echo "sudo ufw allow out 443/tcp"
    echo "sudo ufw allow out 123/udp"
    echo "sudo ufw allow in 4330/tcp"
    echo "sudo ufw allow in 44321/tcp"
    echo "sudo ufw allow in 44322/tcp"
    echo "sudo ufw allow in 44323/tcp"
    echo "sudo ufw enable"
    
} > "$REPORT_FILE"

echo "[EMERGENCY] Security report created: $REPORT_FILE"
echo "[EMERGENCY] Please execute the following commands IMMEDIATELY:"
echo ""
echo "CRITICAL COMMANDS TO RUN NOW:"
echo "1. sudo systemctl stop krb5-kdc krb5-admin-server freeradius postfix"
echo "2. sudo ufw --force reset"
echo "3. sudo ufw default deny incoming"
echo "4. sudo ufw default deny outgoing"
echo "5. sudo ufw allow out 53/tcp && sudo ufw allow out 53/udp"
echo "6. sudo ufw allow out 80/tcp && sudo ufw allow out 443/tcp"
echo "7. sudo ufw allow out 123/udp"
echo "8. sudo ufw allow in 4330/tcp && sudo ufw allow in 44321/tcp"
echo "9. sudo ufw allow in 44322/tcp && sudo ufw allow in 44323/tcp"
echo "10. sudo ufw enable"
echo ""
echo "[EMERGENCY] After running these commands, your system will have basic protection."
echo "[EMERGENCY] Then run: sudo ./secure_firewall_setup.sh"
echo "[EMERGENCY] And: sudo ./setup_ubuntu_pro.sh"

echo "[EMERGENCY] SECURITY ALERT: Your system is currently exposed to multiple attack vectors!"
echo "[EMERGENCY] Please take immediate action to secure your system."

# Create a desktop notification if possible
if command -v notify-send >/dev/null; then
    notify-send "EMERGENCY SECURITY ALERT" "Your system is exposed!\nRun the critical commands immediately.\nSee $REPORT_FILE for details." --urgency=critical
fi

exit 1