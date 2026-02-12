#!/usr/bin/env python3
"""
Production Deployment Script for Advanced AI Orchestrator
Shows how to deploy the system to production with proper configuration
"""

import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime

# Add AIOS environment to path
aios_env_path = os.path.join(os.getcwd(), "environments", "aios-env", "lib", "python3.11", "site-packages")
if aios_env_path not in sys.path:
    sys.path.insert(0, aios_env_path)

try:
    from aios.object import Object
    from aios.state import State
    from aios.core_utils import format_timestamp
    print("✅ AIOS modules imported successfully")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

class ProductionDeployer:
    """Production deployment manager for AI Orchestrator"""
    
    def __init__(self):
        self.deployment_config = {}
        self.environment_vars = {}
        self.docker_config = {}
        self.kubernetes_config = {}
        
        print("🚀 Production Deployment Manager Initialized")
    
    def create_environment_config(self):
        """Create environment configuration files"""
        
        print("\n🔧 Creating Environment Configuration...")
        print("=" * 60)
        
        # Environment variables
        env_config = {
            "AIOS_ENVIRONMENT": "production",
            "AIOS_LOG_LEVEL": "INFO",
            "AIOS_DATABASE_URL": "postgresql://user:pass@localhost:5432/aios_prod",
            "AIOS_REDIS_URL": "redis://localhost:6379/0",
            "AIOS_API_KEY": "your_api_key_here",
            "AIOS_SECRET_KEY": "your_secret_key_here",
            "CREWAI_OPENAI_API_KEY": "your_openai_key_here",
            "CREWAI_ANTHROPIC_API_KEY": "your_anthropic_key_here",
            "CREWAI_GOOGLE_API_KEY": "your_google_key_here",
            "MONITORING_ENABLED": "true",
            "METRICS_COLLECTION": "true",
            "ALERTING_ENABLED": "true"
        }
        
        # Save to .env file
        with open('.env.production', 'w') as f:
            for key, value in env_config.items():
                f.write(f"{key}={value}\n")
        
        print("✅ Environment configuration created: .env.production")
        
        # Create config directory
        os.makedirs('config', exist_ok=True)
        
        # Production configuration
        prod_config = {
            "deployment": {
                "environment": "production",
                "version": "1.0.0",
                "deployment_date": format_timestamp(datetime.now().timestamp()),
                "max_instances": 10,
                "auto_scaling": True,
                "health_check_interval": 30,
                "timeout_seconds": 600
            },
            "aios": {
                "max_agents": 100,
                "max_workflows": 50,
                "state_persistence": True,
                "backup_enabled": True,
                "encryption_enabled": True
            },
            "crewai": {
                "max_concurrent_agents": 20,
                "memory_enabled": True,
                "tool_integration": True,
                "api_rate_limits": {
                    "openai": 1000,
                    "anthropic": 500,
                    "google": 2000
                }
            },
            "monitoring": {
                "prometheus_enabled": True,
                "grafana_enabled": True,
                "log_aggregation": True,
                "alerting": {
                    "email": True,
                    "slack": True,
                    "pagerduty": False
                }
            },
            "security": {
                "authentication": "jwt",
                "authorization": "rbac",
                "encryption": "aes-256",
                "rate_limiting": True,
                "audit_logging": True
            }
        }
        
        # Save production config
        with open('config/production.yaml', 'w') as f:
            yaml.dump(prod_config, f, default_flow_style=False, indent=2)
        
        print("✅ Production configuration created: config/production.yaml")
        
        return prod_config
    
    def create_docker_config(self):
        """Create Docker configuration for containerized deployment"""
        
        print("\n🐳 Creating Docker Configuration...")
        print("=" * 60)
        
        # Dockerfile
        dockerfile = """# Production Dockerfile for AI Orchestrator
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 aios && chown -R aios:aios /app
USER aios

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["python", "app.py"]
"""
        
        with open('Dockerfile', 'w') as f:
            f.write(dockerfile)
        
        # Docker Compose
        docker_compose = """version: '3.8'

services:
  aios-orchestrator:
    build: .
    ports:
      - "8000:8000"
    environment:
      - AIOS_ENVIRONMENT=production
      - AIOS_DATABASE_URL=postgresql://aios:password@postgres:5432/aios_prod
      - AIOS_REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2.0'
        reservations:
          memory: 1G
          cpus: '1.0'

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: aios_prod
      POSTGRES_USER: aios
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    restart: unless-stopped

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
"""
        
        with open('docker-compose.yml', 'w') as f:
            f.write(docker_compose)
        
        print("✅ Docker configuration created:")
        print("   🐳 Dockerfile")
        print("   🐳 docker-compose.yml")
    
    def create_kubernetes_config(self):
        """Create Kubernetes configuration for cloud deployment"""
        
        print("\n☸️ Creating Kubernetes Configuration...")
        print("=" * 60)
        
        # Kubernetes deployment
        k8s_deployment = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: aios-orchestrator
  labels:
    app: aios-orchestrator
spec:
  replicas: 3
  selector:
    matchLabels:
      app: aios-orchestrator
  template:
    metadata:
      labels:
        app: aios-orchestrator
    spec:
      containers:
      - name: aios-orchestrator
        image: aios-orchestrator:latest
        ports:
        - containerPort: 8000
        env:
        - name: AIOS_ENVIRONMENT
          value: "production"
        - name: AIOS_DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: aios-secrets
              key: database-url
        - name: AIOS_API_KEY
          valueFrom:
            secretKeyRef:
              name: aios-secrets
              key: api-key
        resources:
          limits:
            memory: "2Gi"
            cpu: "2000m"
          requests:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: aios-orchestrator-service
spec:
  selector:
    app: aios-orchestrator
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
---
apiVersion: v1
kind: Secret
metadata:
  name: aios-secrets
type: Opaque
data:
  database-url: <base64-encoded-database-url>
  api-key: <base64-encoded-api-key>
"""
        
        with open('k8s/deployment.yaml', 'w') as f:
            os.makedirs('k8s', exist_ok=True)
            f.write(k8s_deployment)
        
        print("✅ Kubernetes configuration created: k8s/deployment.yaml")
    
    def create_monitoring_config(self):
        """Create monitoring and alerting configuration"""
        
        print("\n📊 Creating Monitoring Configuration...")
        print("=" * 60)
        
        # Prometheus configuration
        prometheus_config = """global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'aios-orchestrator'
    static_configs:
      - targets: ['aios-orchestrator:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
"""
        
        os.makedirs('monitoring', exist_ok=True)
        with open('monitoring/prometheus.yml', 'w') as f:
            f.write(prometheus_config)
        
        # Alert rules
        alert_rules = """groups:
  - name: aios_alerts
    rules:
      - alert: AIOSHighCPUUsage
        expr: container_cpu_usage_seconds_total{container="aios-orchestrator"} > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "AIOS Orchestrator CPU usage is above 80%"

      - alert: AIOSHighMemoryUsage
        expr: container_memory_usage_bytes{container="aios-orchestrator"} > 1.5e9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"
          description: "AIOS Orchestrator memory usage is above 1.5GB"

      - alert: AIOSWorkflowFailure
        expr: aios_workflow_failures_total > 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Workflow failures detected"
          description: "AIOS workflows are failing"
"""
        
        with open('monitoring/alert_rules.yml', 'w') as f:
            f.write(alert_rules)
        
        print("✅ Monitoring configuration created:")
        print("   📊 monitoring/prometheus.yml")
        print("   📊 monitoring/alert_rules.yml")
    
    def create_ci_cd_config(self):
        """Create CI/CD pipeline configuration"""
        
        print("\n🔄 Creating CI/CD Configuration...")
        print("=" * 60)
        
        # GitHub Actions workflow
        github_actions = """name: AIOS Orchestrator CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest --cov=aios --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t aios-orchestrator:${{ github.sha }} .
        docker tag aios-orchestrator:${{ github.sha }} aios-orchestrator:latest
    
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
        # Add your deployment commands here
"""
        
        os.makedirs('.github/workflows', exist_ok=True)
        with open('.github/workflows/ci-cd.yml', 'w') as f:
            f.write(github_actions)
        
        print("✅ CI/CD configuration created: .github/workflows/ci-cd.yml")
    
    def create_requirements_file(self):
        """Create production requirements file"""
        
        print("\n📦 Creating Production Requirements...")
        print("=" * 60)
        
        requirements = """# Production requirements for AIOS Orchestrator
# Core AIOS components
aios>=0.2.2

# CrewAI for multi-agent orchestration
crewai>=0.175.0

# Web framework
fastapi>=0.104.0
uvicorn[standard]>=0.24.0

# Database and caching
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
redis>=5.0.0
alembic>=1.12.0

# Monitoring and observability
prometheus-client>=0.19.0
opentelemetry-api>=1.20.0
opentelemetry-sdk>=1.20.0
opentelemetry-exporter-prometheus>=1.20.0

# Security
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6

# Configuration and environment
python-dotenv>=1.0.0
pydantic-settings>=2.0.0
pyyaml>=6.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0

# Development tools
black>=23.0.0
flake8>=6.0.0
mypy>=1.5.0
"""
        
        with open('requirements.txt', 'w') as f:
            f.write(requirements)
        
        print("✅ Production requirements created: requirements.txt")
    
    def create_deployment_script(self):
        """Create deployment automation script"""
        
        print("\n🚀 Creating Deployment Scripts...")
        print("=" * 60)
        
        # Production deployment script
        deploy_script = """#!/bin/bash
# Production Deployment Script for AIOS Orchestrator

set -e

echo "🚀 Starting AIOS Orchestrator Production Deployment..."

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please don't run as root"
    exit 1
fi

# Load environment variables
if [ -f .env.production ]; then
    echo "📋 Loading production environment variables..."
    export $(cat .env.production | xargs)
else
    echo "❌ .env.production file not found"
    exit 1
fi

# Check required environment variables
required_vars=("AIOS_API_KEY" "AIOS_DATABASE_URL" "CREWAI_OPENAI_API_KEY")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Required environment variable $var is not set"
        exit 1
    fi
done

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs data config monitoring

# Install dependencies
echo "📦 Installing production dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️ Running database migrations..."
alembic upgrade head

# Start services
echo "🚀 Starting AIOS Orchestrator services..."

# Start with Docker Compose if available
if command -v docker-compose &> /dev/null; then
    echo "🐳 Starting with Docker Compose..."
    docker-compose up -d
else
    echo "🐍 Starting with Python directly..."
    python app.py &
    echo $! > aios.pid
fi

echo "✅ AIOS Orchestrator deployed successfully!"
echo "🌐 Access the application at: http://localhost:8000"
echo "📊 Access monitoring at: http://localhost:3000 (Grafana)"
echo "📈 Access metrics at: http://localhost:9090 (Prometheus)"
"""
        
        with open('deploy_production.sh', 'w') as f:
            f.write(deploy_script)
        
        # Make executable
        os.chmod('deploy_production.sh', 0o755)
        
        print("✅ Deployment script created: deploy_production.sh")
    
    def generate_deployment_summary(self):
        """Generate deployment summary and next steps"""
        
        print("\n📋 Deployment Summary Generated!")
        print("=" * 60)
        
        summary = {
            "deployment_date": format_timestamp(datetime.now().timestamp()),
            "components_created": [
                "Environment configuration (.env.production)",
                "Production configuration (config/production.yaml)",
                "Docker configuration (Dockerfile, docker-compose.yml)",
                "Kubernetes configuration (k8s/deployment.yaml)",
                "Monitoring configuration (monitoring/)",
                "CI/CD pipeline (.github/workflows/ci-cd.yml)",
                "Production requirements (requirements.txt)",
                "Deployment script (deploy_production.sh)"
            ],
            "next_steps": [
                "1. Configure API keys in .env.production",
                "2. Set up PostgreSQL and Redis databases",
                "3. Configure monitoring endpoints",
                "4. Set up CI/CD pipeline in GitHub",
                "5. Deploy to your target environment",
                "6. Configure monitoring and alerting",
                "7. Set up backup and recovery procedures"
            ],
            "production_features": [
                "Multi-agent orchestration with CrewAI",
                "Advanced state management with AIOS",
                "Containerized deployment with Docker",
                "Kubernetes orchestration support",
                "Comprehensive monitoring and alerting",
                "Automated CI/CD pipelines",
                "Production-grade security and authentication",
                "Scalable architecture with auto-scaling"
            ]
        }
        
        # Save summary
        with open('deployment_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("✅ Deployment summary saved: deployment_summary.json")
        return summary

def main():
    """Main deployment configuration function"""
    
    print("🚀 AIOS Orchestrator Production Deployment Configuration")
    print("=" * 80)
    
    try:
        deployer = ProductionDeployer()
        
        # Create all configuration files
        deployer.create_environment_config()
        deployer.create_docker_config()
        deployer.create_kubernetes_config()
        deployer.create_monitoring_config()
        deployer.create_ci_cd_config()
        deployer.create_requirements_file()
        deployer.create_deployment_script()
        
        # Generate summary
        summary = deployer.generate_deployment_summary()
        
        print("\n" + "=" * 80)
        print("🎉 Production Deployment Configuration Complete!")
        print("\n📁 Files Created:")
        for component in summary["components_created"]:
            print(f"   ✅ {component}")
        
        print("\n🚀 Next Steps:")
        for step in summary["next_steps"]:
            print(f"   {step}")
        
        print("\n🏆 Production Features Available:")
        for feature in summary["production_features"]:
            print(f"   ✨ {feature}")
        
        print("\n🎯 Your AIOS Orchestrator is ready for production deployment!")
        print("🚀 Run './deploy_production.sh' to deploy to production!")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment configuration failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 Production deployment configuration completed successfully!")
    else:
        print("\n💥 There were issues with the deployment configuration.")
