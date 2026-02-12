#!/bin/bash
# Tiny-Cloud Deployment Script for beeAI
# Usage: ./deploy.sh --env [development|staging|production]

set -e

ENV="${2:-development}"
APP_NAME="beeai"
TINY_CLOUD_HOST="${TINY_CLOUD_HOST:-tiny-cloud.local}"

echo "🐝 Deploying beeAI to Tiny-Cloud..."
echo "Environment: $ENV"

# Validate environment
if [[ ! "$ENV" =~ ^(development|staging|production)$ ]]; then
    echo "❌ Invalid environment. Use: development, staging, or production"
    exit 1
fi

# Check prerequisites
echo "🔍 Checking prerequisites..."
command -v docker >/dev/null 2>&1 || { echo "❌ Docker required"; exit 1; }
command -v ssh >/dev/null 2>&1 || { echo "❌ SSH required"; exit 1; }

# Build Docker image
echo "🔨 Building Docker image..."
docker build -t $APP_NAME:$ENV -f ../docker/Dockerfile ../../

# Export image
echo "📦 Exporting image..."
docker save $APP_NAME:$ENV | gzip > $APP_NAME-$ENV.tar.gz

# Deploy to Tiny-Cloud
echo "🚀 Deploying to Tiny-Cloud ($TINY_CLOUD_HOST)..."
scp $APP_NAME-$ENV.tar.gz tiny-cloud@$TINY_CLOUD_HOST:/opt/apps/
ssh tiny-cloud@$TINY_CLOUD_HOST << 'EOF'
    cd /opt/apps
    docker load < beeai-$ENV.tar.gz
    docker stop beeai-$ENV 2>/dev/null || true
    docker rm beeai-$ENV 2>/dev/null || true
    docker run -d \
        --name beeai-$ENV \
        --restart unless-stopped \
        -p 22181:22181 \
        -e T221B_SECRET_KEY="$(cat /etc/secrets/t221b_key)" \
        -e ENV=$ENV \
        beeai:$ENV
EOF

# Cleanup
rm -f $APP_NAME-$ENV.tar.gz

echo "✅ Deployment complete!"
echo "API available at: https://$TINY_CLOUD_HOST:22181"
echo ""
echo "🔍 Health check:"
curl -s https://$TINY_CLOUD_HOST:22181/health || echo "⚠️ Health check failed"
