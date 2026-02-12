# NVIDIA DKMS Kernel 6.17.0 Build Failure Fix Guide

## Problem Description

The NVIDIA DKMS module (version 560.35.05) fails to build with Linux kernel 6.17.0-8-generic. The error occurs because the build system cannot find required header files:

```
nvidia/nv-cray.c:26:10: fatal error: os-interface.h: No such file or directory
nvidia/nv-dma.c:26:10: fatal error: os-interface.h: No such file or directory  
nvidia/nv-mmap.c:26:10: fatal error: os-interface.h: No such file or directory
nvidia/nv.c:30:10: fatal error: nv-firmware.h: No such file or directory
nvidia/nv-dmabuf.c:24:10: fatal error: nv-dmabuf.h: No such file or directory
nvidia/nv-pci.c:25:10: fatal error: nv-pci-types.h: No such file or directory
```

## Root Cause

The NVIDIA source files are trying to include headers using relative paths like:
```c
#include "os-interface.h"
```

But these headers are actually located in `common/inc/` directory, not in the `nvidia/` directory where the compilation is happening.

## Solution Options

### Option 1: Create Symlinks (Recommended)

```bash
# Navigate to the NVIDIA build directory
cd /var/lib/dkms/nvidia/560.35.05/build

# Create symlinks from nvidia/ directory to common/inc/
sudo ln -sf ../common/inc/os-interface.h nvidia/os-interface.h
sudo ln -sf ../common/inc/nv-firmware.h nvidia/nv-firmware.h
sudo ln -sf ../common/inc/nv-dmabuf.h nvidia/nv-dmabuf.h
sudo ln -sf ../common/inc/nv-pci-types.h nvidia/nv-pci-types.h

# Then rebuild the DKMS module
sudo dkms install -m nvidia -v 560.35.05 -k $(uname -r)

# Load the module
sudo modprobe nvidia
```

### Option 2: Copy Header Files

```bash
# Copy the required headers to the nvidia directory
sudo cp common/inc/os-interface.h nvidia/
sudo cp common/inc/nv-firmware.h nvidia/
sudo cp common/inc/nv-dmabuf.h nvidia/
sudo cp common/inc/nv-pci-types.h nvidia/

# Then rebuild as above
sudo dkms install -m nvidia -v 560.35.05 -k $(uname -r)
```

### Option 3: Modify Include Paths (Advanced)

Edit the Kbuild file to ensure proper include paths:

```bash
sudo nano /var/lib/dkms/nvidia/560.35.05/build/Kbuild
```

Find the line:
```makefile
EXTRA_CFLAGS += -I$(src)/common/inc
```

And ensure it's properly included in the compilation flags.

### Option 4: Use DKMS Autoinstall

```bash
# Remove the failed installation
sudo dkms remove -m nvidia -v 560.35.05 --all

# Reinstall
sudo dkms install -m nvidia -v 560.35.05

# Or use autoinstall
sudo dkms autoinstall
```

## Verification Steps

After applying the fix:

1. Check if the module is loaded:
   ```bash
   lsmod | grep nvidia
   ```

2. Check NVIDIA driver status:
   ```bash
   nvidia-smi
   ```

3. Check DKMS status:
   ```bash
   dkms status
   ```

## Alternative Solutions

### Downgrade Kernel (Temporary Workaround)

If you need immediate functionality, you can boot into an older kernel version:

1. Check available kernels:
   ```bash
   ls /boot/vmlinuz-*
   ```

2. Update GRUB to boot from an older kernel
3. Reboot and select the older kernel

### Install Different NVIDIA Driver Version

Some users report success with different NVIDIA driver versions. You can try:

```bash
# Remove current driver
sudo apt purge nvidia-* 

# Install a different version
sudo apt install nvidia-driver-535  # or other version

# Reinstall CUDA if needed
sudo apt install cuda-12-6
```

## Troubleshooting

### If symlinks don't work

Check if the headers exist in the expected location:
```bash
ls -la /var/lib/dkms/nvidia/560.35.05/build/common/inc/
```

### If DKMS still fails

Check the latest build log:
```bash
tail -50 /var/lib/dkms/nvidia/560.35.05/build/make.log
```

### If module won't load

Check kernel messages:
```bash
dmesg | grep nvidia
journalctl -xe | grep nvidia
```

## Prevention for Future Updates

To prevent this issue when updating:

1. **Hold NVIDIA packages during kernel updates:**
   ```bash
   sudo apt-mark hold nvidia-* cuda-* 
   ```

2. **Update NVIDIA drivers before kernel updates**

3. **Use the proprietary NVIDIA installer** instead of distribution packages

## Additional Resources

- NVIDIA DKMS documentation: https://download.nvidia.com/XFree86/Linux-x86_64/560.35.05/README/dkms.html
- Ubuntu NVIDIA troubleshooting: https://wiki.ubuntu.com/NvidiaGraphicsDrivers
- Kernel 6.17 compatibility: Check NVIDIA forums for latest driver updates

## Notes

- This issue occurs because NVIDIA driver 560.35.05 was released before kernel 6.17.0
- NVIDIA typically releases driver updates to support new kernels within a few weeks
- Check for driver updates at: https://www.nvidia.com/Download/index.aspx

## Manual Fix Script

If you have sudo access, you can use the provided `fix_nvidia_dkms.sh` script:

```bash
chmod +x fix_nvidia_dkms.sh
sudo ./fix_nvidia_dkms.sh
```

The script will:
1. Create the necessary symlinks
2. Rebuild the DKMS module  
3. Attempt to load the NVIDIA kernel module
4. Provide status information

## Expected Outcome

After successfully applying the fix:
- ✅ NVIDIA DKMS module builds without errors
- ✅ `nvidia-smi` shows GPU information
- ✅ CUDA applications work properly
- ✅ No more "fatal error: header.h: No such file or directory" messages

If you continue to experience issues, consider:
1. Checking NVIDIA's website for updated drivers
2. Reporting the issue to NVIDIA's Linux driver team
3. Using a different kernel version temporarily