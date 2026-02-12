#!/usr/bin/env python3
"""
Fix AIOS Installation
Properly installs AIOS in the virtual environment
"""

import subprocess
import sys
import os
from pathlib import Path
import shutil

def fix_aios_installation():
    """Fix the AIOS installation"""
    print("🔧 Fixing AIOS Installation...")
    
    # Get paths
    project_root = Path("/home/booze/ai-development")
    aios_env = project_root / "environments" / "aios-env"
    site_packages = aios_env / "lib" / "python3.11" / "site-packages"
    
    print(f"Project root: {project_root}")
    print(f"AIOS environment: {aios_env}")
    print(f"Site packages: {site_packages}")
    
    # Step 1: Clone AIOS repository
    print("\n📥 Step 1: Cloning AIOS repository...")
    aios_repo = project_root / "aios-repo"
    
    if aios_repo.exists():
        print(f"Removing existing AIOS repo: {aios_repo}")
        shutil.rmtree(aios_repo)
    
    try:
        result = subprocess.run([
            "git", "clone", "https://github.com/agiresearch/AIOS.git", str(aios_repo)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ AIOS repository cloned successfully")
        else:
            print(f"❌ Failed to clone AIOS: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error cloning AIOS: {e}")
        return False
    
    # Step 2: Check AIOS source structure
    print("\n🔍 Step 2: Checking AIOS source structure...")
    aios_src = aios_repo / "aios"
    
    if not aios_src.exists():
        print(f"❌ AIOS source directory not found: {aios_src}")
        return False
    
    print(f"✅ AIOS source found: {aios_src}")
    
    # List contents
    for item in aios_src.iterdir():
        if item.is_file():
            print(f"   📄 {item.name}")
        elif item.is_dir():
            print(f"   📁 {item.name}/")
    
    # Step 3: Copy AIOS to site-packages
    print("\n📦 Step 3: Installing AIOS to site-packages...")
    aios_dest = site_packages / "aios"
    
    if aios_dest.exists():
        print(f"Removing existing AIOS installation: {aios_dest}")
        shutil.rmtree(aios_dest)
    
    try:
        shutil.copytree(aios_src, aios_dest)
        print(f"✅ AIOS copied to: {aios_dest}")
    except Exception as e:
        print(f"❌ Failed to copy AIOS: {e}")
        return False
    
    # Step 4: Fix __init__.py if needed
    print("\n🔧 Step 4: Fixing AIOS __init__.py...")
    init_file = aios_dest / "__init__.py"
    
    if init_file.exists():
        # Check if it's empty or needs fixing
        content = init_file.read_text()
        if not content.strip() or "Object" not in content:
            print("Fixing __init__.py...")
            fixed_init = '''"""
AIOS - AGI Research Agent Orchestration System
"""

__version__ = "0.2.2"

from .object import Object
from .state import State

__all__ = ["Object", "State"]
'''
            init_file.write_text(fixed_init)
            print("✅ __init__.py fixed")
        else:
            print("✅ __init__.py looks good")
    else:
        print("❌ __init__.py not found")
        return False
    
    # Step 5: Test installation
    print("\n🧪 Step 5: Testing AIOS installation...")
    
    # Activate environment and test
    python_exe = aios_env / "bin" / "python"
    
    test_code = """
import aios
from aios.object import Object
from aios.state import State

print(f"✅ AIOS {aios.__version__} imported successfully")
print(f"✅ Object class: {Object}")
print(f"✅ State class: {State}")

# Test basic functionality
obj = Object()
state = State(['idle', 'working'], name='test', default='idle')
print(f"✅ Object created: {obj}")
print(f"✅ State created: {state}")
print(f"✅ Current state: {state.current_state}")

print("🎉 AIOS installation test PASSED!")
"""
    
    try:
        result = subprocess.run([str(python_exe), "-c", test_code], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ AIOS installation test passed!")
            print(result.stdout)
        else:
            print(f"❌ AIOS installation test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error testing AIOS: {e}")
        return False
    
    # Step 6: Clean up
    print("\n🧹 Step 6: Cleaning up...")
    try:
        shutil.rmtree(aios_repo)
        print("✅ Temporary AIOS repository removed")
    except Exception as e:
        print(f"⚠️ Warning: Could not remove temp repo: {e}")
    
    print("\n🎉 AIOS Installation Fixed Successfully!")
    return True

def main():
    """Main function"""
    print("🔧 AIOS Installation Fixer")
    print("=" * 40)
    
    success = fix_aios_installation()
    
    if success:
        print("\n🚀 AIOS is now properly installed!")
        print("You can now run the AIOS Builder Agent.")
    else:
        print("\n💥 AIOS installation fix failed!")
        print("Check the logs above for details.")

if __name__ == "__main__":
    main()
