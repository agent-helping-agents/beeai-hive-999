#!/bin/bash

# Military-Grade UFW/IPtables Firewall Setup for Ubuntu 26.04
# Designed for Universal Treasury Security Infrastructure

echo "[*] Starting Military-Grade Firewall Configuration"
echo "[*] Current date: $(date)"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
    echo "[!] This script must be run as root. Please use sudo."
    exit 1
fi

# Install required packages if missing
if ! command_exists ufw; then
    echo "[*] Installing UFW..."
    apt update && apt install -y ufw iptables-persistent
fi

# Reset UFW to default state
echo "[*] Resetting UFW to default state..."
ufw --force reset

# Set default policies - DROP everything by default
echo "[*] Setting default DROP policies..."
ufw default deny incoming
ufw default deny outgoing
ufw default deny routed

# Enable UFW logging for security monitoring
echo "[*] Enabling comprehensive logging..."
ufw logging on
ufw logging medium

# Allow loopback interface (critical for system operation)
echo "[*] Configuring loopback interface..."
ufw allow in on lo
ufw allow out on lo

# Allow established and related connections
echo "[*] Allowing established/related connections..."
ufw allow in proto tcp from any to any state RELATED,ESTABLISHED
ufw allow in proto udp from any to any state RELATED,ESTABLISHED
ufw allow out proto tcp from any to any state RELATED,ESTABLISHED
ufw allow out proto udp from any to any state RELATED,ESTABLISHED

# Allow DNS (critical for internet connectivity)
echo "[*] Configuring DNS access..."
ufw allow out 53/tcp
ufw allow out 53/udp
ufw allow out 5353/udp  # mDNS

# Allow NTP for time synchronization (security critical)
echo "[*] Configuring NTP access..."
ufw allow out 123/udp

# Allow HTTPS for secure web access
echo "[*] Configuring secure web access..."
ufw allow out 443/tcp

# Allow HTTP (can be restricted later for privacy)
echo "[*] Configuring web access..."
ufw allow out 80/tcp

# Allow SSH (restricted to specific IPs later)
echo "[*] Configuring SSH access..."
ufw allow out 22/tcp

# Universal Treasury specific ports (restrict to localhost or specific networks)
echo "[*] Configuring Universal Treasury ports..."
ufw allow in 4330/tcp comment "Universal Treasury API"
ufw allow in 44321/tcp comment "Universal Treasury Service 1"
ufw allow in 44322/tcp comment "Universal Treasury Service 2"  
ufw allow in 44323/tcp comment "Universal Treasury Service 3"

# Restrict Kerberos services to localhost only
echo "[*] Securing Kerberos services..."
ufw deny in 88/tcp comment "Block Kerberos TCP"
ufw deny in 88/udp comment "Block Kerberos UDP"
ufw deny in 464/tcp comment "Block Kerberos Password Change"
ufw deny in 464/udp comment "Block Kerberos Password Change UDP"
ufw deny in 749/tcp comment "Block Kerberos Admin"
ufw deny in 750/tcp comment "Block Kerberos IV"

# Restrict SMTP to localhost only (prevent open relay)
echo "[*] Securing SMTP service..."
ufw deny in 25/tcp comment "Block SMTP from external"

# Restrict RADIUS services
echo "[*] Securing RADIUS services..."
ufw deny in 1812/udp comment "Block RADIUS Authentication"
ufw deny in 1813/udp comment "Block RADIUS Accounting"

# Allow ICMP for network diagnostics (ping)
echo "[*] Configuring ICMP..."
ufw allow out proto icmp
ufw allow in proto icmp

# Rate limiting to prevent brute force attacks
echo "[*] Implementing rate limiting..."
ufw limit 22/tcp comment "SSH rate limiting"
ufw limit 4330/tcp comment "Treasury API rate limiting"

# Enable UFW
echo "[*] Enabling UFW..."
ufw --force enable

# Additional IPtables rules for advanced security
echo "[*] Adding advanced IPtables rules..."

# Create custom chains for advanced filtering
iptables -N LOGGING
iptables -N PORTSCAN
iptables -N MALICIOUS

# Log and drop port scanning attempts
iptables -A INPUT -p tcp --tcp-flags SYN,ACK,FIN,RST RST -m limit --limit 1/s -j LOGGING
iptables -A INPUT -p tcp --tcp-flags SYN,ACK,FIN,RST RST -j DROP

# Log and drop invalid packets
iptables -A INPUT -m conntrack --ctstate INVALID -j LOGGING
iptables -A INPUT -m conntrack --ctstate INVALID -j DROP

# Log and drop new connections that are not SYN packets
iptables -A INPUT -p tcp ! --syn -m conntrack --ctstate NEW -j LOGGING
iptables -A INPUT -p tcp ! --syn -m conntrack --ctstate NEW -j DROP

# Log and drop fragments
iptables -A INPUT -f -j LOGGING
iptables -A INPUT -f -j DROP

# Log and drop XMAS packets
iptables -A INPUT -p tcp --tcp-flags ALL ALL -j LOGGING
iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP

# Log and drop NULL packets
iptables -A INPUT -p tcp --tcp-flags ALL NONE -j LOGGING
iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP

# Logging chain configuration
iptables -A LOGGING -m limit --limit 2/min -j LOG --log-prefix "[UFW BLOCK] " --log-level 4
iptables -A LOGGING -j DROP

# Save IPtables rules
echo "[*] Saving IPtables rules..."
iptables-save > /etc/iptables/rules.v4
ip6tables-save > /etc/iptables/rules.v6

# Enable IPtables persistence
echo "[*] Enabling IPtables persistence..."
systemctl enable netfilter-persistent
systemctl start netfilter-persistent

# Configure sysctl for additional network security
echo "[*] Hardening kernel network parameters..."
cat > /etc/sysctl.d/99-security-hardening.conf << EOF
# IP Spoofing protection
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# Ignore ICMP broadcast requests
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Disable source packet routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv6.conf.default.accept_source_route = 0

# Ignore send redirects
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0

# Block SYN attacks
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 5

# Log Martians
net.ipv4.conf.all.log_martians = 1
net.ipv4.conf.default.log_martians = 1

# Ignore ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0

# Ignore Directed pings
net.ipv4.icmp_echo_ignore_all = 1

# Disable IPv6 if not needed (can be enabled for IPv6 networks)
# net.ipv6.conf.all.disable_ipv6 = 1
# net.ipv6.conf.default.disable_ipv6 = 1
EOF

# Apply sysctl changes
sysctl -p /etc/sysctl.d/99-security-hardening.conf

echo "[*] Firewall configuration completed!"
echo "[*] Current UFW status:"
ufw status numbered
echo "[*] Current IPtables rules:"
iptables -L -n --line-numbers

echo "[*] Security hardening completed on $(date)"
echo "[*] System requires reboot for all changes to take full effect."
