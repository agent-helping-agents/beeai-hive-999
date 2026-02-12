# 🕵️ HIVE³ Radicle Setup Guide

**Maximum Privacy, IP Protection & Sovereign Code Collaboration**

---

## Prerequisites

- Linux, macOS, or BSD
- Git 2.34.0 or later
- OpenSSH 9.1+ with ssh-agent
- Terminal access

---

## Step 1: Install Radicle

```bash
# Install Radicle using official installer
curl -sSLf https://radicle.xyz/install | sh

# Or install to custom location
curl -sSLf https://radicle.xyz/install | sh -s -- --prefix=/usr/local

# Verify installation
rad --version
```

---

## Step 2: Create Cryptographic Identity

```bash
# Initialize your Radicle identity
rad auth

# You will be prompted for:
# - Alias (public name, can be anything)
# - Passphrase (secure your private key)
```

**Example session:**
```
$ rad auth
Initializing your radicle 👾 identity

✓ Enter your alias: hive3-architect
✓ Enter a passphrase: ********
✓ Creating your Ed25519 keypair...
✓ Adding your radicle key to ssh-agent...
✓ Your Radicle DID is did:key:z6Mkhp7VUnuufpvuQ3PdysShAjL86VDRUpPpkesqiysDBGs9
```

### Understanding Your Identity

```bash
# View full identity
rad self

# Get your DID (Decentralized Identifier)
rad self --did

# Get your Node ID
rad node status --only nid

# View SSH key
rad self --ssh-key
```

**Key Points:**
- **DID**: Your sovereign identity - share freely
- **Passphrase**: Protects your private key
- **No email required**: Complete privacy
- **No phone number**: No surveillance

---

## Step 3: Initialize HIVE³ Repository

### Option A: New Repository

```bash
# Navigate to project
cd /home/boozelee/HIVE3-729-Detective-Agency

# Initialize in Radicle
rad init

# Configuration:
# ✓ Name: HIVE3-729-Detective-Agency
# ✓ Description: "HIVE³ - The 729 Detective Agency | 28 AI Agents | Solana Blockchain | Digital Root 9"
# ✓ Default branch: main
# ✓ Visibility: PRIVATE (for IP protection)
```

### Option B: Existing Repository

```bash
cd /home/boozelee/HIVE3-729-Detective-Agency

# Initialize existing Git repo in Radicle
rad init

# Push to Radicle remote
git push rad main
```

---

## Step 4: Configure Private Repository

```bash
# Set up allow list for private repo
rad id update --add-delegate <TRUSTED_DID_1>
rad id update --add-delegate <TRUSTED_DID_2>

# Set threshold for multi-sig (optional)
# This means 2 out of 3 delegates must approve changes
rad id update --threshold 2
```

---

## Step 5: Enable Cryptographic Signing

```bash
# Configure Git to use Radicle key for signing
git config user.signingKey "$(rad self --ssh-key)"
git config gpg.format ssh
git config gpg.ssh.program ssh-keygen
git config gpg.ssh.allowedSignersFile .gitsigners
git config commit.gpgsign true

# Create signers file
echo "$(rad self --ssh-key) $(rad self --alias)" > .gitsigners
git add .gitsigners
git commit -m "Add cryptographic signers"
```

---

## Step 6: Start Your Node

```bash
# Start Radicle node daemon
rad node start --daemon

# Check node status
rad node status

# View connected peers
rad node status --peers
```

---

## Step 7: Repository Operations

### Publishing Changes

```bash
# Make changes
git add .
git commit -m "Implement feature X"

# Push to Radicle (works offline!)
git push rad main

# Changes sync automatically when online
```

### Viewing Repository Info

```bash
# Get Repository ID (RID)
rad .

# View project details
rad inspect --payload

# Check sync status
rad sync status
```

### Working with Issues (COBs)

```bash
# List issues
rad issue

# Create issue
rad issue open

# Show issue
rad issue show <ISSUE_ID>

# Comment on issue
rad issue comment <ISSUE_ID> --message "Working on this"
```

### Working with Patches

```bash
# Create patch
git checkout -b feature-branch
# ... make changes ...
git commit -m "Add feature"
git push rad HEAD:refs/patches

# List patches
rad patch

# Show patch
rad patch show <PATCH_ID>
```

---

## Step 8: Tor Integration (Maximum Privacy)

For ultimate privacy, route Radicle through Tor:

```bash
# Install Tor
sudo apt-get install tor  # Debian/Ubuntu
brew install tor          # macOS

# Configure Radicle for Tor
rad node config --tor

# Or use mixed mode (Tor + clearnet)
rad node config --tor-mixed
```

---

## Step 9: Backup Strategy

### Local Backup

```bash
# Backup Radicle keys
cp -r ~/.radicle/keys ~/backup/radicle-keys-$(date +%Y%m%d)

# Backup repositories
cp -r ~/.radicle/storage ~/backup/radicle-storage-$(date +%Y%m%d)

# Encrypt backup
gpg --symmetric --cipher-algo AES256 ~/backup/radicle-backup-$(date +%Y%m%d).tar.gz
```

### Seed Node Strategy

Run your own seed node for redundancy:

```bash
# Seed important repositories
rad seed rad:YOUR_REPO_ID

# Run public seed node (optional)
# See: https://radicle.xyz/guides/seeder
```

---

## Security Checklist

- [ ] Strong passphrase on private key
- [ ] Commit signing enabled
- [ ] Private repository configured
- [ ] Allow list curated
- [ ] Seed nodes diversified
- [ ] Local backups encrypted
- [ ] Tor enabled (optional)
- [ ] Multi-sig for critical repos (optional)

---

## Troubleshooting

### Node Won't Start
```bash
# Check logs
rad node logs

# Reset node (keeps identity)
rad node stop
rm -rf ~/.radicle/node/*
rad node start
```

### Can't Push
```bash
# Check remote
git remote -v

# Verify rad remote exists
git remote show rad

# Re-initialize if needed
rad init
```

### Identity Issues
```bash
# Check identity
rad self

# Re-auth if needed (keeps repos)
rad auth
```

---

## Quick Reference

```bash
# Identity
rad auth              # Create/login
rad self              # Show identity
rad self --did        # Get DID

# Repositories
rad init              # Initialize repo
rad .                 # Show current RID
rad ls                # List my repos

# Node
rad node start        # Start node
rad node status       # Check status
rad node stop         # Stop node

# Collaboration
rad clone <RID>       # Clone repo
rad seed <RID>        # Seed repo
rad follow <DID>      # Follow user

# Issues & Patches
rad issue             # List issues
rad issue open        # Create issue
rad patch             # List patches
```

---

*"The sovereign forge belongs to those who control their keys."*
