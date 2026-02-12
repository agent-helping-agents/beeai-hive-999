# 🔒 Secure Hive 999 ⟷ Terminal 221b Communication

This document describes the security-hardened implementation for communication between Hive 999 and Terminal 221b.

---

## 📋 Security Features Implemented

### 1. Authentication & Authorization

| Feature | Implementation | Status |
|---------|----------------|--------|
| JWT Tokens | `python-jose` with HS256 | ✅ |
| Token Expiry | 30 minutes access, 7 days refresh | ✅ |
| Password Hashing | Argon2 (bcrypt fallback) | ✅ |
| Role-Based Access | Admin/User roles | ✅ |
| Account Lockout | 15 min after 5 failed attempts | ✅ |
| Token Revocation | Revoked token registry | ✅ |

### 2. API Security

| Feature | Implementation | Status |
|---------|----------------|--------|
| Rate Limiting | `slowapi` - 100 req/min default | ✅ |
| Input Validation | Pydantic v2 models | ✅ |
| XSS Prevention | `nh3` HTML sanitization | ✅ |
| Secure Headers | FastAPI built-in + middleware | ✅ |
| CORS Protection | Configurable allowed origins | ✅ |
| Trusted Hosts | Host header validation | ✅ |

### 3. Transport Security

| Feature | Implementation | Status |
|---------|----------------|--------|
| TLS/HTTPS | Configurable certificate paths | ✅ |
| SSL Verification | Client-side verification | ✅ |
| Certificate Pinning | Optional in client | ✅ |

### 4. Audit & Monitoring

| Feature | Implementation | Status |
|---------|----------------|--------|
| Request Logging | All requests logged with IP/UA hash | ✅ |
| Auth Logging | Success/failure tracked | ✅ |
| Security Events | Dedicated security log | ✅ |
| Investigation Audit | Query + duration logged | ✅ |

### 5. Secrets Management

| Feature | Implementation | Status |
|---------|----------------|--------|
| Encrypted Storage | Fernet encryption for tokens | ✅ |
| Memory-Only | No disk storage of credentials | ✅ |
| Environment Variables | Config via env vars | ✅ |
| Secure Permissions | 0o600 on key files | ✅ |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SECURITY ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐         ┌──────────────────┐         ┌──────────────┐ │
│  │   🐝 Hive 999    │         │   🔒 Security    │         │ 🕵️ T-221b    │ │
│  │                  │◄───────►│      Layer       │◄───────│   API Server │ │
│  │  - Secure Client │         │                  │         │              │ │
│  │  - TUI Controller│         │  - Rate Limiting │         │  - JWT Auth  │ │
│  │  - Audit Logging │         │  - Input Sanitiz.│         │  - RBAC      │ │
│  │                  │         │  - TLS/mTLS      │         │  - Audit Log │ │
│  └──────────────────┘         └──────────────────┘         └──────────────┘ │
│                                                                              │
│  Security Layers:                                                            │
│  1. Network: TLS 1.2+, Certificate pinning                                  │
│  2. Transport: HTTPS, CORS, Trusted Hosts                                   │
│  3. Authentication: JWT with short expiry                                   │
│  4. Authorization: Role-based access control                                │
│  5. Application: Rate limiting, input validation                            │
│  6. Audit: Comprehensive logging and monitoring                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Secure Files Created

| File | Purpose | Lines | Security Features |
|------|---------|-------|-------------------|
| `terminal_221b/api/secure_server.py` | Hardened API server | 600+ | JWT, Rate limiting, RBAC, Audit |
| `secure_hive_client.py` | Secure client | 500+ | Token mgmt, Encryption, Retry logic |
| `secure_tui_integration.py` | TUI integration | 400+ | Secure input, Auto-reconnect |

---

## 🔐 Default Credentials (CHANGE IN PRODUCTION!)

```yaml
# Admin user - Full access
username: admin
password: ChangeMe123!
roles: [admin, user]

# Hive user - Limited access
username: hive
password: HiveConnect2024!
roles: [user]
```

⚠️ **IMPORTANT**: Change these passwords immediately in production!

---

## 🚀 Usage

### 1. Start Secure Server

```bash
# Set environment variables (optional)
export T221B_SECRET_KEY="your-256-bit-secret-key-here"
export T221B_RATE_LIMIT="100"
export T221B_TOKEN_EXPIRY="30"

# Start server
python terminal_221b/api/secure_server.py
```

### 2. Connect with Secure Client

```python
from secure_hive_client import SecureTerminal221bClient

client = SecureTerminal221bClient(
    base_url="http://localhost:22181",
    username="hive",
    password="HiveConnect2024!",
    verify_ssl=False  # Set True with cert_path in production
)

# Connect and authenticate
await client.connect()
await client.authenticate()

# Use API
result = await client.investigate(
    query="Analyze address...",
    personality="holmes"
)
```

### 3. TUI Integration

```python
from secure_tui_integration import SecureTUIController

controller = SecureTUIController()
await controller.connect("hive", "HiveConnect2024!")

# In TUI command handler
result = await controller.investigate("Analyze address...")
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `T221B_SECRET_KEY` | Random | JWT signing key |
| `T221B_TOKEN_EXPIRY` | 30 | Access token expiry (minutes) |
| `T221B_REFRESH_EXPIRY` | 7 | Refresh token expiry (days) |
| `T221B_RATE_LIMIT` | 100 | Requests per window |
| `T221B_RATE_WINDOW` | 60 | Rate limit window (seconds) |
| `T221B_TLS_CERT` | None | TLS certificate path |
| `T221B_TLS_KEY` | None | TLS private key path |
| `T221B_ALLOWED_HOSTS` | localhost,127.0.0.1 | Allowed hosts |
| `T221B_CORS_ORIGINS` | None | Allowed CORS origins |
| `T221B_AUDIT_LOG` | /tmp/t221b_audit.log | Audit log path |
| `T221B_ENABLE_DOCS` | None | Enable Swagger/ReDoc |

### TLS/HTTPS Setup

```bash
# Generate self-signed certificate (development only)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Set environment variables
export T221B_TLS_CERT="/path/to/cert.pem"
export T221B_TLS_KEY="/path/to/key.pem"

# Start server - will use HTTPS
python terminal_221b/api/secure_server.py
```

---

## 📊 Security Testing

### Test Authentication

```bash
# Get token
curl -X POST http://localhost:22181/token \
  -H "Content-Type: application/json" \
  -d '{"username":"hive","password":"HiveConnect2024!"}'

# Response: {"access_token":"...","token_type":"bearer","expires_in":1800}
```

### Test Rate Limiting

```bash
# Make 101 requests quickly - should hit rate limit
for i in {1..101}; do
  curl -s http://localhost:22181/health | head -1
done
```

### Test Input Validation

```bash
# XSS attempt - should be sanitized
curl -X POST http://localhost:22181/investigate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"<script>alert(1)</script>","personality":"holmes"}'
```

### Test Authorization

```bash
# Admin endpoint with user token - should fail
curl -H "Authorization: Bearer $USER_TOKEN" \
  http://localhost:22181/admin/stats
# Response: 403 Forbidden
```

---

## 🔍 Audit Logs

### Server Audit Log

Location: `/tmp/t221b_audit.log`

```
2024-01-15 10:30:45 - audit - INFO - REQUEST: ip=127.0.0.1 user=hive method=POST path=/investigate action=investigate_holmes ua=a1b2c3d4...
2024-01-15 10:30:46 - audit - WARNING - AUTH: user=admin status=SUCCESS
2024-01-15 10:31:02 - audit - INFO - INVESTIGATION_COMPLETE: id=abc123 user=hive personality=holmes duration=15.34s
```

### Client Audit Log

Location: `/tmp/hive_secure_client.log`

```
2024-01-15 10:30:45 - hive_secure_client - INFO - REQUEST: method=POST endpoint=token status=200
2024-01-15 10:30:46 - hive_secure_client - WARNING - AUTH: status=SUCCESS
```

---

## 🛡️ Security Best Practices

### 1. Production Deployment

```yaml
# Docker Compose with TLS
version: '3'
services:
  terminal-221b:
    build: ./terminal_221b
    environment:
      - T221B_SECRET_KEY=${SECRET_KEY}
      - T221B_TLS_CERT=/certs/cert.pem
      - T221B_TLS_KEY=/certs/key.pem
      - T221B_RATE_LIMIT=1000
    volumes:
      - ./certs:/certs:ro
    ports:
      - "22181:22181"
  
  hive:
    build: ./beeai-hive-999
    environment:
      - T221B_BASE_URL=https://terminal-221b:22181
      - T221B_VERIFY_SSL=true
      - T221B_CERT_PATH=/certs/ca.crt
```

### 2. Key Rotation

```python
# Rotate JWT secret
# 1. Update environment variable
# 2. Restart server
# 3. Clients will re-authenticate automatically

# Rotate user passwords periodically
# Use: auth_manager.users["username"].hashed_password = pwd_context.hash("newpass")
```

### 3. Monitoring

```python
# Alert on security events
if "SECURITY:" in log_line:
    send_alert_to_security_team(log_line)

# Monitor failed auth attempts
if "AUTH: status=FAILED" in log_line:
    if count_failures(ip) > 10:
        block_ip(ip)
```

---

## 🔐 OWASP Top 10 Mitigation

| Risk | Mitigation |
|------|------------|
| Broken Access Control | RBAC with explicit permission checks |
| Cryptographic Failures | Argon2 hashing, JWT with HS256, TLS 1.2+ |
| Injection | Pydantic validation, `nh3` sanitization |
| Insecure Design | Rate limiting, account lockout, audit logging |
| Security Misconfiguration | Secure defaults, env var config |
| Vulnerable Components | Dependency scanning with pip-audit |
| Auth Failures | JWT with expiry, refresh tokens, revocation |
| Data Integrity Failures | Request signing (optional) |
| Logging Failures | Comprehensive audit logging |
| SSRF | URL validation, request restrictions |

---

## 📚 References

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [NIST Zero Trust Architecture](https://www.nist.gov/publications/zero-trust-architecture)

---

**🔒 Security is not a feature, it's a process.**

*"The game is afoot, and this time the detectives are secure!"*
