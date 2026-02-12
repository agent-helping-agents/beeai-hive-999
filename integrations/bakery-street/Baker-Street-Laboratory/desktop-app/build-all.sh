#!/bin/bash
echo "🔬 Building Baker Street Laboratory Desktop App for All Platforms"
echo "================================================================"

echo "Building for Windows..."
npm run build-win

echo "Building for macOS..."
npm run build-mac

echo "Building for Linux..."
npm run build-linux

echo "✅ Build complete! Check the 'dist' directory for installers."
