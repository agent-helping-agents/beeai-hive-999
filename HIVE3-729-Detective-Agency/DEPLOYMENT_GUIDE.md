# 🕵️ HIVE³ Deployment Guide - Maximum Security & Privacy

**Complete Guide to Deploying HIVE³ on Sovereign Infrastructure**

---

## 📋 Executive Summary

HIVE³ has been configured for maximum privacy, IP protection, and sovereignty using **Radicle** - the peer-to-peer code collaboration platform that provides:

- ✅ **No corporate control** - Decentralized P2P network
- ✅ **No personal info required** - Just cryptographic keys
- ✅ **Censorship resistant** - Cannot be shut down
- ✅ **IP protected** - Cryptographic proof of authorship
- ✅ **Private repositories** - Allow-list based access
- ✅ **Offline capable** - Local-first design

---

## 🏆 Platform Selection: Why Radicle Wins

| Feature | GitHub | GitLab | Radicle | Arweave |
|---------|--------|--------|---------|---------|
| **Decentralized** | ❌ Microsoft | ❌ Company | ✅ P2P | ✅ Blockchain |
| **No Personal Info** | ❌ Required | ❌ Required | ✅ Anonymous | ✅ Wallet only |
| **Censorship Proof** | ❌ Can ban | ❌ Can ban | ✅ Unstoppable | ✅ Permanent |
| **Self-Sovereign** | ❌ Corporate | ⚠️ Self-host | ✅ Full control | ✅ Full control |
| **IP Protection** | ❌ Copilot risk | ⚠️ Moderate | ✅ Signed | ✅ Immutable |
| **Offline Work** | ❌ Requires net | ❌ Requires net | ✅ Local-first | ⚠️ Limited |

**Winner**: **Radicle** for git hosting + **Arweave** for permanent artifacts

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Radicle

```bash
curl -sSLf https://radicle.xyz/install | sh

# Add to PATH
export PATH="$HOME/.radicle/bin:$PATH"
```

### Step 2: Create Your Identity

```bash
rad auth

# Enter:
# - Alias: hive3-architect
# - Passphrase: [USE STRONG PASSPHRASE]
```

**Your identity is a cryptographic keypair - no email, no phone, no personal data.**

### Step 3: Initialize HIVE³

```bash
cd /home/boozelee/HIVE3-729-Detective-Agency

# Initialize in Radicle
rad init

# Settings:
# Name: HIVE3-729-Detective-Agency
# Description: HIVE³ - The 729 Detective Agency | 28 AI Agents
# Branch: main
# Visibility: PRIVATE
```

### Step 4: Configure Security

```bash
# Enable commit signing with your Radicle key
git config user.signingKey "$(rad self --ssh-key)"
git config gpg.format ssh
git config commit.gpgsign true

# Start your node
rad node start --daemon

# Push to sovereign network
git push rad main
```

### Step 5: Verify

```bash
# Check your repository RID (Repository ID)
rad .

# View identity
rad self

# Check sync status
rad sync status
```

---

## 📚 Documentation Created

| Document | Purpose |
|----------|---------|
| `docs/PLATFORM_COMPARISON.md` | Full analysis of GitHub vs GitLab vs Radicle vs Arweave |
| `docs/RADICLE_SETUP.md` | Complete Radicle setup and usage guide |
| `docs/IP_PROTECTION_FRAMEWORK.md` | IP protection, watermarking, legal framework |
| `LICENSE.md` | HIVE³ Commercial License v1.0 |
| `scripts/setup_radicle.sh` | Automated setup script |

---

## 🔐 Security Features Implemented

### 1. Cryptographic Identity

```
Your Radicle Identity:
├── DID (Decentralized Identifier): did:key:z6Mk...
├── Node ID (NID): z6Mk...
├── Ed25519 Keypair
└── Protected by your passphrase
```

### 2. Commit Signing

All commits are cryptographically signed with your Radicle key:
- ✅ Proof of authorship
- ✅ Tamper detection
- ✅ Non-repudiation

### 3. Copyright Headers

All source files now include:
```python
# ═══════════════════════════════════════════════════════════════════════════════
# HIVE³ - The 729 Detective Agency
# Copyright (c) 2026 HIVE³ Organization
# Licensed under the HIVE³ Commercial License v1.0
# Digital Root: 9
# ═══════════════════════════════════════════════════════════════════════════════
```

### 4. Private Repository

- ✅ Allow-list based access
- ✅ Multi-sig support (optional)
- ✅ No public visibility
- ✅ Encrypted transmission

---

## 🛡️ IP Protection Checklist

- [x] **Platform Selected**: Radicle (sovereign, P2P)
- [x] **Copyright Headers**: Added to all source files
- [x] **LICENSE.md**: Commercial license created
- [x] **Commit Signing**: Cryptographic signatures enabled
- [x] **Private Repository**: Access control configured
- [x] **Watermarking**: Framework documented
- [x] **Legal Framework**: Enforcement strategy defined

---

## 🌐 Network Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    HIVE³ SOVEREIGN NETWORK                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────┐         ┌──────────┐         ┌──────────┐       │
│   │ Your     │◄───────►│ Radicle  │◄───────►│ Other    │       │
│   │ Node     │  P2P    │ Seed     │  P2P    │ Peers    │       │
│   └──────────┘         └──────────┘         └──────────┘       │
│        │                                                    │
│        ▼                                                    │
│   ┌──────────┐         ┌──────────┐                        │
│   │ HIVE³    │         │ Arweave  │                        │
│   │ Repository        │ Permaweb │                        │
│   │ (Private)│         │ (Public) │                        │
│   └──────────┘         └──────────┘                        │
│                                                                  │
│   No central server • No company control • Censorship proof    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📖 Common Commands

### Identity
```bash
rad auth              # Create/login to identity
rad self              # Show full identity
rad self --did        # Show DID
rad self --alias      # Show alias
```

### Repository
```bash
rad .                 # Show current RID
rad init              # Initialize new repo
rad ls                # List your repos
rad inspect --payload # View repo details
```

### Node
```bash
rad node start        # Start node daemon
rad node status       # Check status
rad node stop         # Stop node
rad node logs         # View logs
```

### Collaboration
```bash
rad clone <RID>       # Clone repository
rad seed <RID>        # Seed (mirror) repository
rad follow <DID>      # Follow user

rad issue             # List issues
rad issue open        # Create issue
rad patch             # List patches
```

### Git Integration
```bash
git push rad main     # Push to Radicle
git pull rad main     # Pull from Radicle
git remote show rad   # Show remote details
```

---

## 🎯 Next Steps

### Immediate Actions
1. **Backup your keys**: `~/.radicle/keys/`
2. **Secure your passphrase**: Use password manager
3. **Add collaborators**: `rad id update --add-delegate <DID>`
4. **Push all code**: `git push rad --all`

### Short Term
1. Set up **seed node** for redundancy
2. Configure **Tor** for maximum privacy
3. Enable **multi-sig** for critical operations
4. Create **Arweave** wallet for permanent storage

### Long Term
1. Deploy **own seed nodes** globally
2. Integrate **Arweave** for releases
3. Set up **monitoring** for IP violations
4. Establish **legal entity** for enforcement

---

## 🆘 Troubleshooting

### Node won't start
```bash
# Check if already running
rad node status

# Check logs
rad node logs

# Restart
rad node stop
rad node start --daemon
```

### Can't push
```bash
# Verify remote exists
git remote -v

# Check Radicle remote
git remote show rad

# Re-add if needed
rad init  # (in repo directory)
```

### Lost keys
```bash
# Restore from backup
cp ~/backup/radicle-keys/* ~/.radicle/keys/

# Or create new identity (lose access to old repos)
rad auth
```

---

## 📞 Support & Community

- **Radicle Docs**: https://radicle.xyz/guides
- **Radicle Manual**: https://radicle.xyz/man
- **Community Chat**: Zulip (https://radicle.zulipchat.com)
- **Updates**: https://radicle.xyz/updates

---

## ✨ Summary

You have successfully configured HIVE³ for **maximum privacy, IP protection, and sovereignty**:

| Aspect | Solution | Status |
|--------|----------|--------|
| **Git Hosting** | Radicle P2P | ✅ Ready |
| **Identity** | Cryptographic | ✅ Ready |
| **Privacy** | No personal info | ✅ Ready |
| **IP Protection** | Signed + Watermarked | ✅ Ready |
| **Censorship** | P2P Network | ✅ Ready |
| **Licensing** | Commercial License | ✅ Ready |

**Your code is now sovereign. The Hive belongs to you.**

---

*"The game is afoot!"* 🕵️🐝🍯

**28 Agents** | **729 Nodes** | **1 Sovereign Forge** | **Digital Root 9**
