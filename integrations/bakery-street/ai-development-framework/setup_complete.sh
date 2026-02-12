#!/usr/bin/env bash
# Complete NeoSpiral AI Framework for Parrot OS
set -euo pipefail

echo "=== Setting up complete AI development environment ==="

# Create virtual environments
cd ~/ai-development
python3 -m venv environments/ai-main
python3 -m venv environments/neuromorphic
python3 -m venv environments/research

# Install in main environment
source environments/ai-main/bin/activate
pip install --upgrade pip
pip install gpt4all transformers torch jupyterlab aider-chat

# Install in neuromorphic environment  
source environments/neuromorphic/bin/activate
pip install brian2 snntorch lava-nc nengo qiskit pennylane

# Install research tools
source environments/research/bin/activate
pip install datasets arxiv scholarly matplotlib seaborn

echo "Setup complete! Use 'source ~/ai-development/environments/ai-main/bin/activate' to start"
