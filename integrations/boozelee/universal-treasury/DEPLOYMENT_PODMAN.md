# Universal Treasury CLI - Podman Deployment Guide

## 🐳 Podman-Based Deployment

This guide provides comprehensive instructions for deploying the Universal Treasury CLI using Podman (Docker alternative) for production environments.

## 🎯 Features

- **Rootless containers**: No need for sudo/root privileges
- **Systemd integration**: Automatic startup and recovery
- **Multi-platform support**: Works on Linux, macOS, Windows
- **Secure by default**: Non-root user, read-only filesystems
- **Production-ready**: Health checks, logging, monitoring

## 📋 Prerequisites

### 1. Install Podman

#### **Linux (Debian/Ubuntu)**:
```bash
sudo apt-get update
sudo apt-get install -y podman podman-compose
```

#### **Linux (Fedora/RHEL/CentOS)**:
```bash
sudo dnf install -y podman podman-compose
```

#### **macOS**:
```bash
brew install podman podman-compose
```

#### **Windows**:
```powershell
choco install podman
```

### 2. Verify Installation
```bash
podman --version
podman-compose --version
```

## 🚀 Quick Start

### 1. Build and Run with Podman

```bash
# Navigate to project directory
cd ~/workspace/universal-treasury

# Build the application
export PATH=$PATH:~/local/go/bin
go build -o treasury main.go

# Build the Podman container
podman build -t universal-treasury-cli:1.0.0 -f Containerfile .

# Run the container
podman run -it --rm \
    -v ~/.treasury:/home/appuser/.treasury \
    universal-treasury-cli:1.0.0 --help
```

### 2. Use the Deployment Script

```bash
# Run the comprehensive deployment script
./scripts/deploy-podman.sh
```

This script will:
- Build the Go application
- Create a Podman container
- Set up a pod with proper networking
- Configure volume mounts for persistent data
- Start the service with automatic restart

## 🎯 Production Deployment

### Option A: Manual Deployment

```bash
# Create a pod
podman pod create --name treasury-pod -p 8080:8080

# Run the container
podman run -d \
    --pod treasury-pod \
    --name treasury-cli \
    -v ~/.treasury:/home/appuser/.treasury \
    -v ./config:/app/config \
    --restart always \
    universal-treasury-cli:1.0.0

# Check status
podman pod ps
podman ps --pod
```

### Option B: Systemd Service (Recommended)

```bash
# Run as root
sudo ./scripts/create-systemd-service.sh

# Service management
sudo systemctl start treasury-cli
sudo systemctl enable treasury-cli
sudo systemctl status treasury-cli

# View logs
journalctl -u treasury-cli -f
```

## 📦 Podman Compose Deployment

```bash
# Install podman-compose if not available
pip install podman-compose

# Start all services
podman-compose -f podman-compose.yml up -d

# Stop all services
podman-compose -f podman-compose.yml down

# View logs
podman-compose -f podman-compose.yml logs -f
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
# Wise API Configuration
WISE_CLIENT_ID=your_client_id_from_wise
WISE_REDIRECT_URI=https://yourdomain.com/callback
WISE_API_KEY=your_api_key_after_authentication

# Database (if using external DB)
DB_HOST=localhost
DB_PORT=5432
DB_USER=treasury
DB_PASSWORD=securepassword
DB_NAME=treasury
```

### Configuration File

The CLI uses `~/.treasury.yaml` for configuration:

```yaml
# Wise configuration
wise:
  api_key: "your_api_key"
  client_id: "your_client_id"
  redirect_uri: "https://yourdomain.com/callback"

# Database configuration
database:
  type: "sqlite"  # or "postgres"
  path: "~/.treasury/treasury.db"

# Logging configuration
logging:
  level: "info"
  file: "~/.treasury/treasury.log"
```

## 🛡 Security Best Practices

### 1. Rootless Containers
```bash
# Podman runs rootless by default
podman info | grep rootless
```

### 2. Read-Only Filesystem
```bash
podman run --read-only -v ~/.treasury:/home/appuser/.treasury:rw ...
```

### 3. Resource Limits
```bash
podman run --memory=512m --cpus=1 ...
```

### 4. Network Isolation
```bash
podman network create treasury-net
podman run --network treasury-net ...
```

## 🔄 Updating the Application

```bash
# Pull latest code
cd ~/workspace/universal-treasury
git pull origin main

# Rebuild and redeploy
export PATH=$PATH:~/local/go/bin
go build -o treasury main.go
podman build -t universal-treasury-cli:1.0.0 -f Containerfile .

# Restart the service
podman stop treasury-cli
podman rm treasury-cli
podman run -d --pod treasury-pod --name treasury-cli \
    -v ~/.treasury:/home/appuser/.treasury \
    universal-treasury-cli:1.0.0
```

## 📊 Monitoring and Logging

### View Container Logs
```bash
podman logs treasury-cli -f
```

### Check Resource Usage
```bash
podman stats treasury-cli
```

### Health Check
```bash
podman inspect --format='{{.State.Health.Status}}' treasury-cli
```

## 🚨 Troubleshooting

### Common Issues

**1. Permission denied errors**
```bash
# Ensure proper permissions
chmod -R 755 ~/.treasury
podman unshare chown -R $UID:$GID ~/.treasury
```

**2. Port already in use**
```bash
# Find and kill process
sudo lsof -i :8080
kill -9 PID
```

**3. Database connection issues**
```bash
# Check SQLite permissions
chmod 644 ~/.treasury/treasury.db
```

**4. Podman service not starting**
```bash
# Check systemd logs
journalctl -u treasury-cli -f
```

## 🎯 Advanced Configuration

### Multi-Container Setup

Edit `podman-compose.yml` to uncomment and configure:
- PostgreSQL database service
- Webhook receiver service
- Redis caching service

### Custom Networking
```bash
podman network create treasury-net --subnet=10.88.0.0/16
podman run --network treasury-net --ip=10.88.0.100 ...
```

### Volume Management
```bash
# List volumes
podman volume ls

# Inspect volume
podman volume inspect treasury-data

# Cleanup
podman volume prune
```

## 📚 API Documentation

### Wise API Integration

The CLI integrates with Wise API v3:

**Authentication Flow**:
1. `treasury login` - Generates OAuth2 URL
2. User authorizes in browser
3. `treasury auth --code CODE` - Exchanges code for token
4. Token saved to `~/.treasury.yaml`

**Available Endpoints**:
- `GET /v3/profiles` - Get user profiles
- `GET /v4/accounts` - List accounts
- `GET /v1/balances` - Check balances
- `POST /v1/transfers` - Create transfers

## 🔧 Development Workflow

### Local Development with Podman
```bash
# Run in development mode
podman run -it --rm \
    -v ~/.treasury:/home/appuser/.treasury \
    -v ./:/app \
    -w /app \
    universal-treasury-cli:1.0.0 bash

# Test commands inside container
./treasury --help
./treasury login --client-id test --redirect-uri http://localhost:8080
```

### Debugging
```bash
# Enter running container
podman exec -it treasury-cli sh

# Check environment
printenv

# Test connectivity
curl https://api.sandbox.transferwise.tech/v3/profiles
```

## 🎉 Success!

You now have a production-ready Universal Treasury CLI deployed with Podman. The application features:

- ✅ **Complete Wise OAuth2 integration**
- ✅ **Real API calls with proper error handling**
- ✅ **SQLite database for local storage**
- ✅ **Multi-platform container deployment**
- ✅ **Systemd service for production**
- ✅ **Extensible architecture for more providers**

**Next Steps**:
1. Set up Wise developer account and get API credentials
2. Configure webhooks for real-time notifications
3. Add more financial providers (Stripe, Revolut)
4. Set up monitoring and alerts

Enjoy your Universal Treasury CLI! 🚀