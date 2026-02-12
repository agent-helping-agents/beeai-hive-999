# ☁️ Cloud Deployment Guide

## Overview

This directory contains configurations for deploying beeAI to various cloud platforms.

---

## 🏆 Recommended: Oracle Cloud Infrastructure (OCI)

**Best free tier option!** Oracle Cloud offers a genuinely useful "Always Free" tier.

| Resource | Free Allocation |
|----------|-----------------|
| **Ampere A1 (Arm)** | 4 OCPUs + 24 GB RAM |
| **AMD Micro** | 2 VMs (1 GB RAM each) |
| **Block Storage** | 200 GB |
| **Outbound Data** | 10 TB/month |
| **Duration** | Forever |

### Quick Deploy to OCI
```bash
# Option 1: Using the install script (after creating VM)
ssh ubuntu@<your-oci-ip> "curl -fsSL https://raw.githubusercontent.com/BoozeLee/beeAI/main/deploy/oci/install.sh | bash"

# Option 2: Using Terraform
cd deploy/oci/terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your OCI credentials
terraform init
terraform apply
```

See [deploy/oci/README.md](oci/README.md) for detailed instructions.

---

## 📁 All Deployment Options

| Platform | Best For | Free Tier | File |
|----------|----------|-----------|------|
| **Oracle Cloud** | Best free tier | ✅ Always Free | `deploy/oci/` |
| **Render** | Simple web apps | ✅ Limited | `render.yaml` |
| **Railway** | Modern deployment | ✅ $5 credit | `deploy/railway/` |
| **Tiny-Cloud** | Private cloud | ✅ Limited | `deploy/tiny-cloud/` |
| **Cloudsmith** | Package hosting | ✅ 10 GB | `deploy/cloudsmith/` |
| **Docker** | Containerized | Self-hosted | `deploy/docker/` |
| **Kubernetes** | Large scale | Self-hosted | `deploy/k8s/` |

---

## 🔐 Pre-Deployment Checklist

### Security
- [ ] Change default passwords (admin/admin123)
- [ ] Set strong `T221B_SECRET_KEY` (32+ random chars)
- [ ] Enable TLS/HTTPS
- [ ] Configure firewall rules
- [ ] Set up log monitoring
- [ ] Enable audit logging

### Configuration
- [ ] Update API URLs (localhost → domain)
- [ ] Configure CORS origins
- [ ] Set rate limiting per environment
- [ ] Configure database connections
- [ ] Set up secrets management

### Monitoring
- [ ] Configure health checks
- [ ] Set up error tracking (Sentry)
- [ ] Enable uptime monitoring
- [ ] Configure log aggregation

---

## 🌐 Environment-Specific Settings

### Development
```yaml
API_URL: http://localhost:22181
RATE_LIMIT: 100/min
DEBUG: true
LOG_LEVEL: debug
```

### Staging
```yaml
API_URL: https://api-staging.beeai.example.com
RATE_LIMIT: 60/min
DEBUG: false
LOG_LEVEL: info
TLS: true
```

### Production
```yaml
API_URL: https://api.beeai.example.com
RATE_LIMIT: 30/min
DEBUG: false
LOG_LEVEL: warning
TLS: true
HSTS: true
CSP: strict
```

---

## 📊 Resource Requirements

### Minimal Deployment (Always Free Tier)
| Component | CPU | RAM | Storage |
|-----------|-----|-----|---------|
| API Server | 1 OCPU | 2 GB | 50 GB |
| **Total** | **1 OCPU** | **2 GB** | **50 GB** |

### Recommended Production
| Component | CPU | RAM | Storage |
|-----------|-----|-----|---------|
| API Server (×2) | 2 OCPU | 4 GB | 100 GB |
| Agent Workers | 2 OCPU | 8 GB | 100 GB |
| **Total** | **4 OCPU** | **12 GB** | **200 GB** |

---

## 🔧 Post-Deployment

### Verification Steps
```bash
# Test API health
curl https://api.example.com/health

# Test authentication
curl -X POST https://api.example.com/token \
  -d "username=admin&password=YOUR_PASSWORD"

# Test protected endpoint
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.example.com/detectives
```

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Oracle Cloud** | $0 (4 OCPU, 24 GB) | ~$0.01/OCPU/hr | Long-term hosting |
| **Render** | $0 (sleeps) | $7+/month | Simple apps |
| **Railway** | $5 credit | Usage-based | Variable workloads |
| **AWS** | $0 (12 months) | Variable | Enterprise |
| **GCP** | $0 ($300 credit) | Variable | ML workloads |
| **Azure** | $0 ($200 credit) | Variable | Microsoft stack |

---

## 📞 Support

- **Issues**: Open a GitHub issue
- **Security**: security@beeai.example.com
- **Docs**: https://docs.beeai.example.com

---

**Ready to deploy to the cloud!** ☁️🐝

**Recommendation**: Start with Oracle Cloud's Always Free tier for the best value!
