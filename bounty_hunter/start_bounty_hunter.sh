#!/bin/bash
# Bounty Hunter - Startup Script
# Quick startup script for the Bounty Hunter automation system.

# Colors for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored text
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Python is available
check_python() {
    if command -v python3 >/dev/null 2>&1; then
        PYTHON=python3
        return 0
    elif command -v python >/dev/null 2>&1; then
        PYTHON=python
        return 0
    else
        print_error "Python 3 or higher not found"
        echo "Please install Python 3.8 or higher"
        return 1
    fi
}

# Function to check if required files exist
check_files() {
    local files=("bounty_hunter_todo.py" "bounty_hunter_todo.json" "bounty_hunter_checklist.json")
    
    for file in "${files[@]}"; do
        if [ ! -f "$file" ]; then
            print_error "File not found: $file"
            if [ "$file" = "bounty_hunter_todo.json" ] || [ "$file" = "bounty_hunter_checklist.json" ]; then
                print_warning "Note: These files will be created automatically when the script is run"
            else
                return 1
            fi
        fi
    done
    
    return 0
}

# Function to check script permissions
check_permissions() {
    if [ ! -x "bounty_hunter_todo.py" ]; then
        print_info "Making script executable..."
        chmod +x "bounty_hunter_todo.py"
        if [ $? -ne 0 ]; then
            print_error "Failed to make script executable"
            return 1
        fi
    fi
    
    return 0
}

# Function to run system checks
run_system_checks() {
    print_info "Running system checks..."
    
    # Check Python installation
    check_python
    if [ $? -ne 0 ]; then
        return 1
    fi
    
    # Check files
    check_files
    if [ $? -ne 0 ]; then
        return 1
    fi
    
    # Check permissions
    check_permissions
    if [ $? -ne 0 ]; then
        return 1
    fi
    
    print_info "System checks passed"
    return 0
}

# Function to start the bounty hunter system
start_system() {
    print_info "Starting Bounty Hunter automation system..."
    
    # Run the Python script
    $PYTHON "bounty_hunter_todo.py"
    
    # Check exit status
    if [ $? -ne 0 ]; then
        print_error "Bounty Hunter system exited with error"
        return 1
    fi
    
    return 0
}

# Main function
main() {
    # Check current directory
    if [ ! -f "bounty_hunter_todo.py" ]; then
        print_error "Bounty Hunter files not found in current directory"
        print_warning "Please navigate to the directory containing the bounty hunter files"
        return 1
    fi
    
    # Run system checks
    run_system_checks
    if [ $? -ne 0 ]; then
        print_error "System checks failed. Cannot start Bounty Hunter system."
        return 1
    fi
    
    # Start the system
    start_system
    if [ $? -ne 0 ]; then
        print_error "Failed to start Bounty Hunter system"
        return 1
    fi
    
    return 0
}

# Display header
echo "========================================"
echo "BOUNTY HUNTER - AUTOMATION SYSTEM"
echo "========================================"
echo ""

# Run main function
main

# Exit with appropriate code
exit $?
