# 🔒 Security Checklist

## Pre-Production Security Audit

Use this checklist before deploying to production.

---

## ✅ Authentication & Authorization

### Password Security
- [ ] **Default passwords changed** - Never use admin/admin123 or hive/hive123 in production
- [ ] **Strong password policy** - Min 12 chars, mixed case, numbers, symbols
- [ ] **Argon2 configured** - Memory ≥ 64MB, iterations ≥ 3, parallelism ≥ 1
- [ ] **Password rotation** - Users can change passwords
- [ ] **Brute force protection** - Account lockout after 5 failed attempts

### JWT Security
- [ ] **Strong secret key** - 32+ bytes random string in environment variable
- [ ] **Short access token TTL** - 15-30 minutes maximum
- [ ] **Refresh token rotation** - New refresh token on each use
- [ ] **Token blacklisting** - Logout invalidates tokens
- [ ] **Algorithm explicitly set** - Use HS256, not "none"

### RBAC
- [ ] **Principle of least privilege** - Users have minimum necessary permissions
- [ ] **Role separation** - Admin, user, service accounts distinct
- [ ] **Permission auditing** - Regular review of role assignments

---

## 🌐 Network Security

### TLS/HTTPS
- [ ] **TLS 1.2+ only** - Disable older versions
- [ ] **Strong cipher suites** - Use modern configuration
- [ ] **HSTS enabled** - Strict-Transport-Security header
- [ ] **Certificate valid** - Not expired, from trusted CA
- [ ] **Auto-renewal** - Let's Encrypt or similar

### Rate Limiting
- [ ] **Global rate limit** - 100 req/min default
- [ ] **Per-endpoint limits** - Stricter for auth endpoints
- [ ] **Per-user limits** - Account-based throttling
- [ ] **IP-based blocking** - Temporary bans for abuse

### CORS
- [ ] **Explicit origins** - No wildcard (*) in production
- [ ] **Allowed methods** - Only necessary HTTP methods
- [ ] **Allowed headers** - Minimal required set
- [ ] **Credentials handling** - Secure cookie settings

---

## 🛡️ Input Validation & Sanitization

### XSS Prevention
- [ ] **nh3 library used** - HTML sanitization on all outputs
- [ ] **Content-Type headers** - Application/json for APIs
- [ ] **CSP headers** - Content-Security-Policy configured

### Injection Prevention
- [ ] **Parameterized queries** - No string concatenation in SQL
- [ ] **Input validation** - Pydantic models for all inputs
- [ ] **File upload limits** - Size and type restrictions
- [ ] **Path traversal protection** - Sanitize file paths

---

## 📝 Logging & Monitoring

### Audit Logging
- [ ] **Authentication events** - Login, logout, failures
- [ ] **Authorization events** - Permission changes
- [ ] **Data access** - Sensitive data reads/writes
- [ ] **Configuration changes** - Settings modifications

### Security Monitoring
- [ ] **Failed login alerts** - Notify on suspicious activity
- [ ] **Rate limit alerts** - Detect potential attacks
- [ ] **Error tracking** - Sentry or similar configured
- [ ] **Log retention** - 90+ days for security logs

---

## 🔧 Configuration Security

### Secrets Management
- [ ] **Environment variables** - No secrets in code
- [ ] **Secret rotation** - Regular key rotation
- [ ] **Encryption at rest** - Database encryption
- [ ] **Backup encryption** - Encrypted backups

### Dependencies
- [ ] **Vulnerability scanning** - Regular dependency audits
- [ ] **Up-to-date packages** - Security patches applied
- [ ] **Minimal dependencies** - Remove unused packages
- [ ] **License compliance** - All licenses acceptable

---

## 🚨 Incident Response

### Preparation
- [ ] **Response plan** - Documented procedures
- [ ] **Contact list** - Security team contacts
- [ ] **Backup strategy** - Regular tested backups
- [ ] **Rollback plan** - Quick revert capability

### Detection
- [ ] **Anomaly detection** - Unusual traffic patterns
- [ ] **Error monitoring** - Spikes in 4xx/5xx errors
- [ ] **Performance monitoring** - Resource usage spikes

---

## 📋 Pre-Production Sign-Off

### Security Review
- [ ] Code review completed
- [ ] Security tests passing
- [ ] Penetration testing done
- [ ] Dependencies scanned
- [ ] Configuration reviewed

### Documentation
- [ ] Security policies documented
- [ ] Incident response documented
- [ ] User security guidelines
- [ ] API security documentation

---

## 🔄 Ongoing Security

### Regular Tasks
- [ ] **Weekly**: Review access logs
- [ ] **Monthly**: Dependency updates
- [ ] **Quarterly**: Security audit
- [ ] **Annually**: Penetration test

---

## 🎯 Production Readiness Score

| Category | Weight | Score |
|----------|--------|-------|
| Authentication | 25% | ___/100 |
| Network Security | 20% | ___/100 |
| Input Validation | 15% | ___/100 |
| Logging/Monitoring | 15% | ___/100 |
| Configuration | 15% | ___/100 |
| Incident Response | 10% | ___/100 |
| **Total** | 100% | ___/100 |

**Minimum to deploy: 80%**

---

**Security is not a destination, it's a journey.** 🔐🐝
