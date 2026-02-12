#!/bin/bash

# NVIDIA DKMS Kernel 6.17 Build Failure Fix
# This script fixes the missing header file issue for NVIDIA DKMS 560.35.05 with kernel 6.17.0

echo "=== NVIDIA DKMS Kernel 6.17 Build Failure Fix ==="
echo "Fixing missing header file includes for NVIDIA driver 560.35.05"
echo ""

# Check if we're running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root. Please use sudo."
    exit 1
fi

# Check if the NVIDIA DKMS build directory exists
NVIDIA_BUILD_DIR="/var/lib/dkms/nvidia/560.35.05/build"
if [ ! -d "$NVIDIA_BUILD_DIR" ]; then
    echo "NVIDIA DKMS build directory not found: $NVIDIA_BUILD_DIR"
    exit 1
fi

echo "1. Checking current build status..."
cd "$NVIDIA_BUILD_DIR" || exit 1

# Check if the common/inc directory exists and has the required headers
echo "2. Verifying header files exist..."
if [ ! -f "common/inc/os-interface.h" ]; then
    echo "ERROR: os-interface.h not found in common/inc/"
    exit 1
fi

if [ ! -f "common/inc/nv-firmware.h" ]; then
    echo "ERROR: nv-firmware.h not found in common/inc/"
    exit 1
fi

if [ ! -f "common/inc/nv-dmabuf.h" ]; then
    echo "ERROR: nv-dmabuf.h not found in common/inc/"
    exit 1
fi

if [ ! -f "common/inc/nv-pci-types.h" ]; then
    echo "ERROR: nv-pci-types.h not found in common/inc/"
    exit 1
fi

echo "✓ All required header files found"

echo "3. Creating symlinks for missing headers in nvidia directory..."
# Create symlinks from the nvidia directory to the common/inc directory
ln -sf ../common/inc/os-interface.h nvidia/os-interface.h
ln -sf ../common/inc/nv-firmware.h nvidia/nv-firmware.h  
ln -sf ../common/inc/nv-dmabuf.h nvidia/nv-dmabuf.h
ln -sf ../common/inc/nv-pci-types.h nvidia/nv-pci-types.h

echo "✓ Symlinks created"

echo "4. Attempting to rebuild NVIDIA DKMS module..."
# Try to rebuild the DKMS module
dkms install -m nvidia -v 560.35.05 -k $(uname -r)

if [ $? -eq 0 ]; then
    echo "✓ NVIDIA DKMS module built successfully!"
    
    echo "5. Loading NVIDIA kernel module..."
    modprobe nvidia
    
    if [ $? -eq 0 ]; then
        echo "✓ NVIDIA kernel module loaded successfully!"
        echo ""
        echo "=== Fix Complete ==="
        echo "The NVIDIA driver should now be working properly."
        echo "You may need to reboot for all changes to take effect."
    else
        echo "⚠ NVIDIA kernel module failed to load"
        echo "You may need to reboot for the module to load properly."
    fi
else
    echo "✗ NVIDIA DKMS module build failed"
    echo "Please check /var/lib/dkms/nvidia/560.35.05/build/make.log for details"
    exit 1
fi