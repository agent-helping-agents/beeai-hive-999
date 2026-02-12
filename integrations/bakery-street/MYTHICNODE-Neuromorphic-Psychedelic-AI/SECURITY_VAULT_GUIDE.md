# SECURITY VAULT GUIDE
## How to Safely Store All Your Keys, APIs, and Secrets

**Copyright (c) 2024-2025 Bakery Street Project - ALL RIGHTS RESERVED**

---

## YOUR SECURE STORAGE LOCATIONS

| What | Where | How to Access |
|------|-------|---------------|
| **Filebase Keys** | Replit Secrets | Dashboard > Secrets tab |
| **GitHub Token** | Replit Secrets | `REALGHTOKEN` |
| **Master Keys** | Filebase IPFS | WEB3_KEYVAULT.py |
| **Stripe Keys** | Replit Secrets | `STRIPE_SECRET_KEY` |
| **Perplexity Key** | Replit Secrets | `PERPLEXITY_API_KEY` |

---

## STEP 1: STORE NEW SECRETS IN REPLIT

1. Go to your Replit project
2. Click **"Secrets"** tab (lock icon in left sidebar)
3. Click **"+ New Secret"**
4. Enter key name and value
5. Click Save

**Your current secrets:**
- `FILEBASE_ACCESS_KEY` - For IPFS blockchain storage
- `FILEBASE_SECRET_KEY` - For IPFS blockchain storage  
- `REALGHTOKEN` - GitHub access (rotate after sessions!)
- `STRIPE_SECRET_KEY` - Payment processing
- `STRIPE_WEBHOOK_SECRET` - Stripe webhooks
- `PERPLEXITY_API_KEY` - AI research
- `SESSION_SECRET` - App sessions
- `DATABASE_URL` - PostgreSQL connection

---

## STEP 2: STORE MASTER KEYS ON BLOCKCHAIN (PERMANENT)

Use WEB3_KEYVAULT to store encryption keys on IPFS forever:

```python
from WEB3_KEYVAULT import FilebaseVault

vault = FilebaseVault()

# Store any secret permanently
receipt = vault.store("your-master-password", b"my-secret-key-data")

# SAVE THESE SOMEWHERE SAFE:
print(f"Vault ID: {receipt.vault_id}")
print(f"IPFS CID: {receipt.ipfs_cid}")
print(f"Gateway: https://ipfs.filebase.io/ipfs/{receipt.ipfs_cid}")
```

**To retrieve later:**
```python
vault = FilebaseVault()
secret = vault.retrieve("your-master-password", "VAULT-abc123...")
```

---

## STEP 3: ORGANIZE YOUR KEYS

### Create a Password-Protected Key Registry

Store this info in a password manager (1Password, Bitwarden, etc.):

```
BAKERY STREET PROJECT - KEY REGISTRY
=====================================

REPLIT PROJECT: [your-replit-url]

FILEBASE (IPFS Storage):
- Access Key: [stored in Replit Secrets]
- Secret Key: [stored in Replit Secrets]
- Bucket: bakery-vault

MASTER VAULTS (on IPFS):
- Main Vault: VAULT-[id]  |  CID: Qm...  |  Password: [your password]
- Backup Vault: VAULT-[id]  |  CID: Qm...  |  Password: [your password]

GITHUB:
- Token: REALGHTOKEN  |  Rotate: [date]
- Org: Bakery-street-project

STRIPE:
- Secret Key: [in Replit Secrets]
- Webhook Secret: [in Replit Secrets]
- Dashboard: https://dashboard.stripe.com

PERPLEXITY AI:
- API Key: [in Replit Secrets]
- Dashboard: https://www.perplexity.ai/settings/api
```

---

## SECURITY RULES

### DO:
- Store API keys in Replit Secrets (encrypted)
- Store master keys on IPFS via WEB3_KEYVAULT (permanent)
- Use strong unique passwords for vault encryption
- Rotate GitHub token after each session
- Keep vault IDs in a password manager

### DON'T:
- Put keys directly in code
- Commit secrets to GitHub
- Share vault passwords
- Use the same password everywhere
- Forget to save vault IDs (you'll lose access!)

---

## QUICK REFERENCE COMMANDS

### Check your Replit secrets:
```bash
# In Replit shell
echo $FILEBASE_ACCESS_KEY | head -c 10  # Shows first 10 chars
```

### Store a new master key:
```python
from WEB3_KEYVAULT import FilebaseVault
vault = FilebaseVault()
receipt = vault.store("password123", b"my-new-secret")
print(receipt.vault_id)  # SAVE THIS!
```

### List all your vaults:
```python
from WEB3_KEYVAULT import FilebaseVault
vault = FilebaseVault()
for v in vault.list_vaults():
    print(v)
```

### Retrieve a secret:
```python
from WEB3_KEYVAULT import FilebaseVault
vault = FilebaseVault()
secret = vault.retrieve("password123", "VAULT-abc123...")
print(secret)
```

---

## WHAT'S STORED WHERE

```
+------------------+     +------------------+     +------------------+
|  REPLIT SECRETS  |     |  FILEBASE IPFS   |     |  PASSWORD MGR    |
|  (encrypted)     |     |  (blockchain)    |     |  (your device)   |
+------------------+     +------------------+     +------------------+
| - API Keys       |     | - Master Keys    |     | - Vault IDs      |
| - Filebase creds |     | - Certificates   |     | - Passwords      |
| - GitHub token   |     | - Encrypted data |     | - Recovery info  |
| - Stripe keys    |     | - Permanent!     |     | - Backup codes   |
+------------------+     +------------------+     +------------------+
         |                       |                       |
         v                       v                       v
    Easy access            Never deleted            Your backup
    from code              (IPFS forever)           (offline safe)
```

---

## EMERGENCY RECOVERY

If you lose access to Replit:
1. Your IPFS data is still on blockchain (access via CID)
2. Log into filebase.com with your account
3. Your secrets are in your password manager

If you forget vault password:
- **Game over** - that's the point of encryption
- Always keep passwords in a password manager!

---

## COST SUMMARY

| Service | Cost | Limit |
|---------|------|-------|
| Replit Secrets | FREE | Unlimited |
| Filebase IPFS | FREE | 5 GB |
| IPFS Storage | FREE | Uses Filebase |
| Password Manager | FREE-$3/mo | Unlimited |

**Total: $0/month** for secure key storage!

---

*Remember: "100% EASY FOR YOU - 1000000% IMPOSSIBLE FOR THEM"*

*Bakery Street Project - Your secrets, your rules.*
