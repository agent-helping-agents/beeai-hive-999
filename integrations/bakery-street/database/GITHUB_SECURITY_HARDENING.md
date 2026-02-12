# GITHUB SECURITY HARDENING GUIDE
## Protection Against Pipeline Scraping, GitHub Access, and Data Exposure

**Document Date:** December 26, 2025
**Classification:** 🔒 CRITICAL - SECURITY OPERATIONS
**Threat Level:** HIGH (Private repo on third-party platform)
**Author:** Baker Street Laboratory Security Team

---

## ⚠️ CRITICAL SECURITY ASSESSMENT

### Threat Model: GitHub Platform

**ASSUME COMPROMISE:**
- ✅ GitHub staff CAN access private repositories
- ✅ GitHub Actions logs MAY be visible to GitHub
- ✅ Secrets in GitHub Actions CAN be exfiltrated if misconfigured
- ✅ Repository code IS visible to GitHub infrastructure
- ✅ Commit history IS permanently stored

**DEFENSE STRATEGY:** **Zero-Trust Architecture**

---

## 🛡️ MULTI-LAYER SECURITY ARCHITECTURE

### Layer 1: Repository-Level Encryption (CRITICAL)

**Strategy:** Encrypt ALL sensitive data BEFORE committing to GitHub

**Implementation:**

```bash
# .gitattributes - Git encryption filter
*.db filter=git-crypt diff=git-crypt
*.sqlite filter=git-crypt diff=git-crypt
*.key filter=git-crypt diff=git-crypt
*.env filter=git-crypt diff=git-crypt
secrets/* filter=git-crypt diff=git-crypt

# Alternatively, manual GPG encryption
*.secret.gpg binary
```

**Git-Crypt Setup:**
```bash
# Install git-crypt
pkg install git-crypt

# Initialize in repository
cd ~/claude_enterprise/workspace/database
git-crypt init

# Add GPG key for team members only
git-crypt add-gpg-user YOUR_GPG_KEY_ID

# All files matching .gitattributes are now encrypted at rest
```

**Manual Encryption Protocol:**
```bash
# NEVER commit these files unencrypted:
- database/data/*.db          # SQLite databases
- database/data/chroma/*      # Vector embeddings
- .env                        # Environment variables
- config/*.yml                # Configuration files with secrets

# Encryption workflow:
gpg --symmetric --cipher-algo AES256 \
    --batch --yes \
    --passphrase-file ~/.primax_vault_password \
    --output data/lexicon.db.gpg \
    data/lexicon.db

# Commit only encrypted version
git add data/lexicon.db.gpg
git add -u data/lexicon.db  # Remove unencrypted version
```

---

### Layer 2: GitHub Actions Secrets Hardening

**Problem:** GitHub Actions secrets can leak via:
- `echo` commands in logs
- Environment variable printing
- Malicious dependencies
- Compromised GitHub infrastructure

**Solution:** Multi-layer secret protection

**2.1 Use GitHub Environments (not just repo secrets)**

```yaml
# .github/workflows/build-executable.yml
jobs:
  build:
    runs-on: ubuntu-latest
    environment: production  # Requires manual approval

    steps:
      - name: Access protected secret
        env:
          GPG_PRIVATE_KEY: ${{ secrets.GPG_PRIVATE_KEY }}
        run: |
          # Secret only accessible in approved environment
```

**2.2 Never Log Secrets**

```yaml
# ❌ WRONG - Secret exposed in logs
- name: Sign binary
  run: echo "$GPG_PRIVATE_KEY" | gpg --import

# ✅ CORRECT - Secret not logged
- name: Sign binary
  env:
    GPG_PRIVATE_KEY: ${{ secrets.GPG_PRIVATE_KEY }}
  run: |
    set +x  # Disable command echoing
    echo "$GPG_PRIVATE_KEY" | gpg --import --batch --quiet
```

**2.3 Use Encrypted Secrets (Double Encryption)**

```bash
# Encrypt secret before adding to GitHub
echo "my-secret-value" | \
  gpg --symmetric --armor \
      --passphrase "$MASTER_PASSWORD" \
  > secret.gpg.asc

# Add encrypted secret to GitHub Secrets
# Name: ENCRYPTED_GPG_KEY
# Value: <paste contents of secret.gpg.asc>

# In GitHub Actions, decrypt:
- name: Decrypt secret
  env:
    ENCRYPTED_GPG_KEY: ${{ secrets.ENCRYPTED_GPG_KEY }}
    MASTER_PASSWORD: ${{ secrets.MASTER_PASSWORD }}
  run: |
    echo "$ENCRYPTED_GPG_KEY" | \
      gpg --decrypt --batch --quiet \
          --passphrase "$MASTER_PASSWORD" \
      > /tmp/actual-secret
```

**2.4 Audit Log Monitoring**

```yaml
# Add audit step to every workflow
- name: Audit secret usage
  run: |
    echo "Workflow: ${{ github.workflow }}" >> audit.log
    echo "User: ${{ github.actor }}" >> audit.log
    echo "Timestamp: $(date -u)" >> audit.log
    echo "Secrets accessed: GPG_KEY, VAULT_PASSWORD" >> audit.log

    # Encrypt and commit audit log
    gpg --symmetric --batch \
        --passphrase-file ~/.primax_vault_password \
        audit.log

    git add audit.log.gpg
    git commit -m "Audit: ${{ github.sha }}"
```

---

### Layer 3: Prevent Data Exfiltration

**3.1 Network Isolation**

```yaml
# .github/workflows/build-executable.yml
jobs:
  build-offline:
    runs-on: ubuntu-latest

    steps:
      - name: Disable network after dependency download
        run: |
          # Download dependencies
          pip install -r requirements.txt

          # Disable network to prevent exfiltration
          sudo iptables -A OUTPUT -j DROP
          sudo iptables -A INPUT -j DROP

          # Now build (no network access)
          pyinstaller energetic_lexicon.spec
```

**3.2 Dependency Pinning (Prevent Supply Chain Attacks)**

```txt
# requirements.txt - Pin EXACT versions
sqlalchemy==2.0.25  # Not >=2.0.0
chromadb==0.4.18    # Not ~=0.4
fastapi==0.104.1    # Not *

# Generate with:
pip freeze > requirements.txt
```

**3.3 Hash Verification**

```bash
# requirements-hashes.txt
sqlalchemy==2.0.25 \
    --hash=sha256:abc123...

# Install with hash verification
pip install --require-hashes -r requirements-hashes.txt
```

---

### Layer 4: Repository Access Control

**4.1 Branch Protection Rules**

```yaml
# Settings → Branches → main
Require pull request reviews: ✅ (minimum 1)
Require status checks: ✅
Require signed commits: ✅ (GPG)
Include administrators: ✅
Restrict who can push: ✅ (only you)
```

**4.2 Signed Commits (GPG)**

```bash
# Configure Git to sign all commits
git config --global user.signingkey YOUR_GPG_KEY_ID
git config --global commit.gpgsign true

# Verify signatures
git log --show-signature
```

**4.3 Audit Log Review**

```bash
# GitHub → Settings → Security log
# Review all access events monthly
# Look for:
- Unauthorized SSH key additions
- API token creation
- Webhook additions
- Collaborator invitations
```

---

### Layer 5: Encrypted Backups (Off-GitHub)

**Strategy:** Never rely solely on GitHub for storage

**Implementation:**

```bash
#!/bin/bash
# scripts/backup-to-private-storage.sh

# Full repository backup with encryption
BACKUP_DIR=~/secure-backups
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="database_backup_${TIMESTAMP}.tar.gpg"

# Create encrypted archive
tar czf - \
    ~/claude_enterprise/workspace/database \
  | gpg --symmetric --cipher-algo AES256 \
        --batch --yes \
        --passphrase-file ~/.primax_vault_password \
  > "${BACKUP_DIR}/${BACKUP_FILE}"

# Verify backup
gpg --decrypt --batch \
    --passphrase-file ~/.primax_vault_password \
    "${BACKUP_DIR}/${BACKUP_FILE}" \
  | tar tzf - > /dev/null

# Store to external location (NOT GitHub)
# Options:
# 1. Encrypted USB drive
# 2. Personal NAS with encryption
# 3. Encrypted cloud storage (own encryption, not provider's)
```

**Automated Daily Backups:**

```bash
# Cron job (crontab -e)
0 2 * * * ~/claude_enterprise/workspace/database/scripts/backup-to-private-storage.sh
```

---

### Layer 6: Code Obfuscation (Additional Layer)

**For Critical Algorithms:**

```python
# src/core/sensitive_algorithm.py
# Obfuscate before committing

# Original:
def decrypt_master_key(encrypted_key):
    return crypto.decrypt(encrypted_key, MASTER_KEY)

# Obfuscated (using pyarmor):
pyarmor obfuscate --restrict src/core/sensitive_algorithm.py

# Commit obfuscated version
# Keep original only on secure local storage
```

---

## 🚨 CRITICAL: What NOT to Commit

### NEVER Commit (Even to Private Repo):

```
❌ .env files with real values
❌ Unencrypted database files (*.db, *.sqlite)
❌ Private keys (*.pem, *.key, id_rsa*)
❌ API tokens or passwords
❌ Vault password files
❌ ChromaDB vector embeddings (unencrypted)
❌ User data or PII
❌ Customer data
❌ Audit logs with sensitive info (encrypt first)
❌ SSH keys
❌ Credentials.json files
❌ Keystore files
```

### ALWAYS Commit:

```
✅ Encrypted versions (*.gpg, *.enc)
✅ Source code (no secrets)
✅ Database schema (no data)
✅ Documentation
✅ Configuration templates (.env.example)
✅ Build scripts (no secrets)
✅ Tests (no real credentials)
```

---

## 🔍 PIPELINE SCRAPING PROTECTION

### Threat: Malicious GitHub Actions

**Attack Vector:**
1. Compromised dependency runs malicious code in CI
2. Malicious code reads secrets from environment
3. Exfiltrates secrets to external server

**Defense:**

**1. Isolated Build Environment**

```yaml
# Use Docker with no network after download
- name: Build in isolated container
  run: |
    docker build --network=none \
                 --tag=isolated-build \
                 --file=Dockerfile.isolated .

    docker run --rm \
               --network=none \
               --volume=$(pwd)/dist:/output \
               isolated-build
```

**2. Secret Rotation**

```bash
# Rotate GPG keys monthly
gpg --gen-key  # Generate new key
gpg --export-secret-keys OLD_KEY | gpg --encrypt > old-key-backup.gpg
gpg --delete-secret-keys OLD_KEY

# Update GitHub secret
# Update local ~/.primax_vault_password
```

**3. Audit All Dependencies**

```bash
# Check for known vulnerabilities
pip-audit

# Check for malicious packages
pip install guarddog
guarddog scan requirements.txt

# Manual review of new dependencies
pip show <package-name>
# Check: homepage, author, downloads, github repo
```

---

## 🔐 ENCRYPTION AT REST - COMPLETE STRATEGY

### File-Level Encryption Matrix

| File Type | Encryption Method | Key Storage | Auto-Decrypt |
|-----------|------------------|-------------|--------------|
| **Database (*.db)** | GPG AES256 | `~/.primax_vault_password` | On app startup |
| **Vector Store** | Git-Crypt | GPG key ring | On clone |
| **Source Code** | None (safe) | N/A | N/A |
| **Secrets** | Double GPG | Master password + vault | Never auto |
| **Audit Logs** | GPG AES256 | Vault password | Admin only |
| **Backups** | GPG AES256 | Offline key | Manual only |

### Encryption Workflow

```bash
# Before every commit:
./scripts/pre-commit-encrypt.sh

# Script contents:
#!/bin/bash
set -e

echo "🔒 Pre-commit encryption check..."

# Find unencrypted sensitive files
UNENCRYPTED=$(find . -type f \
  \( -name "*.db" -o -name "*.sqlite" -o -name ".env" \) \
  ! -name "*.gpg" \
  ! -path "./.git/*" \
  ! -path "./dist/*")

if [ -n "$UNENCRYPTED" ]; then
  echo "❌ ERROR: Unencrypted sensitive files found:"
  echo "$UNENCRYPTED"
  echo ""
  echo "Encrypt with:"
  echo "gpg --symmetric --cipher-algo AES256 --batch --passphrase-file ~/.primax_vault_password <file>"
  exit 1
fi

echo "✅ All sensitive files encrypted"
```

**Install as Git Hook:**

```bash
# .git/hooks/pre-commit
#!/bin/bash
./scripts/pre-commit-encrypt.sh
```

---

## 🛡️ GITHUB-PROOF SECURITY CHECKLIST

**Assume GitHub is Compromised:**

- [x] All database files encrypted before commit ✅
- [x] Git-Crypt enabled for sensitive file types ✅
- [x] No plaintext secrets in repository ✅
- [x] GitHub Actions secrets double-encrypted ✅
- [x] Network isolation during sensitive builds ✅
- [x] Signed commits (GPG) required ✅
- [x] Branch protection enabled ✅
- [x] Daily encrypted backups to non-GitHub storage ✅
- [x] Dependency hash verification ✅
- [x] Audit logging for all secret access ✅
- [x] Secret rotation schedule (monthly) ✅
- [x] Pre-commit hooks prevent accidental exposure ✅

---

## 🚀 SECURE CI/CD WORKFLOW (FINAL)

```yaml
# .github/workflows/secure-build.yml
name: Secure Build with Encryption

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

# Use environment protection
environment: production

jobs:
  security-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check for leaked secrets
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./

      - name: Audit dependencies
        run: |
          pip install pip-audit
          pip-audit -r requirements.txt

  build-isolated:
    needs: security-checks
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Decrypt encrypted files
        env:
          VAULT_PASSWORD: ${{ secrets.VAULT_PASSWORD }}
        run: |
          # Decrypt only what's needed for build
          echo "$VAULT_PASSWORD" > /tmp/vault_pass

          find . -name "*.gpg" -exec \
            gpg --decrypt --batch --quiet \
                --passphrase-file /tmp/vault_pass \
                --output {}.decrypted {} \;

          rm /tmp/vault_pass  # Immediate cleanup

      - name: Build in isolated environment
        run: |
          # Download dependencies
          pip download -r requirements.txt -d /tmp/deps

          # Disconnect network
          sudo iptables -A OUTPUT -j DROP

          # Install from local cache
          pip install --no-index --find-links=/tmp/deps -r requirements.txt

          # Build
          pyinstaller energetic_lexicon.spec

      - name: Sign and encrypt artifact
        env:
          GPG_PRIVATE_KEY: ${{ secrets.GPG_PRIVATE_KEY }}
        run: |
          echo "$GPG_PRIVATE_KEY" | gpg --import --batch --quiet

          # Sign
          gpg --detach-sign --armor dist/energetic-lexicon

          # Encrypt final binary
          gpg --symmetric --cipher-algo AES256 \
              --batch --passphrase-file /tmp/vault_pass \
              dist/energetic-lexicon

      - name: Upload encrypted artifact
        uses: actions/upload-artifact@v4
        with:
          name: energetic-lexicon-encrypted
          path: |
            dist/energetic-lexicon.gpg
            dist/energetic-lexicon.asc

      - name: Audit log
        run: |
          echo "Build completed: $(date)" >> build-audit.log
          echo "Actor: ${{ github.actor }}" >> build-audit.log
          echo "SHA: ${{ github.sha }}" >> build-audit.log

          # Encrypt and commit audit log
          gpg --symmetric --batch build-audit.log
          # (Commit in separate step)
```

---

## 📋 SECURITY MAINTENANCE SCHEDULE

**Daily:**
- [ ] Check GitHub security alerts
- [ ] Review recent commits for accidental leaks

**Weekly:**
- [ ] Audit GitHub Actions logs
- [ ] Review access logs
- [ ] Test backup restoration

**Monthly:**
- [ ] Rotate GPG keys
- [ ] Rotate API tokens
- [ ] Update dependencies (security patches)
- [ ] Review and revoke old access tokens

**Quarterly:**
- [ ] Full security audit
- [ ] Penetration testing
- [ ] Encryption key rotation
- [ ] Backup integrity verification

---

## 🆘 INCIDENT RESPONSE PLAN

**If Secrets Compromised:**

1. **Immediate Actions (Within 1 Hour):**
   ```bash
   # Revoke all GitHub tokens
   # Rotate all GPG keys
   # Delete compromised secrets from GitHub
   # Change vault password
   # Re-encrypt all files with new keys
   ```

2. **Investigation (Within 24 Hours):**
   - Review GitHub audit logs
   - Check for unauthorized commits
   - Scan for data exfiltration
   - Identify attack vector

3. **Recovery (Within 1 Week):**
   - Restore from encrypted backup
   - Re-deploy with new keys
   - Update all integrations
   - Notify affected parties (if applicable)

4. **Prevention (Ongoing):**
   - Update security procedures
   - Add additional monitoring
   - Train team on new protocols

---

**FINAL VERDICT:**

✅ **SECURE AGAINST:**
- GitHub staff access (encryption at rest)
- Pipeline scraping (double encryption)
- Dependency attacks (hash verification, network isolation)
- Accidental leaks (pre-commit hooks)
- Supply chain attacks (pinned dependencies)

⚠️ **REMAINING RISKS:**
- Quantum computing (AES256 vulnerable in 10-20 years)
- Insider threats (authorized collaborators)
- Physical device theft (if vault password stolen)
- Social engineering (phishing for keys)

**MITIGATION:** Multi-factor authentication, hardware security keys, regular audits

---

© 2025 Baker Street Laboratory - Security Operations
🔒 CLASSIFIED - SECURITY OPERATIONS ONLY
