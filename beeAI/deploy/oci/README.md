# ☁️ Oracle Cloud Infrastructure (OCI) Deployment

## Overview

Oracle Cloud Infrastructure offers a generous **Always Free** tier that's perfect for hosting beeAI.

## 🎁 Always Free Tier Benefits

| Resource | Allocation | Notes |
|----------|------------|-------|
| **Ampere A1 (Arm)** | 4 OCPUs + 24 GB RAM | Can split into 1-4 VMs |
| **AMD Micro** | 2 VMs (1/8 OCPU + 1 GB each) | Alternative option |
| **Block Storage** | 200 GB | For boot volumes |
| **Outbound Data** | 10 TB/month | Generous transfer |
| **Duration** | Forever | Truly always-free |

## Recommended Configuration for beeAI

```
VM.Standard.A1.Flex
├── OCPUs: 2
├── RAM: 8 GB
├── Boot Volume: 100 GB
└── OS: Ubuntu 22.04 LTS
```

This leaves you 2 OCPUs + 16 GB RAM for other projects!

---

## 🚀 Quick Deploy

### 1. Sign Up
1. Go to https://www.oracle.com/cloud/free/
2. Sign up for an account (credit card required for verification, but won't be charged for Always Free)
3. Verify your email and complete registration

### 2. Create Compute Instance

```bash
# Using OCI CLI (after setup)
oci compute instance launch \
    --availability-domain $(oci iam availability-domain list --query 'data[0].name' --raw-output) \
    --compartment-id $COMPARTMENT_ID \
    --shape 'VM.Standard.A1.Flex' \
    --shape-config '{"ocpus": 2, "memoryInGBs": 8}' \
    --os-name 'Ubuntu' \
    --os-version '22.04' \
    --ssh-authorized-keys-file ~/.ssh/id_rsa.pub \
    --display-name 'beeai-server'
```

Or use the web console:
1. Navigation → Compute → Instances
2. Click "Create Instance"
3. Select "VM.Standard.A1.Flex" shape
4. Configure: 2 OCPUs, 8 GB RAM
5. Add SSH key
6. Create

### 3. Configure Security List

Add ingress rules:
- Port 22 (SSH): 0.0.0.0/0
- Port 80 (HTTP): 0.0.0.0/0
- Port 443 (HTTPS): 0.0.0.0/0
- Port 22181 (beeAI API): 0.0.0.0/0

### 4. Deploy beeAI

```bash
# SSH into your instance
ssh ubuntu@<your-instance-ip>

# Run the install script
curl -fsSL https://raw.githubusercontent.com/BoozeLee/beeAI/main/deploy/oci/install.sh | bash
```

Or manually:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Clone beeAI
git clone https://github.com/BoozeLee/beeAI.git
cd beeAI

# Start with Docker Compose
docker-compose -f deploy/docker/docker-compose.yml up -d
```

---

## 🔐 Security Setup

### Generate Strong Secret Key
```bash
export T221B_SECRET_KEY=$(openssl rand -hex 32)
echo "T221B_SECRET_KEY=$T221B_SECRET_KEY" >> ~/.bashrc
```

### Set Up TLS with Let's Encrypt
```bash
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com
```

---

## 📊 Monitoring (Free Options)

| Service | Free Tier | Setup |
|---------|-----------|-------|
| **OCI Monitoring** | Always Free basic metrics | Built-in |
| **UptimeRobot** | 50 monitors | External |
| **Sentry** | 5k errors/month | See docs |

---

## 💰 Cost Estimate

| Scenario | Monthly Cost |
|----------|--------------|
| **Always Free only** | **$0** |
| Exceed 4 OCPUs | ~$0.01/hour per OCPU |
| Exceed 200 GB storage | ~$0.0255/GB/month |

**Tip**: Set up budget alerts at $1 to avoid surprises!

---

## 🆘 Troubleshooting

### "Out of Capacity" Error
- Try a different availability domain
- Try at a different time (capacity fluctuates)
- Consider upgrading to Pay-as-You-Go (no charge for Always Free resources)

### Instance Reclaimed (Idle)
Oracle may reclaim idle instances. Keep your server active:
```bash
# Add to crontab (minimal CPU usage)
*/5 * * * * curl -s http://localhost:22181/health > /dev/null
```

### Connection Issues
- Verify security list rules
- Check network ACLs
- Ensure VCN has internet gateway

---

## 📚 Resources

- [OCI Always Free FAQ](https://www.oracle.com/cloud/free/faq.html)
- [OCI Compute Documentation](https://docs.oracle.com/en-us/iaas/Content/Compute/Concepts/computeoverview.htm)
- [OCI Free Tier Details](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm)

---

**Oracle Cloud is the best free tier option for beeAI!** ☁️🐝
