#!/bin/bash
set -e

echo "🚀 Building Universal Treasury CLI for multiple architectures"
echo "=========================================================="

# Set version
VERSION="1.0.0"

# Platforms to build for
PLATFORMS=(
    "linux/amd64"
    "linux/arm64"
)

echo "📦 Building binaries..."

# Create dist directory
mkdir -p dist

for platform in "${PLATFORMS[@]}"
do
    echo "Building for $platform..."
    
    # Split platform into OS and ARCH
    IFS='/' read -r OS ARCH <<< "$platform"
    
    # Set output name
    OUTPUT="dist/treasury_${VERSION}_${OS}_${ARCH}"
    
    # Build
    GOOS=$OS GOARCH=$ARCH CGO_ENABLED=0 go build -o "$OUTPUT" main.go
    
    # Make executable
    chmod +x "$OUTPUT"
    
    echo "✅ Built: $OUTPUT"
done

echo ""
echo "🐳 Building Podman containers..."

for platform in "${PLATFORMS[@]}"
do
    echo "Building container for $platform..."
    
    # Split platform into OS and ARCH
    IFS='/' read -r OS ARCH <<< "$platform"
    
    # Set image name
    IMAGE="universal-treasury-cli:${VERSION}-${OS}-${ARCH}"
    
    # Set binary path
    BINARY="dist/treasury_${VERSION}_${OS}_${ARCH}"
    
    # Build Podman container
    podman build -t "$IMAGE" \
        --build-arg BINARY="$BINARY" \
        --build-arg PLATFORM="$platform" \
        -f Containerfile.multiarch .
    
    echo "✅ Built: $IMAGE"
done

echo ""
echo "🎉 Multi-architecture build complete!"
echo "===================================="
echo "Available binaries:"
ls -lh dist/
echo ""
echo "Available containers:"
podman images | grep universal-treasury-cli