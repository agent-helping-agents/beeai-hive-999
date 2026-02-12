#!/bin/bash
# Poly-AI Framework Setup Script

set -e

echo "🚀 Poly-AI Framework Setup"
echo "=========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check if Python 3.8+ is installed
check_python() {
    print_header "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        print_status "Python $PYTHON_VERSION found"
        
        # Check if version is 3.8 or higher
        if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
            print_status "Python version is compatible"
        else
            print_error "Python 3.8 or higher is required"
            exit 1
        fi
    else
        print_error "Python 3 is not installed"
        exit 1
    fi
}

# Create virtual environment
create_venv() {
    print_header "Creating virtual environment..."
    
    if [ ! -d "poly_env" ]; then
        python3 -m venv poly_env
        print_status "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source poly_env/bin/activate
    print_status "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    print_header "Installing dependencies..."
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    if [ -f "requirements_poly.txt" ]; then
        pip install -r requirements_poly.txt
        print_status "Dependencies installed successfully"
    else
        print_error "requirements_poly.txt not found"
        exit 1
    fi
}

# Setup configuration
setup_config() {
    print_header "Setting up configuration..."
    
    if [ ! -f "poly_config.yaml" ]; then
        print_status "Creating default configuration file..."
        python3 -c "
from poly_framework import PolyAIFramework
framework = PolyAIFramework()
framework.create_config_file('poly_config.yaml')
print('Configuration file created')
"
    else
        print_warning "Configuration file already exists"
    fi
    
    # Check for environment variables
    print_status "Checking environment variables..."
    
    if [ -z "$GITHUB_TOKEN" ]; then
        print_warning "GITHUB_TOKEN not set"
        echo "Please set your GitHub token:"
        echo "export GITHUB_TOKEN='your_github_token_here'"
    else
        print_status "GITHUB_TOKEN is set"
    fi
    
    if [ -z "$PERPLEXITY_API_KEY" ]; then
        print_warning "PERPLEXITY_API_KEY not set (optional for AI features)"
        echo "To enable AI features, set:"
        echo "export PERPLEXITY_API_KEY='your_perplexity_key_here'"
    else
        print_status "PERPLEXITY_API_KEY is set"
    fi
}

# Run tests
run_tests() {
    print_header "Running tests..."
    
    if [ -f "tests/test_poly_framework.py" ]; then
        python3 -m pytest tests/test_poly_framework.py -v
        print_status "Tests completed"
    else
        print_warning "Test file not found, skipping tests"
    fi
}

# Create example scripts
create_examples() {
    print_header "Creating example scripts..."
    
    # Make example scripts executable
    chmod +x examples/*.py 2>/dev/null || true
    
    print_status "Example scripts ready"
}

# Setup CLI
setup_cli() {
    print_header "Setting up CLI..."
    
    if [ -f "poly_cli.py" ]; then
        chmod +x poly_cli.py
        print_status "CLI setup complete"
        
        # Create symlink for easy access
        if [ ! -L "/usr/local/bin/poly-ai" ]; then
            echo "To make poly-ai command available globally, run:"
            echo "sudo ln -s $(pwd)/poly_cli.py /usr/local/bin/poly-ai"
        fi
    else
        print_warning "CLI script not found"
    fi
}

# Main setup function
main() {
    print_header "Starting Poly-AI Framework setup..."
    
    check_python
    create_venv
    install_dependencies
    setup_config
    run_tests
    create_examples
    setup_cli
    
    print_header "Setup completed successfully!"
    echo ""
    print_status "Next steps:"
    echo "1. Set your environment variables:"
    echo "   export GITHUB_TOKEN='your_github_token'"
    echo "   export PERPLEXITY_API_KEY='your_perplexity_key' (optional)"
    echo ""
    echo "2. Activate the virtual environment:"
    echo "   source poly_env/bin/activate"
    echo ""
    echo "3. Run the framework:"
    echo "   python3 poly_framework.py"
    echo "   or"
    echo "   python3 poly_cli.py --help"
    echo ""
    echo "4. Try the examples:"
    echo "   python3 examples/advanced_usage.py"
    echo ""
    print_status "Poly-AI Framework is ready to use! 🎉"
}

# Run main function
main "$@"
