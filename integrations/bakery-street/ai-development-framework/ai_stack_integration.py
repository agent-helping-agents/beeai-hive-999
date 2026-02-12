#!/usr/bin/env python3
"""
AI Development Stack Integration Script - Part 1
Integrates comprehensive AI tools and frameworks into AIOS project
"""

import subprocess
import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple

class AIStackIntegrator:
    def __init__(self):
        self.project_root = Path("/home/booze/ai-development")
        self.ai_stack_dir = self.project_root / "ai-stack"
        self.repositories = {
            "parrotos-practical-guide": {
                "url": "https://github.com/HassanNetSec/parrotos-practical-guide.git",
                "description": "Parrot OS cybersecurity and ethical hacking guide",
                "type": "guide",
                "install_method": "clone_only"
            },
            "aiostreams": {
                "url": "https://github.com/Viren070/AIOStreams.git",
                "description": "Stremio super-addon for streaming aggregation",
                "type": "media",
                "install_method": "docker"
            },
            "system-prompts-and-models": {
                "url": "https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools.git",
                "description": "20,000+ lines of system prompts and AI models",
                "type": "ai_resources",
                "install_method": "clone_only"
            },
            "db-gpt": {
                "url": "https://github.com/eosphoros-ai/DB-GPT.git",
                "description": "AI-native framework for data app development",
                "type": "ai_framework",
                "install_method": "pip_install"
            },
            "yao": {
                "url": "https://github.com/YaoApp/yao.git",
                "description": "All-in-one engine for building web apps with AI",
                "type": "web_framework",
                "install_method": "binary_download"
            },
            "promptic": {
                "url": "https://github.com/knowsuchagency/promptic.git",
                "description": "Python library for LLM app development",
                "type": "ai_library",
                "install_method": "pip_install"
            },
            "next-money": {
                "url": "https://github.com/virgoone/next-money.git",
                "description": "Flux AI image generator SaaS starter",
                "type": "web_app",
                "install_method": "node_install"
            },
            "transformers": {
                "url": "https://github.com/huggingface/transformers.git",
                "description": "Core library for NLP and multimodal models",
                "type": "ai_library",
                "install_method": "pip_install"
            },
            "langchain": {
                "url": "https://github.com/langchain-ai/langchain.git",
                "description": "Framework for building LLM apps with chains and agents",
                "type": "ai_framework",
                "install_method": "pip_install"
            },
            "autogen": {
                "url": "https://github.com/microsoft/autogen.git",
                "description": "Multi-agent framework for conversational AI",
                "type": "ai_framework",
                "install_method": "pip_install"
            },
            "deepspeed": {
                "url": "https://github.com/microsoft/DeepSpeed.git",
                "description": "Optimization library for large model training",
                "type": "ai_library",
                "install_method": "pip_install"
            },
            "dvc": {
                "url": "https://github.com/iterative/dvc.git",
                "description": "Data version control for datasets and pipelines",
                "type": "data_tools",
                "install_method": "pip_install"
            },
            "mlflow": {
                "url": "https://github.com/mlflow/mlflow.git",
                "description": "MLOps platform for experiment tracking and deployment",
                "type": "mlops",
                "install_method": "pip_install"
            },
            "bentoml": {
                "url": "https://github.com/bentoml/BentoML.git",
                "description": "Packaging and deploying models as APIs/microservices",
                "type": "deployment",
                "install_method": "pip_install"
            }
        }
        
    def setup_environment(self):
        """Set up the AI stack environment"""
        print("🚀 Setting up AI Development Stack Environment...")
        
        # Create AI stack directory
        self.ai_stack_dir.mkdir(exist_ok=True)
        print(f"✅ Created AI stack directory: {self.ai_stack_dir}")
        
        # Create subdirectories for different types
        for repo_type in ["ai_framework", "ai_library", "data_tools", "mlops", "deployment", "web_framework", "web_app", "ai_resources", "guide", "media"]:
            (self.ai_stack_dir / repo_type).mkdir(exist_ok=True)
        
        print("✅ Created organized directory structure")
        
    def install_system_dependencies(self):
        """Install system-level dependencies"""
        print("\n🔧 Installing system dependencies...")
        
        dependencies = [
            "git", "docker.io", "nodejs", "npm", "golang-go", "python3-pip",
            "python3-venv", "build-essential", "curl", "wget"
        ]
        
        for dep in dependencies:
            try:
                print(f"Installing {dep}...")
                result = subprocess.run(["sudo", "apt", "install", "-y", dep], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {dep} installed")
                else:
                    print(f"⚠️ {dep} installation had issues")
            except Exception as e:
                print(f"❌ Failed to install {dep}: {e}")
        
        # Start Docker service
        try:
            subprocess.run(["sudo", "systemctl", "start", "docker"], 
                          capture_output=True, text=True)
            subprocess.run(["sudo", "systemctl", "enable", "docker"], 
                          capture_output=True, text=True)
            print("✅ Docker service started and enabled")
        except Exception as e:
            print(f"⚠️ Docker service setup had issues: {e}")

# Main execution for Part 1
if __name__ == "__main__":
    print("🧠 AI Stack Integration - Part 1: Environment Setup")
    print("=" * 50)
    
    integrator = AIStackIntegrator()
    
    # Run Part 1 setup
    integrator.setup_environment()
    integrator.install_system_dependencies()
    
    print("\n✅ Part 1 Complete: Environment and Dependencies")
    print("🚀 Ready for Part 2: Repository Cloning")
