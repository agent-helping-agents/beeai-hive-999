#!/bin/bash
# NeoSpiral AI Tools Menu System

show_menu() {
    echo "🧠 === NeoSpiral AI Development Tools ==="
    echo "1) OpenCode (Terminal AI Assistant)"
    echo "2) Cursor IDE (AI-Powered Code Editor)"  
    echo "3) Aider (AI Pair Programmer)"
    echo "4) Ollama Models (Local LLMs)"
    echo "5) Mathematical Tools Demo"
    echo "6) Environment Status"
    echo "7) Research Tools"
    echo "8) Exit"
    echo "=================================="
}

activate_ai_env() {
    source ~/ai-development/environments/ai-main/bin/activate
    export OPENAI_API_KEY="${OPENAI_API_KEY:-}"
    export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-}"
}

while true; do
    show_menu
    read -p "Select option (1-8): " choice
    
    case $choice in
        1)
            echo "🤖 Starting OpenCode..."
            cd ~/ai-development
            opencode
            ;;
        2)
            echo "📝 Starting Cursor IDE..."
            cursor ~/ai-development &
            ;;
        3)
            echo "👥 Starting Aider..."
            cd ~/ai-development
            activate_ai_env
            aider
            ;;
        4)
            echo "🧬 Ollama Models:"
            ollama list
            echo ""
            echo "Available commands:"
            echo "  ollama run codellama:7b"
            echo "  ollama run deepseek-coder:6.7b"
            read -p "Press Enter to continue..."
            ;;
        5)
            echo "📊 Running Mathematical Tools Demo..."
            cd ~/ai-development
            activate_ai_env
            echo "Running Shannon entropy analysis..."
            python tools/shannon_entropy.py
            echo ""
            echo "Running STDP learning demo..."
            python tools/stdp_learning.py
            echo ""
            echo "Running spiral network analysis..."
            python tools/spiral_network.py
            read -p "Press Enter to continue..."
            ;;
        6)
            echo "📋 Environment Status:"
            echo "✓ OpenCode: $(opencode --version)"
            echo "✓ Aider: $(aider --version)"
            echo "✓ Cursor: $(cursor --version 2>/dev/null || echo 'Installing...')"
            echo "✓ Ollama: $(ollama list | wc -l) models installed"
            echo "✓ GitHub: $(gh auth status --hostname github.com | grep 'Logged in' || echo 'Not authenticated')"
            echo "✓ Python envs: $(ls ~/ai-development/environments/ 2>/dev/null | wc -l) environments"
            read -p "Press Enter to continue..."
            ;;
        7)
            echo "🔬 Research Tools:"
            echo "Available research scripts:"
            ls ~/ai-development/tools/
            echo ""
            echo "Research directories:"
            ls ~/ai-development/research/ 2>/dev/null || echo "(empty)"
            read -p "Press Enter to continue..."
            ;;
        8)
            echo "Goodbye! 🚀"
            break
            ;;
        *)
            echo "Invalid option. Please select 1-8."
            ;;
    esac
    echo ""
done
