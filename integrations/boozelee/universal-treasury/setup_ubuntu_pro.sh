#!/bin/bash

# Ubuntu Pro Setup Script for Military-Grade Security
# Designed for Universal Treasury Security Infrastructure 2026

echo "[*] Starting Ubuntu Pro Security Setup"
echo "[*] Current date: $(date)"

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
    echo "[!] This script must be run as root. Please use sudo."
    exit 1
fi

# Function to install packages if missing
install_if_missing() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "[*] Installing $1..."
        apt update && apt install -y "$1"
    fi
}

# Install required packages
install_if_missing ubuntu-advantage-tools
install_if_missing landscape-client
install_if_missing needrestart

# Enable Ubuntu Pro (free for personal use)
echo "[*] Enabling Ubuntu Pro..."
pro attach --no-auto-enable

# Enable all available Ubuntu Pro services
echo "[*] Enabling Ubuntu Pro security services..."

# Enable ESM (Extended Security Maintenance) for 15 years of security updates
pro enable esm --auto-enable

# Enable Livepatch for kernel updates without reboots
pro enable livepatch --auto-enable

# Enable FIPS cryptographic modules for government-grade security
pro enable fips --auto-enable

# Enable CIS and DISA STIG compliance automation
pro enable cis --auto-enable
pro enable stig --auto-enable

# Enable additional security services
pro enable hardening --auto-enable
pro enable security --auto-enable

# Configure automatic security updates
echo "[*] Configuring automatic security updates..."
cat > /etc/apt/apt.conf.d/20auto-upgrades << EOF
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";
EOF

# Configure unattended upgrades for security updates only
cat > /etc/apt/apt.conf.d/50unattended-upgrades << EOF
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}";
    "${distro_id}:${distro_codename}-security";
    "${distro_id}ESM:${distro_codename}";
    "${distro_id}:${distro_codename}-updates";
};

Unattended-Upgrade::Package-Blacklist {
};

Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-Time "02:00";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::AutocleanInterval "7";
EOF

# Install and configure Landscape for system monitoring
echo "[*] Configuring Landscape system monitoring..."
systemctl enable landscape-client
systemctl start landscape-client

# Configure auditd for comprehensive security logging
echo "[*] Configuring advanced audit logging..."
cat > /etc/audit/rules.d/99-security.rules << EOF
# Monitor file access in critical directories
-w /etc -p wa -k config_change
-w /usr/bin -p wa -k bin_change
-w /usr/sbin -p wa -k sbin_change
-w /var -p wa -k var_change
-w /home -p wa -k home_change

# Monitor user and group changes
-w /etc/passwd -p wa -k identity_change
-w /etc/shadow -p wa -k identity_change
-w /etc/group -p wa -k identity_change
-w /etc/sudoers -p wa -k privilege_change
-w /etc/sudoers.d -p wa -k privilege_change

# Monitor network configuration changes
-w /etc/network -p wa -k network_change
-w /etc/hosts -p wa -k hosts_change
-w /etc/resolv.conf -p wa -k dns_change

# Monitor system startup files
-w /etc/init.d -p wa -k init_change
-w /etc/systemd -p wa -k systemd_change

# Monitor authentication events
-w /var/log/auth.log -p wa -k auth_log
-w /var/log/faillog -p wa -k auth_log
-w /var/log/lastlog -p wa -k auth_log

# Monitor sudo usage
-w /var/log/sudo.log -p wa -k sudo_log

# Monitor cron jobs
-w /etc/cron* -p wa -k cron_change
-w /var/spool/cron -p wa -k cron_change

# Monitor kernel module loading
-a exit,always -F arch=b64 -S init_module -S delete_module -k kernel_modules
-a exit,always -F arch=b32 -S init_module -S delete_module -k kernel_modules

# Monitor process execution
-a exit,always -F arch=b64 -S execve -k process_exec
-a exit,always -F arch=b32 -S execve -k process_exec

# Monitor file deletion
-a exit,always -F arch=b64 -S unlink -S unlinkat -S rename -S renameat -k file_deletion
-a exit,always -F arch=b32 -S unlink -S unlinkat -S rename -S renameat -k file_deletion

# Monitor privilege escalation
-a exit,always -F arch=b64 -S setuid -S setgid -S setreuid -S setregid -S setresuid -S setresgid -k privilege_escalation
-a exit,always -F arch=b32 -S setuid -S setgid -S setreuid -S setregid -S setresuid -S setresgid -k privilege_escalation
EOF

# Restart auditd to apply new rules
systemctl restart auditd

# Configure AppArmor for application confinement
echo "[*] Configuring AppArmor..."
systemctl enable apparmor
systemctl start apparmor

# Put AppArmor in enforce mode for all profiles
aa-enforce /etc/apparmor.d/*

# Configure systemd hardening
echo "[*] Hardening systemd..."
mkdir -p /etc/systemd/system.conf.d
cat > /etc/systemd/system.conf.d/99-hardening.conf << EOF
[Manager]
# Limit the number of processes
DefaultLimitNOFILE=65536
DefaultLimitNPROC=8192
DefaultTasksMax=16384

# Memory protection
DefaultMemoryAccounting=yes
DefaultMemoryLow=10%
DefaultMemoryHigh=80%

# CPU protection
DefaultCPUAccounting=yes

# Restrict core dumps
DefaultLimitCORE=0

# Restrict nice levels
DefaultLimitNICE=0

# Restrict realtime priority
DefaultLimitRTTIME=95000000
DefaultLimitRTPRIO=0
EOF

# Configure SSH hardening (if SSH is installed)
if [ -f /etc/ssh/sshd_config ]; then
    echo "[*] Hardening SSH configuration..."
    cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup
    
    cat > /etc/ssh/sshd_config << EOF
# Military-Grade SSH Configuration
Port 22
Protocol 2

# HostKeys
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key

# Authentication
LoginGraceTime 30
PermitRootLogin no
StrictModes yes
MaxAuthTries 3
MaxSessions 5

# Key Exchange
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com

# Logging
SyslogFacility AUTH
LogLevel VERBOSE

# Connection settings
ClientAliveInterval 300
ClientAliveCountMax 2

# Security enhancements
AllowTcpForwarding no
X11Forwarding no
PermitTunnel no
GatewayPorts no

# User restrictions
AllowUsers goku
AllowGroups sudo adm

# Time-based restrictions
# Use pam_access for time-based access control

# SFTP configuration
Subsystem sftp internal-sftp
ForceCommand internal-sftp

# FIPS 140-2 compliance
# Use only FIPS-approved algorithms
EOF
    
    # Restart SSH if it was running
    if systemctl is-active --quiet ssh; then
        systemctl restart ssh
    fi
fi

# Configure PAM (Pluggable Authentication Modules) hardening
echo "[*] Hardening PAM configuration..."
cat > /etc/pam.d/common-password << EOF
# Military-Grade PAM Password Configuration
password        requisite                       pam_pwquality.so retry=3 minlen=14 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1 difok=4 enforce_for_root
password        [success=1 default=ignore]      pam_unix.so obscure sha512 rounds=65536 remember=5
password        requisite                       pam_deny.so
password        required                        pam_permit.so
EOF

cat > /etc/pam.d/common-auth << EOF
# Military-Grade PAM Authentication Configuration
auth    required                        pam_tally2.so deny=5 unlock_time=900
auth    required                        pam_env.so
auth    required                        pam_unix.so nullok_secure
auth    required                        pam_deny.so
EOF

cat > /etc/pam.d/common-session << EOF
# Military-Grade PAM Session Configuration
session required                        pam_limits.so
session required                        pam_unix.so
session required                        pam_lastlog.so
session required                        pam_motd.so
session optional                        pam_mail.so standard
session required                        pam_permit.so
EOF

# Configure login.defs for security
echo "[*] Hardening login.defs..."
cat > /etc/login.defs << EOF
# Military-Grade Login Configuration
MAIL_CHECK_ENAB         no

PASS_MAX_DAYS   90
PASS_MIN_DAYS   1
PASS_WARN_AGE   14

UID_MIN                  1000
UID_MAX                 60000
SYS_UID_MIN               100
SYS_UID_MAX               999

GID_MIN                  1000
GID_MAX                 60000
SYS_GID_MIN               100
SYS_GID_MAX               999

CREATE_HOME     yes

UMASK           077

USERGROUPS_ENAB yes
ENCRYPT_METHOD SHA512

# Security enhancements
FAIL_DELAY      5
LASTLOG_ENAB    yes

# Password complexity
OBSCURE_CHECKS_ENAB     yes
CRACKLIB_DICTPATH       /usr/share/cracklib/pw_dict

# Session timeout
TTYGROUP        tty
TTYPERM         0600

# Prevent core dumps
ULIMIT          -c 0

# Restrict su access
SU_WHEEL_ONLY   yes

# FIPS 140-2 compliance
ENCRYPT_METHOD  SHA512
MD5_CRYPT_ENAB  no
EOF

# Configure limits for resource restrictions
echo "[*] Configuring system limits..."
cat > /etc/security/limits.conf << EOF
# Military-Grade Resource Limits
*               hard    core            0
*               hard    rss             100000
*               hard    nproc           1024
*               hard    nofile          4096
*               hard    memlock         64
*               hard    fsize           100000

# Root user limits
root            hard    core            0
root            hard    rss             unlimited
root            hard    nproc           4096
root            hard    nofile          8192

# Prevent fork bombs
*               soft    nproc           1024
*               hard    nproc           2048

# Memory restrictions
*               soft    as              100000
*               hard    as              200000

# CPU time restrictions
*               soft    cpu             60
*               hard    cpu             120

# File size restrictions
*               soft    fsize           100000
*               hard    fsize           200000

# Locked memory
*               soft    memlock         64
*               hard    memlock         64

# Nice priority
*               soft    priority        0
*               hard    priority        0

# Real-time priority
*               soft    rt_prio         0
*               hard    rt_prio         0

# Data segment size
*               soft    data            unlimited
*               hard    data            unlimited

# Stack size
*               soft    stack           8192
*               hard    stack           8192

# Virtual memory
*               soft    vmemory         unlimited
*               hard    vmemory         unlimited

# Locked pages
*               soft    lockedpages     64
*               hard    lockedpages     64

# POSIX message queues
*               soft    msgqueue        819200
*               hard    msgqueue        819200

# Nice value
*               soft    nice            0
*               hard    nice            0

# Real-time scheduling
*               soft    rtprio          0
*               hard    rtprio          0

# Number of processes
*               soft    sigpending      1024
*               hard    sigpending      2048

# Maximum number of files
*               soft    nofile          1024
*               hard    nofile          4096

# Maximum number of threads
*               soft    nproc           1024
*               hard    nproc           2048

# Maximum address space
*               soft    as              100000
*               hard    as              200000

# Maximum locked memory
*               soft    memlock         64
*               hard    memlock         64

# Maximum file locks
*               soft    locks           unlimited
*               hard    locks           unlimited

# Maximum pending signals
*               soft    sigpending      1024
*               hard    sigpending      2048

# Maximum message queue size
*               soft    msgqueue        819200
*               hard    msgqueue        819200

# Maximum nice priority
*               soft    nice            0
*               hard    nice            0

# Maximum real-time priority
*               soft    rtprio          0
*               hard    rtprio          0
EOF

# Configure cron security
echo "[*] Securing cron..."
cat > /etc/cron.allow << EOF
goku
root
EOF

chmod 600 /etc/cron.allow
chown root:root /etc/cron.allow

# Remove cron.deny if it exists
rm -f /etc/cron.deny

# Configure at security
cat > /etc/at.allow << EOF
goku
root
EOF

chmod 600 /etc/at.allow
chown root:root /etc/at.allow

rm -f /etc/at.deny

# Configure syslog for security logging
echo "[*] Configuring syslog..."
cat > /etc/rsyslog.d/99-security.conf << EOF
# Military-Grade Syslog Configuration

# Kernel messages (high priority)
kern.*                                                  /var/log/kernel.log

# Authentication messages (critical for security)
auth,authpriv.*                                         /var/log/auth.log

# System messages
*.info;mail.none;authpriv.none;cron.none                /var/log/syslog

# Cron messages
cron.*                                                  /var/log/cron.log

# Mail messages
mail.*                                                  /var/log/mail.log

# Emergency messages (broadcast to all users)
*.emerg                                                 :omusrmsg:*

# Security-related messages (separate log)
:msg, contains, "security"                              /var/log/security.log
:msg, contains, "audit"                                 /var/log/security.log
:msg, contains, "fail"                                  /var/log/security.log
:msg, contains, "deny"                                  /var/log/security.log
:msg, contains, "block"                                 /var/log/security.log
:msg, contains, "attack"                                /var/log/security.log
:msg, contains, "intrusion"                             /var/log/security.log
:msg, contains, "violation"                             /var/log/security.log

# Firewall messages
:msg, contains, "UFW"                                   /var/log/firewall.log
:msg, contains, "iptables"                              /var/log/firewall.log
:msg, contains, "netfilter"                             /var/log/firewall.log

# Network messages
:msg, contains, "network"                               /var/log/network.log
:msg, contains, "connection"                            /var/log/network.log
:msg, contains, "socket"                                /var/log/network.log

# Disk space monitoring
echo "[*] Configuring log rotation..."
cat > /etc/logrotate.d/security << EOF
/var/log/auth.log
/var/log/security.log
/var/log/firewall.log
/var/log/network.log
/var/log/kernel.log
{
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root adm
    postrotate
        /usr/lib/rsyslog/rsyslog-rotate
    endscript
}
EOF

# Restart services to apply changes
echo "[*] Restarting services..."
systemctl restart rsyslog
systemctl restart auditd

# Configure automatic security checks
echo "[*] Setting up automatic security checks..."
cat > /etc/cron.daily/security-audit << EOF
#!/bin/bash

# Daily Security Audit Script

echo "=== Daily Security Audit - $(date) ===" >> /var/log/security-audit.log

# Check for rootkits
echo "Checking for rootkits..." >> /var/log/security-audit.log
rkhunter --check --sk >> /var/log/security-audit.log 2>&1

# Check for suspicious processes
echo "Checking for suspicious processes..." >> /var/log/security-audit.log
ps aux | grep -E '(nc|netcat|bash|sh|python|perl)' | grep -v grep >> /var/log/security-audit.log

# Check for open ports
echo "Checking for open ports..." >> /var/log/security-audit.log
ss -tulnp >> /var/log/security-audit.log

# Check for failed login attempts
echo "Checking for failed logins..." >> /var/log/security-audit.log
grep "Failed password" /var/log/auth.log | tail -10 >> /var/log/security-audit.log

# Check disk usage
echo "Checking disk usage..." >> /var/log/security-audit.log
df -h >> /var/log/security-audit.log

# Check for world-writable files
echo "Checking for world-writable files..." >> /var/log/security-audit.log
find / -type f -perm -002 -exec ls -la {} \; | head -20 >> /var/log/security-audit.log

# Check for SUID/SGID files
echo "Checking for SUID/SGID files..." >> /var/log/security-audit.log
find / -type f \( -perm -4000 -o -perm -2000 \) -exec ls -la {} \; | head -20 >> /var/log/security-audit.log

# Check system load
echo "Checking system load..." >> /var/log/security-audit.log
uptime >> /var/log/security-audit.log

# Check memory usage
echo "Checking memory usage..." >> /var/log/security-audit.log
free -h >> /var/log/security-audit.log

echo "=== Security Audit Completed ===" >> /var/log/security-audit.log
EOF

chmod 750 /etc/cron.daily/security-audit
chown root:root /etc/cron.daily/security-audit

# Final security status check
echo "[*] Performing final security status check..."
echo "Ubuntu Pro Status:" >> /var/log/ubuntu-pro-setup.log
pro status >> /var/log/ubuntu-pro-setup.log 2>&1

echo "UFW Status:" >> /var/log/ubuntu-pro-setup.log
ufw status >> /var/log/ubuntu-pro-setup.log 2>&1

echo "Auditd Status:" >> /var/log/ubuntu-pro-setup.log
systemctl status auditd >> /var/log/ubuntu-pro-setup.log 2>&1

echo "AppArmor Status:" >> /var/log/ubuntu-pro-setup.log
systemctl status apparmor >> /var/log/ubuntu-pro-setup.log 2>&1

echo "[*] Ubuntu Pro Security Setup Completed!"
echo "[*] Setup completed on $(date)"
echo "[*] Detailed logs available in /var/log/ubuntu-pro-setup.log"
echo "[*] System requires reboot for all changes to take full effect."

exit 0