# 🔐 Security Specifications

**Repository:** Energetic Lexicon Database
**Classification:** 🔒 PRIVATE - PROPRIETARY
**Security Level:** HIGH
**Last Updated:** December 26, 2025

---

## 🎯 Security Objectives

1. **Confidentiality** - Protect proprietary research and repository metadata
2. **Integrity** - Ensure data accuracy and prevent unauthorized modifications
3. **Availability** - Maintain system uptime with encrypted backups
4. **Auditability** - Track all access and modifications
5. **Compliance** - Maintain AGPL license separation for AgenticSeek integration

---

## 🏗️ Multi-Layer Security Architecture

### Layer 1: Data at Rest Encryption

**Technology:** GPG (GNU Privacy Guard) with AES256

**Implementation:**
```bash
# Encryption
gpg --symmetric \
    --cipher-algo AES256 \
    --batch --yes \
    --passphrase-file ~/.primax_vault_password \
    --output lexicon.db.gpg \
    lexicon.db

# Decryption
gpg --decrypt \
    --batch --yes \
    --passphrase-file ~/.primax_vault_password \
    --output lexicon.db \
    lexicon.db.gpg
```

**Protected Files:**
- SQLite database files (`*.db`)
- ChromaDB vector embeddings (`chroma/`)
- PDF documents (`pdfs/`)
- Audit logs (`logs/*.audit`)
- Backup archives (`encrypted_backups/*.gpg`)

**Encryption Key:**
- Location: `~/.primax_vault_password`
- Permissions: `600` (read/write owner only)
- Backup: Stored in secure offline location
- Rotation: Manual, on security incident or quarterly

### Layer 2: Data in Transit Encryption

**Technology:** TLS 1.3

**Configuration:**
```python
# FastAPI with TLS
uvicorn main:app \
    --host 0.0.0.0 \
    --port 8443 \
    --ssl-keyfile /path/to/private.key \
    --ssl-certfile /path/to/certificate.crt \
    --ssl-version TLSv1_3
```

**Requirements:**
- Minimum TLS 1.3 (no TLS 1.2 or lower)
- Strong cipher suites only
- Certificate validation required
- No self-signed certificates in production

### Layer 3: Authentication & Authorization

**Technology:** JWT (JSON Web Tokens) with role-based access control

**Token Structure:**
```json
{
  "sub": "user_id",
  "role": "admin|developer|readonly",
  "exp": 1735251600,
  "iat": 1735248000,
  "scopes": ["read:repos", "write:concepts", "admin:system"]
}
```

**Roles & Permissions:**

| Role | Read Repos | Write Repos | Read Concepts | Write Concepts | Admin |
|------|-----------|-------------|---------------|----------------|-------|
| **readonly** | ✅ | ❌ | ✅ | ❌ | ❌ |
| **developer** | ✅ | ✅ | ✅ | ✅ | ❌ |
| **admin** | ✅ | ✅ | ✅ | ✅ | ✅ |

**Token Lifecycle:**
- **Access token expiration:** 1 hour
- **Refresh token expiration:** 7 days
- **Refresh token storage:** Encrypted at rest
- **Token rotation:** Required every 30 days
- **Revocation:** Immediate via blacklist

### Layer 4: Access Control

**Network Security:**
- IP whitelisting for production API
- Rate limiting: 60 requests/minute per IP
- DDoS protection via reverse proxy
- No public internet access without VPN

**File Permissions:**
```bash
# Database files
chmod 600 data/lexicon.db
chmod 700 data/

# Encryption keys
chmod 600 ~/.primax_vault_password

# Configuration
chmod 600 .env

# Scripts
chmod 700 scripts/*.py

# Logs
chmod 600 logs/*.log
chmod 700 logs/
```

**GitHub Repository:**
- Private repository only
- Branch protection on `main`:
  - Require pull request reviews (minimum 1)
  - Dismiss stale reviews on new commits
  - Require status checks to pass
  - Require signed commits (GPG)
- No force pushes allowed
- No deletions allowed

### Layer 5: Audit Logging

**Technology:** Append-only encrypted logs

**Logged Events:**
- All database mutations (INSERT, UPDATE, DELETE)
- Authentication attempts (success/failure)
- API calls with timestamp, user, endpoint, parameters
- File access (read/write/delete)
- Configuration changes
- Encryption/decryption operations
- Backup creation/restoration

**Log Format:**
```json
{
  "timestamp": "2025-12-26T18:30:00Z",
  "event_type": "database_write",
  "user_id": "user_123",
  "ip_address": "192.168.1.100",
  "action": "INSERT",
  "table": "repos",
  "record_id": "repo_456",
  "success": true,
  "error": null
}
```

**Log Storage:**
- Primary: `logs/audit.log` (encrypted with GPG)
- Backup: Daily encrypted archives in `encrypted_backups/`
- Retention: 1 year minimum
- Immutable: Append-only, no modifications allowed

---

## 🛡️ Threat Model

### Protected Against

✅ **Unauthorized Repository Access**
- Private GitHub repository
- IP whitelisting
- JWT authentication required

✅ **Data Exfiltration**
- All data encrypted at rest (GPG AES256)
- TLS 1.3 in transit
- No plaintext exports without authorization

✅ **Man-in-the-Middle Attacks**
- TLS 1.3 with strong ciphers
- Certificate pinning
- No HTTP allowed (HTTPS only)

✅ **Replay Attacks**
- JWT expiration (1 hour)
- Nonce validation
- Timestamp checks

✅ **SQL Injection**
- Parameterized queries (SQLAlchemy ORM)
- Input validation
- No raw SQL execution

✅ **API Abuse**
- Rate limiting (60 req/min)
- API key rotation (30 days)
- Request size limits

✅ **Insider Threats**
- Audit logging (all actions tracked)
- Role-based permissions
- Least privilege principle

### Assumptions & Limitations

**Assumptions:**
- Attacker does NOT have access to:
  - GPG private key
  - Vault password file (`~/.primax_vault_password`)
  - GitHub authentication tokens
  - Server SSH keys
- Trusted execution environment (Termux on controlled device)
- Physical device security maintained
- No malware on host system

**Limitations:**
- ⚠️ GPG password in plaintext file (acceptable for local dev, not production)
- ⚠️ No hardware security module (HSM) for key storage
- ⚠️ Limited to symmetric encryption (no PKI infrastructure)
- ⚠️ Single point of failure (one encryption key)

---

## 🚨 Incident Response

### Security Incident Procedure

**1. Detection**
- Monitor audit logs for suspicious activity
- Alert on failed authentication attempts (>5/hour)
- Alert on unusual API usage patterns
- Regular security reviews

**2. Containment**
- Immediately revoke compromised tokens
- Disable affected user accounts
- Block suspicious IP addresses
- Isolate affected systems

**3. Investigation**
- Review audit logs for attack timeline
- Identify compromised data
- Determine attack vector
- Assess scope of damage

**4. Recovery**
- Restore from encrypted backups if needed
- Rotate all encryption keys
- Reset all API tokens
- Apply security patches

**5. Lessons Learned**
- Document incident in `INCIDENTS.md`
- Update security procedures
- Implement additional controls
- Conduct security training

### Emergency Contacts

**Security Lead:** [To be assigned]
**Backup Contact:** [To be assigned]
**24/7 Hotline:** [To be configured]

---

## 🔍 Security Checklist

### Daily
- [ ] Review audit logs for anomalies
- [ ] Verify backup completion
- [ ] Check system resource usage
- [ ] Monitor API error rates

### Weekly
- [ ] Review access logs
- [ ] Check for failed authentication attempts
- [ ] Verify encryption key integrity
- [ ] Test backup restoration

### Monthly
- [ ] Rotate API keys
- [ ] Review user permissions
- [ ] Update dependencies (security patches)
- [ ] Conduct vulnerability scan

### Quarterly
- [ ] Full security audit
- [ ] Penetration testing (if applicable)
- [ ] Rotate encryption keys
- [ ] Review and update security policies

---

## 🔒 Data Classification

### CRITICAL (Highest Protection)
- Encryption keys (`~/.primax_vault_password`)
- API tokens (`GITHUB_TOKEN`, `JWT_SECRET_KEY`)
- User passwords (hashed)
- Private repository metadata

**Protection:**
- GPG AES256 encryption at rest
- Never logged in plaintext
- Never transmitted unencrypted
- Access restricted to admin role only

### CONFIDENTIAL (High Protection)
- Repository descriptions and READMEs
- PDF content
- Concept definitions
- Research findings

**Protection:**
- GPG encryption at rest
- TLS 1.3 in transit
- Access logged in audit trail
- Developer role or higher required

### INTERNAL (Medium Protection)
- Repository names and URLs
- Concept terms (not definitions)
- Automation run status
- Database schema

**Protection:**
- GPG encryption at rest
- TLS 1.3 in transit
- Access logged
- Readonly role or higher required

### PUBLIC (Low Protection)
- Repository classification (public/private flag only)
- Technology stack lists
- Documentation structure

**Protection:**
- TLS 1.3 in transit
- No encryption at rest required
- Access logged (optional)
- No authentication required (if exposed)

---

## 🧪 Security Testing

### Automated Tests

**Encryption Tests:**
```python
def test_encryption_decryption():
    """Verify GPG encryption/decryption works correctly"""
    original = "test data"
    encrypted = encrypt_data(original)
    decrypted = decrypt_data(encrypted)
    assert decrypted == original
    assert encrypted != original  # Actually encrypted
```

**Authentication Tests:**
```python
def test_jwt_expiration():
    """Verify JWT tokens expire correctly"""
    token = create_token(user_id="test", expiration=1)
    time.sleep(2)
    assert not verify_token(token)  # Should be expired
```

**Authorization Tests:**
```python
def test_role_permissions():
    """Verify role-based access control"""
    readonly_user = create_user(role="readonly")
    assert can_read_repos(readonly_user) == True
    assert can_write_repos(readonly_user) == False
```

### Manual Security Review

**Code Review Checklist:**
- [ ] No hardcoded secrets or credentials
- [ ] All inputs validated and sanitized
- [ ] Parameterized queries (no string concatenation)
- [ ] Authentication required for all sensitive endpoints
- [ ] Authorization checks for all operations
- [ ] Sensitive data encrypted before storage
- [ ] Error messages don't leak information
- [ ] Logging doesn't expose sensitive data

**Infrastructure Review:**
- [ ] File permissions correctly set (600/700)
- [ ] No world-readable files
- [ ] `.gitignore` protects sensitive files
- [ ] Environment variables used (not hardcoded)
- [ ] Dependencies up to date (no known vulnerabilities)

---

## 📚 Security Resources

### Internal Documentation
- `ENERGETIC_LEXICON_RESEARCH.md` - Threat model section
- `README.md` - Security classification
- `.env.example` - Secure configuration template

### External References
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GPG Best Practices](https://riseup.net/en/security/message-security/openpgp/best-practices)
- [JWT Security Best Practices](https://tools.ietf.org/html/rfc8725)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

---

## 🔄 Security Updates

**Latest Update:** December 26, 2025
- Initial security specification
- Multi-layer architecture defined
- Threat model documented
- Incident response procedure established

**Next Review:** March 26, 2026 (Quarterly)

---

**Security Classification:** 🔒 PRIVATE - PROPRIETARY
**Distribution:** Authorized Personnel Only
**Questions:** Contact security lead

© 2025 Bakery Street Project - All Rights Reserved
