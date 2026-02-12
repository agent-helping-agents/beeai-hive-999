#!/bin/bash

# AIOS Launcher Script
# Provides easy access to AIOS with menu-driven interface

# Colors for better UI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# AIOS Environment Path
AIOS_ENV="/home/booze/ai-development/environments/aios-env"

# Function to show banner
show_banner() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🧠 AIOS Launcher 🧠                      ║"
    echo "║              AGI Research - Agent Orchestration             ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Function to check if AIOS environment exists
check_aios_env() {
    if [ ! -d "$AIOS_ENV" ]; then
        echo -e "${RED}❌ AIOS environment not found at: $AIOS_ENV${NC}"
        echo -e "${YELLOW}Please ensure AIOS is properly installed.${NC}"
        exit 1
    fi
}

# Function to activate AIOS environment
activate_aios() {
    echo -e "${GREEN}🔧 Activating AIOS environment...${NC}"
    source "$AIOS_ENV/bin/activate"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ AIOS environment activated successfully!${NC}"
        echo -e "${BLUE}Current Python: $(which python)${NC}"
        echo -e "${BLUE}AIOS Version: $(python -c 'import aios; print(aios.__version__)' 2>/dev/null || echo 'Version info not available')${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to activate AIOS environment${NC}"
        return 1
    fi
}

# Function to show main menu
show_main_menu() {
    echo -e "${YELLOW}📋 Available Options:${NC}"
    echo ""
    echo -e "${GREEN}1.${NC} 🚀 Launch AIOS Interactive Shell"
    echo -e "${GREEN}2.${NC} 🐍 Start Python with AIOS Loaded"
    echo -e "${GREEN}3.${NC} 📚 Show AIOS Documentation/Help"
    echo -e "${GREEN}4.${NC} 🔧 Check AIOS Installation Status"
    echo -e "${GREEN}5.${NC} 📦 Install/Update AIOS Packages"
    echo -e "${GREEN}6.${NC} 🧪 Run AIOS Quick Test"
    echo -e "${GREEN}7.${NC} 🗂️  Open AIOS Project Directory"
    echo -e "${GREEN}8.${NC} 🆘 Troubleshooting & Support"
    echo -e "${GREEN}9.${NC} 🚪 Exit"
    echo ""
}

# Function to handle menu selection
handle_menu_selection() {
    local choice
    read -p "Enter your choice (1-9): " choice
    
    case $choice in
        1)
            echo -e "${CYAN}🚀 Launching AIOS Interactive Shell...${NC}"
            if activate_aios; then
                echo -e "${GREEN}✅ AIOS is now active! You can start coding with AIOS.${NC}"
                echo -e "${YELLOW}Type 'exit()' to return to the launcher.${NC}"
                echo ""
                python
                deactivate
            fi
            ;;
        2)
            echo -e "${CYAN}🐍 Starting Python with AIOS pre-loaded...${NC}"
            if activate_aios; then
                echo -e "${GREEN}✅ Starting Python with AIOS modules loaded...${NC}"
                python -c "
import aios
import cerebrum
print('✅ AIOS and Cerebrum successfully imported!')
print('🧠 AIOS Version:', getattr(aios, '__version__', 'Unknown'))
print('🧠 Cerebrum Version:', getattr(cerebrum, '__version__', 'Unknown'))
print('\\n🚀 Ready for AIOS development!')
"
                deactivate
            fi
            ;;
        3)
            echo -e "${CYAN}📚 AIOS Documentation & Help${NC}"
            echo ""
            echo -e "${BLUE}📖 Official Resources:${NC}"
            echo "   • GitHub: https://github.com/agiresearch/AIOS"
            echo "   • Cerebrum SDK: https://github.com/agiresearch/Cerebrum"
            echo ""
            echo -e "${BLUE}🔧 Local Help:${NC}"
            if activate_aios; then
                echo "   • Python help: help(aios)"
                echo "   • Cerebrum help: help(cerebrum)"
                python -c "
try:
    import aios
    print('\\n📋 AIOS Module Info:')
    print('   • Available attributes:', [attr for attr in dir(aios) if not attr.startswith('_')])
except Exception as e:
    print('❌ Error:', e)
"
                deactivate
            fi
            ;;
        4)
            echo -e "${CYAN}🔧 AIOS Installation Status Check${NC}"
            echo ""
            check_installation_status
            ;;
        5)
            echo -e "${CYAN}📦 AIOS Package Management${NC}"
            if activate_aios; then
                echo -e "${GREEN}✅ AIOS environment activated for package management${NC}"
                echo ""
                echo -e "${YELLOW}Available commands:${NC}"
                echo "   • pip list - Show installed packages"
                echo "   • pip install --upgrade aios - Update AIOS"
                echo "   • pip install --upgrade cerebrum - Update Cerebrum"
                echo ""
                read -p "Press Enter to continue..."
                deactivate
            fi
            ;;
        6)
            echo -e "${CYAN}🧪 Running AIOS Quick Test${NC}"
            run_aios_test
            ;;
        7)
            echo -e "${CYAN}🗂️  Opening AIOS Project Directory${NC}"
            if command -v xdg-open >/dev/null 2>&1; then
                xdg-open "/home/booze/ai-development"
            else
                echo -e "${YELLOW}Opening directory in terminal...${NC}"
                cd /home/booze/ai-development
                echo -e "${GREEN}✅ Current directory: $(pwd)${NC}"
                ls -la
            fi
            ;;
        8)
            echo -e "${CYAN}🆘 Troubleshooting & Support${NC}"
            show_troubleshooting
            ;;
        9)
            echo -e "${GREEN}👋 Thank you for using AIOS Launcher!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Invalid choice. Please enter a number between 1-9.${NC}"
            ;;
    esac
}

# Function to check installation status
check_installation_status() {
    echo -e "${BLUE}🔍 Checking AIOS Installation...${NC}"
    echo ""
    
    # Check environment
    if [ -d "$AIOS_ENV" ]; then
        echo -e "${GREEN}✅ AIOS Environment: $AIOS_ENV${NC}"
    else
        echo -e "${RED}❌ AIOS Environment: Not found${NC}"
    fi
    
    # Check Python version
    if command -v python3 >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Python: $(python3 --version)${NC}"
    else
        echo -e "${RED}❌ Python: Not found${NC}"
    fi
    
    # Check GPU
    if command -v nvidia-smi >/dev/null 2>&1; then
        echo -e "${GREEN}✅ NVIDIA GPU: Available${NC}"
        nvidia-smi --query-gpu=name,driver_version --format=csv,noheader,nounits 2>/dev/null | head -1
    else
        echo -e "${YELLOW}⚠️  NVIDIA GPU: Not detected${NC}"
    fi
    
    # Check Ollama
    if command -v ollama >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Ollama: Available${NC}"
    else
        echo -e "${YELLOW}⚠️  Ollama: Not installed${NC}"
    fi
    
    echo ""
    read -p "Press Enter to continue..."
}

# Function to run AIOS test
run_aios_test() {
    echo -e "${CYAN}🧪 Running AIOS Quick Test...${NC}"
    echo ""
    
    if activate_aios; then
        echo -e "${GREEN}✅ Environment activated, running tests...${NC}"
        
        # Test 1: Import test
        echo -e "${BLUE}📦 Test 1: Import Test${NC}"
        python -c "
try:
    import aios
    print('   ✅ AIOS import successful')
except ImportError as e:
    print('   ❌ AIOS import failed:', e)

try:
    import cerebrum
    print('   ✅ Cerebrum import successful')
except ImportError as e:
    print('   ❌ Cerebrum import failed:', e)
"
        
        # Test 2: Version test
        echo -e "${BLUE}📋 Test 2: Version Test${NC}"
        python -c "
try:
    import aios
    version = getattr(aios, '__version__', 'Unknown')
    print('   ✅ AIOS version:', version)
except Exception as e:
    print('   ❌ AIOS version check failed:', e)

try:
    import cerebrum
    version = getattr(cerebrum, '__version__', 'Unknown')
    print('   ✅ Cerebrum version:', version)
except Exception as e:
    print('   ❌ Cerebrum version check failed:', e)
"
        
        # Test 3: Basic functionality test
        echo -e "${BLUE}⚙️  Test 3: Basic Functionality${NC}"
        python -c "
try:
    import aios
    import cerebrum
    
    # Check if modules have any content
    aios_attrs = [attr for attr in dir(aios) if not attr.startswith('_')]
    cerebrum_attrs = [attr for attr in dir(cerebrum) if not attr.startswith('_')]
    
    print('   ✅ AIOS attributes found:', len(aios_attrs))
    print('   ✅ Cerebrum attributes found:', len(cerebrum_attrs))
    
    if aios_attrs:
        print('   📋 Sample AIOS attributes:', aios_attrs[:5])
    if cerebrum_attrs:
        print('   📋 Sample Cerebrum attributes:', cerebrum_attrs[:5])
        
except Exception as e:
    print('   ❌ Functionality test failed:', e)
"
        
        echo -e "${GREEN}✅ AIOS Quick Test completed!${NC}"
        deactivate
    else
        echo -e "${RED}❌ Failed to activate environment for testing${NC}"
    fi
    
    echo ""
    read -p "Press Enter to continue..."
}

# Function to show troubleshooting
show_troubleshooting() {
    echo -e "${CYAN}🆘 AIOS Troubleshooting Guide${NC}"
    echo ""
    echo -e "${BLUE}🔧 Common Issues & Solutions:${NC}"
    echo ""
    echo -e "${YELLOW}1. Virtual Environment Issues:${NC}"
    echo "   • Ensure you're in the correct directory"
    echo "   • Check if environment exists: ls -la environments/aios-env/"
    echo "   • Recreate if corrupted: python3 -m venv environments/aios-env/"
    echo ""
    echo -e "${YELLOW}2. Import Errors:${NC}"
    echo "   • Activate environment: source environments/aios-env/bin/activate"
    echo "   • Check installed packages: pip list"
    echo "   • Reinstall if needed: pip install --force-reinstall aios cerebrum"
    echo ""
    echo -e "${YELLOW}3. GPU Issues:${NC}"
    echo "   • Check NVIDIA drivers: nvidia-smi"
    echo "   • Verify CUDA installation"
    echo "   • Check PyTorch GPU support if using ML features"
    echo ""
    echo -e "${BLUE}📞 Support Resources:${NC}"
    echo "   • GitHub Issues: https://github.com/agiresearch/AIOS/issues"
    echo "   • Community: Check AIOS Foundation website"
    echo "   • Local logs: Check ~/.aios/ directory if it exists"
    echo ""
    read -p "Press Enter to continue..."
}

# Main execution
main() {
    show_banner
    check_aios_env
    
    while true; do
        show_main_menu
        handle_menu_selection
        echo ""
        read -p "Press Enter to return to main menu..."
        show_banner
    done
}

# Run main function
main
