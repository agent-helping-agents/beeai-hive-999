# 🔒 Energetic Lexicon Database

**CLASSIFICATION: PRIVATE - PROPRIETARY**
**Security Level: HIGH**
**Organization:** Bakery Street Project / Baker Street Laboratory
**Repository Type:** Encrypted Knowledge Base

---

## ⚠️ SECURITY NOTICE

This repository contains proprietary research and encrypted database infrastructure for the Bakery Street Project ecosystem.

**Access Control:**
- Private repository - authorized personnel only
- All database files encrypted with GPG AES256
- Multi-layer security architecture
- Audit logging enabled
- No public forks or distributions permitted

**Protected Data:**
- Repository metadata for 50+ Bakery Street projects
- PDF semantic embeddings
- Concept lexicon and knowledge graph
- Automation patterns and CI/CD configurations
- Research findings and architectural decisions

---

## 📋 Repository Contents

### Research Documentation
- `ENERGETIC_LEXICON_RESEARCH.md` - Complete AI Research Geometry™ analysis
  - System architecture design
  - Technology stack recommendations
  - 6-phase implementation roadmap
  - Security specifications
  - AGPL license compliance strategy

### Database System (Coming Soon)
- SQLite primary database with migration path to PostgreSQL
- ChromaDB vector store for semantic search
- GPG encryption wrapper for data at rest
- FastAPI REST/GraphQL API layer
- CLI tool for PRIMAX/AgenticSeek integration

### Automation Infrastructure
- GitHub Actions CI/CD pipelines
- Auto-sync webhooks for repository metadata
- Daily encrypted backups
- Audit logging system

---

## 🏗️ System Architecture

```yaml
Energetic Lexicon Database:
  Storage Layer:
    - Primary: SQLite → PostgreSQL (scalable)
    - Vector: ChromaDB (persistent embeddings)
    - Encryption: GPG AES256 at rest

  API Layer:
    - REST: FastAPI with auto-docs
    - GraphQL: Complex relationship queries
    - CLI: Typer-based for agent integration

  Security:
    - Authentication: JWT tokens
    - Encryption: GPG AES256 (rest) + TLS 1.3 (transit)
    - Audit: All mutations logged
    - Access Control: Role-based permissions
```

---

## 🔐 Encryption Protocol

**Layer 1: Data at Rest**
- All database files encrypted with GPG AES256
- Encryption key: `~/.primax_vault_password`
- Automatic re-encryption on updates

**Layer 2: Data in Transit**
- TLS 1.3 for all API communications
- JWT tokens with 1-hour expiration
- Encrypted refresh tokens

**Layer 3: Access Control**
- Role-based permissions (admin, developer, readonly)
- API key rotation every 30 days
- IP whitelisting for production

**Layer 4: Audit Trail**
- Immutable append-only logs
- Timestamp, user, action tracking
- Encrypted log storage

---

## 📊 Implementation Status

### Phase 1: Foundation ⏳
- [x] Research & architecture design ✅
- [x] Private repository creation ✅
- [x] Security infrastructure ✅
- [ ] Database schema design
- [ ] SQLite setup + basic CRUD
- [ ] GPG encryption wrapper

### Phase 2: Ingestion
- [ ] Fix baker-search PATH issues
- [ ] GitHub API scraper (50 repos)
- [ ] PDF parser implementation
- [ ] Initial dataset population

### Phase 3: Semantic Layer
- [ ] ChromaDB integration
- [ ] PDF embeddings generation
- [ ] Semantic search API
- [ ] Query testing

### Phase 4: Automation
- [ ] GitHub Actions CI/CD
- [ ] Auto-update webhooks
- [ ] Daily encrypted backups
- [ ] Audit logging

### Phase 5: Integration
- [ ] PRIMAX API client
- [ ] AgenticSeek plugin (AGPL)
- [ ] CLI tool
- [ ] Documentation

### Phase 6: Refinement
- [ ] Performance optimization
- [ ] Schema migrations
- [ ] Commercial license tracker
- [ ] Public/private separation

---

## 🔗 Integration Points

**PRIMAX Runtime**
- API endpoint: `/lexicon/query`
- Dynamic tool/concept discovery

**AgenticSeek (AGPL-3.0)**
- Plugin interface (JSON/REST boundary)
- Core lexicon remains proprietary

**baker-search**
- Primary data source for GitHub repos
- Research Geometry mode classification

---

## 📜 License Compliance

**Core Database: Proprietary**
- © 2025 Bakery Street Project
- Commercial use: Authorized projects only
- Redistribution: Prohibited without license

**AgenticSeek Plugin: AGPL-3.0**
- Separate plugin in `integrations/` folder
- Clear API boundary
- Source available if deployed as network service

---

## 🛡️ Threat Model

**Protected Against:**
- ✅ Unauthorized repository access
- ✅ Data exfiltration (encrypted at rest)
- ✅ Man-in-the-middle attacks (TLS)
- ✅ Replay attacks (JWT expiration)
- ✅ SQL injection (parameterized queries)

**Assumptions:**
- Attacker does NOT have access to:
  - GPG private key
  - Vault password file
  - GitHub authentication tokens
- Trusted deployment environment

---

## 📖 Documentation

- `ENERGETIC_LEXICON_RESEARCH.md` - Complete research findings
- `ARCHITECTURE.md` - System design (coming soon)
- `API_REFERENCE.md` - API documentation (coming soon)
- `SECURITY.md` - Security specifications (coming soon)
- `LICENSING_COMPLIANCE.md` - License strategy (coming soon)

---

## 🔬 Research Framework

This project was designed using **AI Research Geometry™** by Baker Street Laboratory - a framework that treats research as geometric/coordinate space rather than simple Q&A.

**Key Principles:**
- Lexicon as coordinates (not definitions)
- Geometric positioning (4-quadrant classification)
- Tension preservation (not premature closure)
- Iterative reframing loops

---

## 🚨 DO NOT REDISTRIBUTE

This is proprietary infrastructure for the Bakery Street Project ecosystem.

**Unauthorized use includes:**
- Public forks or clones
- Sharing encryption keys or credentials
- Redistributing research documentation
- Commercial use without authorization

---

**Repository Created:** December 26, 2025
**Last Updated:** December 26, 2025
**Maintained By:** Baker Street Laboratory
**Security Classification:** 🔒 PRIVATE - PROPRIETARY

© 2025 Bakery Street Project - All Rights Reserved
