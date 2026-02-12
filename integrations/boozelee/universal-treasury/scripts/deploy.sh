#!/bin/bash
set -e

echo "🚀 Universal Treasury CLI - Deployment Script"
echo "============================================"

# Set version
VERSION="1.0.0"

# Build for multiple platforms
PLATFORMS=("linux/amd64" "linux/arm64" "darwin/amd64" "darwin/arm64" "windows/amd64")

echo "📦 Building binaries for all platforms..."

# Create dist directory
mkdir -p dist

for platform in "${PLATFORMS[@]}"
do
    echo "Building for $platform..."
    
    # Split platform into OS and ARCH
    IFS='/' read -r OS ARCH <<< "$platform"
    
    # Set output name
    if [ "$OS" = "windows" ]; then
        OUTPUT="dist/treasury_${VERSION}_${OS}_${ARCH}.exe"
    else
        OUTPUT="dist/treasury_${VERSION}_${OS}_${ARCH}"
    fi
    
    # Build
    GOOS=$OS GOARCH=$ARCH go build -o "$OUTPUT" main.go
    
    # Make executable (not needed for Windows)
    if [ "$OS" != "windows" ]; then
        chmod +x "$OUTPUT"
    fi
    
    echo "✅ Built: $OUTPUT"
done

echo ""
echo "📦 Creating archive..."
cd dist
zip ../treasury_${VERSION}_universal.zip treasury_${VERSION}_*
cd ..

echo ""
echo "🎉 Deployment Complete!"
echo "======================"
echo "Available binaries:"
ls -lh dist/
echo ""
echo "Universal zip archive:"
ls -lh treasury_${VERSION}_universal.zip
echo ""
echo "To install:"
echo "1. Extract the appropriate binary for your platform"
echo "2. Make it executable: chmod +x treasury"
echo "3. Run: ./treasury --help"
