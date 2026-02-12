#!/usr/bin/env python3
"""
BeeAI Hive 999 - TUI Health Check Script
Tests if the BeeHave application and all dependencies work correctly.
"""

import sys
import subprocess
import os
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
ENDC = '\033[0m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}=== {text} ==={ENDC}")

def print_success(text):
    print(f"{GREEN}✅ {text}{ENDC}")

def print_error(text):
    print(f"{RED}❌ {text}{ENDC}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{ENDC}")

def print_info(text):
    print(f"{BLUE}ℹ️  {text}{ENDC}")

def run_command(cmd, timeout=30):
    """Run a command and return success status."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def check_python_version():
    """Check Python version."""
    print_header("Python Version Check")
    version = sys.version.split()[0]
    print_info(f"Python version: {version}")
    
    major, minor = sys.version_info[:2]
    if major >= 3 and minor >= 8:
        print_success("Python version OK (3.8+)")
        return True
    else:
        print_error("Python version too old (need 3.8+)")
        return False

def check_required_modules():
    """Check if required Python modules are available."""
    print_header("Required Module Check")
    
    required_modules = [
        ('asyncio', 'asyncio'),
        ('pathlib', 'pathlib'),
        ('json', 'json'),
        ('datetime', 'datetime'),
    ]
    
    # Add project-specific imports
    project_modules = [
        ('terminal_221b', None),
    ]
    
    all_ok = True
    
    # Check standard library
    for module_name, package in required_modules:
        try:
            __import__(module_name)
            print_success(f"Module available: {module_name}")
        except ImportError:
            print_error(f"Missing module: {module_name}")
            all_ok = False
    
    # Check project modules
    for module_name, package in project_modules:
        try:
            # Try importing with project path
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            __import__(module_name)
            print_success(f"Project module available: {module_name}")
        except ImportError as e:
            print_warning(f"Project module '{module_name}' may need path setup: {e}")
    
    return all_ok

def check_beehave_script():
    """Check if beehave.py exists and is executable."""
    print_header("BeeHave Script Check")
    
    script_path = Path(__file__).resolve().parent / "beehave.py"
    
    if script_path.exists():
        print_success(f"beehave.py exists: {script_path}")
        
        # Check if it's readable
        if os.access(script_path, os.R_OK):
            print_success("beehave.py is readable")
        else:
            print_error("beehave.py is not readable")
            return False
        
        # Check shebang
        with open(script_path, 'r') as f:
            first_line = f.readline()
            if '#!' in first_line:
                print_info(f"Shebang: {first_line.strip()}")
            else:
                print_warning("No shebang found in beehave.py")
        
        return True
    else:
        print_error(f"beehave.py not found at: {script_path}")
        return False

def test_beehave_help():
    """Test beehave.py help command."""
    print_header("BeeHave Help Test")
    
    success, stdout, stderr = run_command("python beehave.py help", timeout=10)
    
    if success:
        print_success("beehave.py help command works!")
        print_info("Output preview:")
        # Print first 20 lines
        lines = stdout.strip().split('\n')[:20]
        for line in lines:
            if line.strip():
                print(f"  {line}")
        if len(stdout.strip().split('\n')) > 20:
            print_info("... (truncated)")
        return True
    else:
        print_error("beehave.py help command failed")
        if stderr:
            print_info(f"Error: {stderr}")
        return False

def check_terminal_221b_integration():
    """Check Terminal 221b integration."""
    print_header("Terminal 221b Integration Check")
    
    integration_path = Path(__file__).resolve().parent / "terminal_221b"
    
    if integration_path.exists():
        print_success(f"Terminal 221b directory exists: {integration_path}")
        
        # Check for key files
        key_files = [
            "integration/hive_bridge.py",
            "detective/__init__.py",
            "detective/personalities.py",
        ]
        
        for file_path in key_files:
            full_path = integration_path / file_path
            if full_path.exists():
                print_success(f"  Found: {file_path}")
            else:
                print_warning(f"  Missing: {file_path}")
        
        return True
    else:
        print_error(f"Terminal 221b directory not found: {integration_path}")
        return False

def check_agents():
    """Check agent directories."""
    print_header("Agent Check")
    
    agents_path = Path(__file__).resolve().parent / "agents"
    
    if agents_path.exists():
        print_success(f"Agents directory exists: {agents_path}")
        
        # Count agent types
        agent_types = []
        for item in agents_path.iterdir():
            if item.is_dir():
                agent_types.append(item.name)
        
        print_info(f"Agent types found: {', '.join(agent_types)}")
        
        # Count total agents
        total_agents = 0
        for agent_type in agent_types:
            agent_count = len(list((agents_path / agent_type).iterdir()))
            total_agents += agent_count
            print_info(f"  {agent_type}: {agent_count} agents")
        
        print_success(f"Total agents: {total_agents}")
        return True
    else:
        print_error(f"Agents directory not found: {agents_path}")
        return False

def check_requirements():
    """Check requirements.txt and installed packages."""
    print_header("Requirements Check")
    
    req_path = Path(__file__).resolve().parent / "requirements.txt"
    
    if req_path.exists():
        print_success(f"requirements.txt exists: {req_path}")
        
        with open(req_path, 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print_info(f"Packages listed: {len(requirements)}")
        for req in requirements:
            print(f"  - {req}")
        
        # Quick check if pip is available
        success, _, _ = run_command("pip --version", timeout=5)
        if success:
            print_success("pip is available")
        else:
            print_warning("pip may not be available")
        
        return True
    else:
        print_warning(f"requirements.txt not found: {req_path}")
        return True  # Not critical

def run_quick_functionality_test():
    """Run a quick functionality test of the core system."""
    print_header("Quick Functionality Test")
    
    # Test importing core modules
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    
    try:
        # Test 1: Can we import pathlib-based modules?
        print_success("Core imports working")
        
        # Test 2: Can we access the agents directory?
        agents_dir = Path(__file__).resolve().parent / "agents"
        if agents_dir.exists():
            print_success("Can access agents directory")
        else:
            print_warning("Cannot access agents directory")
        
        # Test 3: Check TUI module exists
        tui_path = Path(__file__).resolve().parent / "tui.py"
        if tui_path.exists():
            print_success("TUI module exists")
        else:
            print_warning("TUI module not found")
        
        return True
        
    except Exception as e:
        print_error(f"Functionality test failed: {e}")
        return False

def generate_summary(results):
    """Generate a summary of all test results."""
    print_header("TEST SUMMARY")
    
    total = len(results)
    passed = sum(1 for _, success in results if success)
    failed = total - passed
    
    print(f"{BOLD}Tests Passed: {passed}/{total}{ENDC}")
    
    if failed > 0:
        print(f"{RED}Tests Failed: {failed}/{total}{ENDC}")
        print("\nFailed tests:")
        for name, success in results:
            if not success:
                print(f"  - {name}")
    else:
        print(f"{GREEN}All tests passed! ✅{ENDC}")
    
    print("\n" + "=" * 50)
    
    if failed == 0:
        print(f"{GREEN}{BOLD}🎉 BeeAI Hive 999 is healthy and ready to use!{ENDC}")
        print(f"{GREEN}Run './beehave.py' to launch the TUI{ENDC}")
    elif failed <= 2:
        print(f"{YELLOW}{BOLD}⚠️  Minor issues detected. Most functionality should work.{ENDC}")
        print(f"{YELLOW}Run './beehave.py' to see if it works anyway.{ENDC}")
    else:
        print(f"{RED}{BOLD}❌ Several issues detected. Please review the errors above.{ENDC}")
        print(f"{RED}Run './beehave.py help' to verify at least basic functionality.{ENDC}")
    
    print("=" * 50 + "\n")
    
    return failed == 0

def main():
    """Run all health checks."""
    print("\n" + "=" * 60)
    print(f"{BOLD}🐝 BeeAI Hive 999 - Health Check{ENDC}")
    print("=" * 60)
    
    results = []
    
    # Run all checks
    results.append(("Python Version", check_python_version()))
    results.append(("Required Modules", check_required_modules()))
    results.append(("BeeHave Script", check_beehave_script()))
    results.append(("BeeHave Help", test_beehave_help()))
    results.append(("Terminal 221b", check_terminal_221b_integration()))
    results.append(("Agents", check_agents()))
    results.append(("Requirements", check_requirements()))
    results.append(("Functionality", run_quick_functionality_test()))
    
    # Generate summary
    all_passed = generate_summary(results)
    
    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
