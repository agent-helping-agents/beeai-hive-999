#!/bin/bash
set -e

echo "🚀 Universal Treasury CLI - Podman Deployment"
echo "============================================"

# Set version
VERSION="1.0.0"
IMAGE_NAME="universal-treasury-cli"

# Check if podman is installed
if ! command -v podman &> /dev/null; then
    echo "❌ Error: Podman is not installed"
    echo "Please install Podman first:"
    echo "  sudo apt-get install podman (Debian/Ubuntu)"
    echo "  sudo dnf install podman (Fedora/RHEL)"
    exit 1
fi

echo "✅ Podman found: $(podman --version)"

# Build the Go application first
echo "🔨 Building Go application..."
export PATH=$PATH:~/local/go/bin
if ! go build -o treasury main.go; then
    echo "❌ Error: Failed to build Go application"
    exit 1
fi
echo "✅ Go build successful"

# Build the Podman container
echo "🐳 Building Podman container..."
if ! podman build -t "$IMAGE_NAME:$VERSION" -f Containerfile .; then
    echo "❌ Error: Failed to build Podman container"
    exit 1
fi
echo "✅ Podman build successful"

# Create a pod for the application
echo "🎯 Creating Podman pod..."
if podman pod exists treasury-pod; then
    echo "🗑 Removing existing pod..."
    podman pod rm -f treasury-pod
fi

if ! podman pod create --name treasury-pod -p 8080:8080; then
    echo "❌ Error: Failed to create pod"
    exit 1
fi
echo "✅ Pod created successfully"

# Run the container in the pod
echo "🚀 Running container..."
if ! podman run -d \
    --pod treasury-pod \
    --name treasury-cli \
    -v "$HOME/.treasury:/home/appuser/.treasury" \
    -v "$PWD/config:/app/config" \
    --restart always \
    "$IMAGE_NAME:$VERSION"; then
    echo "❌ Error: Failed to run container"
    exit 1
fi
echo "✅ Container running successfully"

# Show pod status
echo ""
echo "📊 Pod Status:"
podman pod ps

echo ""
echo "📦 Container Status:"
podman ps --pod

echo ""
echo "🎉 Deployment Complete!"
echo "======================"
echo "Universal Treasury CLI is now running in Podman"
echo ""
echo "Access the CLI with:"
echo "  podman exec -it treasury-cli treasury --help"
echo ""
echo "Or use specific commands:"
echo "  podman exec -it treasury-cli treasury login --help"
echo "  podman exec -it treasury-cli treasury profile"
echo "  podman exec -it treasury-cli treasury listen"
echo ""
echo "Your data is persisted in:"
echo "  Config: $HOME/.treasury/"
echo "  Database: $HOME/.treasury/treasury.db"
echo ""
echo "To stop the service:"
echo "  podman pod stop treasury-pod"
echo ""
echo "To start the service:"
echo "  podman pod start treasury-pod"
echo ""
echo "To remove everything:"
echo "  podman pod rm -f treasury-pod"
echo "  podman rmi $IMAGE_NAME:$VERSION"