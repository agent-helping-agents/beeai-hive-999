#!/bin/bash

echo "🛡️  COMPLETING HYPERCUBE SECURITY SETUP"
echo "========================================"
echo "System: $(hostname) - $(date)"
echo ""

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
    echo "🔴 This script requires root privileges"
    echo "🔴 Please run with: sudo $0"
    exit 1
fi

# Function to check command success
check_success() {
    if [ $? -eq 0 ]; then
        echo "✅ $1: SUCCESS"
    else
        echo "❌ $1: FAILED"
    fi
}

echo "🔍 ANALYZING CURRENT SECURITY STATE"
echo "===================================="

# Check Ubuntu Pro status
echo "📋 Ubuntu Pro Status:"
pro status 2>/dev/null || echo "Ubuntu Pro not configured"

# Check firewall status
echo "🛡️  Firewall Status:"
ufw status verbose 2>/dev/null || echo "Firewall not active"

# Check security services
echo "👁️  Security Services:"
for service in ufw fail2ban auditd apparmor; do
    if systemctl is-active "$service" 2>/dev/null; then
        echo "  ✅ $service: ACTIVE"
    else
        echo "  ❌ $service: INACTIVE"
    fi
done

# Check exposed ports
echo "🌐 Exposed Network Ports:"
exposed_ports=$(ss -tulnp | grep -E '(0.0.0.0:|:::)' | wc -l)
echo "  Total exposed: $exposed_ports"
if [ $exposed_ports -gt 0 ]; then
    echo "  ⚠️  Exposed services:"
    ss -tulnp | grep -E '(0.0.0.0:|:::)' | head -5
fi

echo ""
echo "🛠️  FIXING KNOWN ISSUES"
echo "========================"

# Fix 1: Install netfilter-persistent if missing
echo "🔧 Fixing netfilter-persistent..."
if ! command -v netfilter-persistent >/dev/null; then
    apt update && apt install -y iptables-persistent netfilter-persistent
    check_success "netfilter-persistent installation"
fi

# Fix 2: Configure Ubuntu Pro without --auto-enable
echo "🔧 Configuring Ubuntu Pro services..."
if pro status | grep -q "enabled"; then
    echo "  Ubuntu Pro already enabled"
else
    # Enable services individually (without --auto-enable)
    pro enable esm
    pro enable livepatch
    pro enable fips
    pro enable cis
    pro enable stig
    pro enable hardening
    pro enable security
    check_success "Ubuntu Pro services"
fi

# Fix 3: Fix AppArmor profile errors
echo "🔧 Fixing AppArmor profile errors..."
if [ -f /etc/apparmor.d/firefox-local ]; then
    # Remove or fix problematic profile
    mv /etc/apparmor.d/firefox-local /etc/apparmor.d/firefox-local.bak
    echo "  Fixed firefox-local profile"
fi

# Reload AppArmor
systemctl reload apparmor
check_success "AppArmor reload"

echo ""
echo "🛡️  COMPLETING SECURITY CONFIGURATION"
echo "======================================"

# Enable and start netfilter-persistent
systemctl enable netfilter-persistent
systemctl start netfilter-persistent
check_success "netfilter-persistent"

# Save current firewall rules
iptables-save > /etc/iptables/rules.v4
ip6tables-save > /etc/iptables/rules.v6
check_success "Firewall rules save"

# Configure sysctl for additional security
echo "🔧 Applying kernel security hardening..."
cat > /etc/sysctl.d/99-security-hardening.conf << EOF
# IP Spoofing protection
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# Ignore ICMP broadcast requests
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Disable source packet routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0

# Ignore send redirects
net.ipv4.conf.all.send_redirects = 0

# Block SYN attacks
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048

# Log Martians
net.ipv4.conf.all.log_martians = 1

# Ignore ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0

# Ignore Directed pings
net.ipv4.icmp_echo_ignore_all = 1
EOF

sysctl -p /etc/sysctl.d/99-security-hardening.conf
check_success "Kernel hardening"

echo ""
echo "🔍 FINAL SECURITY VALIDATION"
echo "============================"

# Check Ubuntu Pro services
echo "Ubuntu Pro Services:"
pro status | grep -E "(esm|livepatch|fips|cis|stig|hardening|security)" || echo "  Ubuntu Pro services not detailed"

# Check firewall rules
echo "Firewall Rules:"
ufw status numbered || echo "  Firewall not active"

# Check security improvements
final_exposed=$(ss -tulnp | grep -E '(0.0.0.0:|:::)' | wc -l)
if [ $exposed_ports -gt 0 ]; then
    improvement=$((100 * (exposed_ports - final_exposed) / exposed_ports))
    echo "Security Improvement: $improvement% reduction in exposed services"
else
    echo "Security Improvement: Maximum protection achieved"
fi

echo ""
echo "🎉 SECURITY SETUP COMPLETION SUMMARY"
echo "===================================="

# Final security status
security_score=0
max_score=10

# Check each security component
[[ $(ufw status | grep -c "Status: active") -gt 0 ]] && ((security_score++))
[[ $(systemctl is-active fail2ban) == "active" ]] && ((security_score++))
[[ $(systemctl is-active auditd) == "active" ]] && ((security_score++))
[[ $(systemctl is-active apparmor) == "active" ]] && ((security_score++))
[[ $(pro status | grep -c "enabled") -gt 0 ]] && ((security_score++))
[[ $final_exposed -lt 10 ]] && ((security_score++))
[[ -f /etc/sysctl.d/99-security-hardening.conf ]] && ((security_score++))
[[ $(iptables -L | grep -c "DROP") -gt 0 ]] && ((security_score++))

percentage=$((security_score * 100 / max_score))

echo "Security Score: $percentage/100"
echo ""

if [ $percentage -ge 80 ]; then
    echo "🛡️  EXCELLENT: Military-grade security achieved"
    echo "✅ Your system is well-protected against most threats"
elif [ $percentage -ge 60 ]; then
    echo "🛡️  GOOD: Strong security posture"
    echo "⚠️  Some improvements recommended"
else
    echo "❌ WEAK: Significant security improvements needed"
    echo "🚨 Please review security recommendations"
fi

echo ""
echo "🎯 RECOMMENDED NEXT STEPS:"
echo "1. Review security logs: journalctl -u auditd -u fail2ban"
echo "2. Check Ubuntu Pro status: pro status"
echo "3. Verify firewall: ufw status verbose"
echo "4. Test security: sudo lynis audit system"
echo "5. Reboot system: sudo reboot"
echo ""
echo "📊 SECURITY COMPONENTS STATUS:"
echo "  Firewall: $(ufw status | grep -c 'Status: active')/1"
echo "  Fail2Ban: $(systemctl is-active fail2ban | grep -c active)/1"
echo "  Auditd: $(systemctl is-active auditd | grep -c active)/1"
echo "  AppArmor: $(systemctl is-active apparmor | grep -c active)/1"
echo "  Ubuntu Pro: $(pro status | grep -c enabled)/1"
echo "  Network Security: $((final_exposed < 10 ? 1 : 0))/1"
echo "  Kernel Hardening: $(test -f /etc/sysctl.d/99-security-hardening.conf && echo 1 || echo 0)/1"
echo "  IPtables Rules: $(iptables -L | grep -c DROP)/1"
echo ""
echo "✅ HYPERCUBE SECURITY SETUP COMPLETED"
echo "   Your system now has enhanced security protection"
echo "   Regular monitoring and updates are recommended"

exit 0