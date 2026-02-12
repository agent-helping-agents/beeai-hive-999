# 🐝 beeAI - Unified AI Ecosystem

**The Complete Merge of Hive 999, Terminal 221b, Hypercube AI, Superposition Engine, and Solana Integration**

> A secure, cloud-ready, multi-agent AI system with blockchain integration.

---

## 📋 Project Overview

This repository represents the unified merge of multiple AI and blockchain projects into a single, cohesive ecosystem. It combines:

- 🐝 **Hive 999** - Multi-agent blockchain intelligence (28+ agents, 729 nodes)
- 🕵️ **Terminal 221b** - Sherlock Holmes-inspired Solana AI detective
- 🧊 **Hypercube AI** - 9×9×9 dimensional computational model
- 🌌 **Superposition Engine** - Quantum-inspired optimization algorithms
- ⛓️ **Solana Integration** - Baker Street Solana Gateway

---

## 🏗️ Architecture

```
beeAI/
├── src/
│   ├── hive/              # Hive 999 core (28+ agents)
│   ├── terminal221b/      # Terminal 221b detective system
│   ├── hypercube/         # Hypercube computational model
│   ├── superposition/     # Quantum-inspired engine
│   ├── solana/            # Solana blockchain integration
│   ├── agents/            # Shared agent framework
│   ├── api/               # Secure API server
│   └── tui/               # Terminal UI
├── deploy/                # Cloud deployment configs
│   ├── cloud/             # Generic cloud setup
│   ├── tiny-cloud/        # Tiny-cloud deployment
│   ├── cloudsmith/        # Cloudsmith packages
│   ├── docker/            # Containerization
│   └── k8s/               # Kubernetes manifests
├── security/              # Security policies & audits
├── docs/                  # Documentation
├── config/                # Configuration files
└── tests/                 # Test suites
```

---

## 🔒 Security-First Design

All localhost services have been hardened for cloud deployment:

- ✅ JWT Authentication with Argon2
- ✅ Role-Based Access Control (RBAC)
- ✅ Rate Limiting (100 req/min default)
- ✅ TLS/HTTPS Support
- ✅ Input Sanitization (nh3 XSS prevention)
- ✅ Audit Logging
- ✅ Secrets Management (Fernet encryption)

---

## 🚀 Quick Start

### Local Development
```bash
# Clone and setup
git clone <repo>
cd beeAI

# Install dependencies
pip install -r requirements.txt
npm install

# Start services
./scripts/start-local.sh
```

### Cloud Deployment

**🏆 Recommended: Oracle Cloud (Always Free - 4 OCPU, 24 GB RAM)**
```bash
# Terraform (Infrastructure as Code)
cd deploy/oci/terraform && terraform init && terraform apply

# Or manual installation
ssh ubuntu@<your-oci-ip> "curl -fsSL https://raw.githubusercontent.com/BoozeLee/beeAI/main/deploy/oci/install.sh | bash"
```

**Other Options:**
```bash
# Render (Simple, but sleeps when idle)
# Connect GitHub repo at render.com

# Railway (Modern workflow)
railway login && railway init && railway up

# Docker (Self-hosted)
docker-compose -f deploy/docker/docker-compose.yml up -d
```

See [DEPLOYMENT_COMPARISON.md](DEPLOYMENT_COMPARISON.md) for full comparison.

---

## 📚 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md)
- [Security Policies](security/POLICIES.md)
- [Deployment Guide](deploy/README.md)
- [Contributors & Credits](docs/CONTRIBUTORS.md)
- [GitHub Gifts Inventory](docs/GITHUB_GIFTS.md)

---

## 🌟 Key Features

| Feature | Status | Description |
|---------|--------|-------------|
| 28+ AI Agents | ✅ | Queen, Workers, Drones, Foragers, Detectives |
| 9×9×9 Matrix | ✅ | 729-node computational hypercube |
| Solana Integration | ✅ | Baker Street Gateway with micro-payments |
| Secure API | ✅ | JWT, RBAC, Rate limiting, TLS |
| Cloud Ready | ✅ | OCI (Always Free), Render, Railway, Docker, K8s |
| TUI Interface | ✅ | Full terminal UI with ANSI art |

---

## 🤝 Contributing

See [CONTRIBUTORS.md](docs/CONTRIBUTORS.md) for the full list of contributors and how to join.

---

## 📜 License

Multi-license project. See individual component directories for specific licenses.

---

**Built with 💎 hands by the Bakery Street Laboratory Team**

*"The game is afoot, and the bees are swarming in the cloud!"*
