#!/usr/bin/env python3
"""
Master AI Stack Integration Script
Runs all parts of the AI stack integration
"""

import subprocess
import sys
from pathlib import Path

def run_part(part_name, script_path):
    """Run a specific part of the integration"""
    print(f"\n🚀 Running {part_name}...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {part_name} completed successfully")
            return True
        else:
            print(f"❌ {part_name} failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running {part_name}: {e}")
        return False

def main():
    """Run the complete AI stack integration"""
    print("🧠 Master AI Stack Integration")
    print("=" * 50)
    
    # Get script directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Define parts
    parts = [
        ("Part 1: Environment Setup", project_root / "ai_stack_integration.py"),
        ("Part 2: Repository Cloning", project_root / "ai_stack_part2.py"),
        ("Part 3: Integration Configuration", project_root / "ai_stack_part3.py")
    ]
    
    # Run each part
    success_count = 0
    for part_name, script_path in parts:
        if script_path.exists():
            if run_part(part_name, script_path):
                success_count += 1
        else:
            print(f"⚠️ {part_name} script not found: {script_path}")
    
    # Summary
    print("\n" + "=" * 50)
    print(f"🎯 Integration Summary: {success_count}/{len(parts)} parts completed")
    
    if success_count == len(parts):
        print("🎉 All parts completed successfully!")
        print("🚀 Your AI Development Stack is ready!")
        print("\nNext steps:")
        print("1. Test integration: python ai-stack/integrate_with_aios.py")
        print("2. Start building with AIOS!")
    else:
        print("⚠️ Some parts failed. Check the logs above.")
        print("💡 You can run individual parts manually.")

if __name__ == "__main__":
    main()
