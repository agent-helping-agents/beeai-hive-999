# 🚀 beeAI Quick Start Guide

Get up and running with beeAI in under 5 minutes!

---

## ⚡ One-Line Setup

```bash
cd /home/boozelee/beeAI && ./scripts/start-local.sh
```

---

## 📋 Manual Setup

### 1. Install Dependencies

```bash
cd /home/boozelee/beeAI
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
export T221B_SECRET_KEY="your-super-secret-key-min-32-chars-long"
export ENV="development"
```

### 3. Start the Server

```bash
python -m src.api.secure_server_fixed
```

---

## 🧪 Test the API

### Health Check
```bash
curl http://localhost:22181/health
```

### Login (Get Token)
```bash
curl -X POST http://localhost:22181/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### List Detectives
```bash
curl http://localhost:22181/detectives \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Start Investigation
```bash
curl -X POST http://localhost:22181/investigate \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"query": "Analyze this transaction", "personality": "holmes"}'
```

---

## 🐳 Docker Deployment

```bash
cd deploy/docker
docker-compose up -d
```

---

## ☁️ Cloud Deployment

### Oracle Cloud (Recommended - Best Free Tier!)
```bash
# Using Terraform (recommended)
cd deploy/oci/terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your credentials
terraform init
terraform apply

# Or manual installation on existing OCI VM
ssh ubuntu@<your-oci-ip> "curl -fsSL https://raw.githubusercontent.com/BoozeLee/beeAI/main/deploy/oci/install.sh | bash"
```
**Free Tier**: 4 OCPUs + 24 GB RAM + 200 GB storage - Forever!

### Render
Connect GitHub repo at [render.com](https://render.com)

### Railway
```bash
railway login
railway init
railway up
```

### Tiny-Cloud
```bash
./deploy/tiny-cloud/deploy.sh --env production
```

---

## 🔐 Production Checklist

Before deploying to production:

- [ ] Change default passwords (NEVER use admin/admin123)
- [ ] Set strong `T221B_SECRET_KEY` (32+ random chars)
- [ ] Enable TLS/HTTPS
- [ ] Configure firewall rules
- [ ] Set up monitoring (Sentry, UptimeRobot)
- [ ] Enable audit logging

See [security/SECURITY_CHECKLIST.md](security/SECURITY_CHECKLIST.md) for full checklist.

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
lsof -ti:22181 | xargs kill -9
```

### Permission Denied
```bash
chmod +x scripts/*.sh deploy/*/*.sh
```

### Import Errors
```bash
pip install -r requirements.txt --upgrade
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Project overview |
| [MERGE_SUMMARY.md](MERGE_SUMMARY.md) | What was merged |
| [docs/CONTRIBUTORS.md](docs/CONTRIBUTORS.md) | Credits |
| [docs/GITHUB_GIFTS.md](docs/GITHUB_GIFTS.md) | Free tier inventory |
| [deploy/README.md](deploy/README.md) | Deployment guide |
| [security/SECURITY_CHECKLIST.md](security/SECURITY_CHECKLIST.md) | Security audit |

---

**You're ready to go!** 🐝☁️

Need help? Open an issue on GitHub.
