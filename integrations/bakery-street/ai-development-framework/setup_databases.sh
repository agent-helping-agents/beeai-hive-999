#!/bin/bash
# Database Setup Script for AIOS Orchestrator
# Sets up PostgreSQL and Redis databases

set -e

echo "🗄️ Setting up Databases for AIOS Orchestrator"
echo "=============================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# Create network for AIOS services
echo "🌐 Creating AIOS network..."
docker network create aios-network 2>/dev/null || echo "Network already exists"

# Start PostgreSQL
echo "🐘 Starting PostgreSQL database..."
docker run -d \
    --name aios-postgres \
    --network aios-network \
    -e POSTGRES_DB=aios_prod \
    -e POSTGRES_USER=aios \
    -e POSTGRES_PASSWORD=aios_password \
    -p 5432:5432 \
    -v aios_postgres_data:/var/lib/postgresql/data \
    postgres:15

echo "✅ PostgreSQL started on port 5432"
echo "   Database: aios_prod"
echo "   Username: aios"
echo "   Password: aios_password"

# Start Redis
echo "🔴 Starting Redis cache..."
docker run -d \
    --name aios-redis \
    --network aios-network \
    -p 6379:6379 \
    -v aios_redis_data:/data \
    redis:7-alpine

echo "✅ Redis started on port 6379"

# Wait for databases to be ready
echo "⏳ Waiting for databases to be ready..."
sleep 10

# Test PostgreSQL connection
echo "🧪 Testing PostgreSQL connection..."
if docker exec aios-postgres pg_isready -U aios -d aios_prod > /dev/null 2>&1; then
    echo "✅ PostgreSQL is ready and accepting connections"
else
    echo "❌ PostgreSQL is not ready yet. Please wait a moment and try again."
fi

# Test Redis connection
echo "🧪 Testing Redis connection..."
if docker exec aios-redis redis-cli ping | grep -q "PONG"; then
    echo "✅ Redis is ready and accepting connections"
else
    echo "❌ Redis is not ready yet. Please wait a moment and try again."
fi

# Update environment file with database URLs
echo "📝 Updating environment configuration..."
if [ -f .env.production ]; then
    # Backup original file
    cp .env.production .env.production.backup
    
    # Update database URLs
    sed -i 's|AIOS_DATABASE_URL=.*|AIOS_DATABASE_URL=postgresql://aios:aios_password@localhost:5432/aios_prod|' .env.production
    sed -i 's|AIOS_REDIS_URL=.*|AIOS_REDIS_URL=redis://localhost:6379/0|' .env.production
    
    echo "✅ Environment file updated with database URLs"
else
    echo "⚠️ .env.production file not found. Please run the API key setup first."
fi

echo ""
echo "🎉 Database setup completed!"
echo "=========================="
echo "📊 PostgreSQL: localhost:5432 (aios_prod)"
echo "🔴 Redis: localhost:6379"
echo "🌐 Network: aios-network"
echo ""
echo "🚀 Next step: Configure API keys and deploy with Docker!"
echo "   Run: python setup_api_keys.py"
echo "   Then: docker-compose up -d"
