#!/bin/bash
# Build Energetic Lexicon Executable
# 🔒 PRIVATE - PROPRIETARY
# © 2025 Baker Street Laboratory

set -e  # Exit on error

echo "🔧 Building Energetic Lexicon Executable"
echo "========================================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Change to project root
cd "$(dirname "$0")/.."

# Step 1: Clean previous builds
echo -e "${YELLOW}1. Cleaning previous builds...${NC}"
rm -rf build/ dist/
mkdir -p dist/

# Step 2: Install dependencies
echo -e "${YELLOW}2. Installing dependencies...${NC}"
if ! command -v pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

# Check for UPX (optional)
UPX_AVAILABLE=false
if command -v upx &> /dev/null; then
    UPX_AVAILABLE=true
    echo "UPX found: Will compress binary"
else
    echo "UPX not found: Skipping compression (install with: pkg install upx)"
fi

# Step 3: Build with PyInstaller
echo -e "${YELLOW}3. Building with PyInstaller...${NC}"
pyinstaller energetic_lexicon.spec --clean

if [ ! -f "dist/energetic-lexicon" ]; then
    echo -e "${RED}❌ Build failed: executable not found${NC}"
    exit 1
fi

# Step 4: Compress with UPX (if available)
if [ "$UPX_AVAILABLE" = true ]; then
    echo -e "${YELLOW}4. Compressing with UPX...${NC}"
    upx --best --lzma dist/energetic-lexicon || {
        echo "UPX compression failed (continuing anyway)"
    }
else
    echo -e "${YELLOW}4. Skipping UPX compression (not installed)${NC}"
fi

# Step 5: Sign binary (if GPG key available)
echo -e "${YELLOW}5. Signing binary with GPG...${NC}"
if command -v gpg &> /dev/null; then
    gpg --detach-sign --armor dist/energetic-lexicon 2>/dev/null || {
        echo "GPG signing skipped (no default key configured)"
    }
else
    echo "GPG not found: Skipping signing"
fi

# Step 6: Generate checksums
echo -e "${YELLOW}6. Generating checksums...${NC}"
cd dist
sha256sum energetic-lexicon* > SHA256SUMS 2>/dev/null || {
    # Fallback for macOS
    shasum -a 256 energetic-lexicon* > SHA256SUMS
}
md5sum energetic-lexicon* > MD5SUMS 2>/dev/null || {
    # Fallback for macOS
    md5 energetic-lexicon* > MD5SUMS
}
cd ..

# Step 7: Test executable
echo -e "${YELLOW}7. Testing executable...${NC}"
chmod +x dist/energetic-lexicon

if ./dist/energetic-lexicon version; then
    echo -e "${GREEN}✅ Version command successful${NC}"
else
    echo -e "${RED}❌ Version command failed${NC}"
    exit 1
fi

# Step 8: Display summary
echo ""
echo -e "${GREEN}✅ Build complete!${NC}"
echo "========================================"
echo "Executable: dist/energetic-lexicon"
echo "Size: $(du -h dist/energetic-lexicon | cut -f1)"
echo ""
echo "Files created:"
ls -lh dist/

echo ""
echo "Next steps:"
echo "  1. Test: ./dist/energetic-lexicon init --no-sample"
echo "  2. Distribute: Upload dist/* to GitHub Releases"
echo "  3. Users run: ./energetic-lexicon --help"
