#!/usr/bin/env python3
"""
AI Development Stack Integration Script - Part 2
Repository cloning and Python package installation
"""

import subprocess
import sys
from pathlib import Path

class AIStackPart2:
    def __init__(self):
        self.project_root = Path("/home/booze/ai-development")
        self.ai_stack_dir = self.project_root / "ai-stack"
        
    def clone_repositories(self):
        """Clone all AI development repositories"""
        print("\n📥 Cloning AI development repositories...")
        
        repositories = {
            "parrotos-practical-guide": {
                "url": "https://github.com/HassanNetSec/parrotos-practical-guide.git",
                "type": "guide"
            },
            "aiostreams": {
                "url": "https://github.com/Viren070/AIOStreams.git",
                "type": "media"
            },
            "system-prompts-and-models": {
                "url": "https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools.git",
                "type": "ai_resources"
            },
            "db-gpt": {
                "url": "https://github.com/eosphoros-ai/DB-GPT.git",
                "type": "ai_framework"
            },
            "yao": {
                "url": "https://github.com/YaoApp/yao.git",
                "type": "web_framework"
            },
            "promptic": {
                "url": "https://github.com/knowsuchagency/promptic.git",
                "type": "ai_library"
            },
            "next-money": {
                "url": "https://github.com/virgoone/next-money.git",
                "type": "web_app"
            },
            "transformers": {
                "url": "https://github.com/huggingface/transformers.git",
                "type": "ai_library"
            },
            "langchain": {
                "url": "https://github.com/langchain-ai/langchain.git",
                "type": "ai_framework"
            },
            "autogen": {
                "url": "https://github.com/microsoft/autogen.git",
                "type": "ai_framework"
            },
            "deepspeed": {
                "url": "https://github.com/microsoft/DeepSpeed.git",
                "type": "ai_library"
            },
            "dvc": {
                "url": "https://github.com/iterative/dvc.git",
                "type": "data_tools"
            },
            "mlflow": {
                "url": "https://github.com/mlflow/mlflow.git",
                "type": "mlops"
            },
            "bentoml": {
                "url": "https://github.com/bentoml/BentoML.git",
                "type": "deployment"
            }
        }
        
        for repo_name, repo_info in repositories.items():
            try:
                repo_type = repo_info["type"]
                repo_url = repo_info["url"]
                target_dir = self.ai_stack_dir / repo_type / repo_name
                
                if target_dir.exists():
                    print(f"⚠️ {repo_name} already exists, skipping...")
                    continue
                
                print(f"Cloning {repo_name}...")
                result = subprocess.run(["git", "clone", repo_url, str(target_dir)], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ {repo_name} cloned to {target_dir}")
                else:
                    print(f"❌ Failed to clone {repo_name}: {result.stderr}")
                    
            except Exception as e:
                print(f"❌ Error cloning {repo_name}: {e}")
    
    def install_python_packages(self):
        """Install Python packages"""
        print("\n🐍 Installing Python packages...")
        
        # Create virtual environment for AI stack
        venv_path = self.ai_stack_dir / "ai-stack-env"
        if not venv_path.exists():
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)])
            print(f"✅ Created virtual environment: {venv_path}")
        
        # Activate virtual environment and install packages
        pip_cmd = str(venv_path / "bin" / "pip")
        
        python_packages = [
            "db-gpt", "promptic", "transformers", "langchain", "pyautogen",
            "deepspeed", "dvc", "mlflow", "bentoml"
        ]
        
        for package in python_packages:
            try:
                print(f"Installing {package}...")
                result = subprocess.run([pip_cmd, "install", package], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {package} installed")
                else:
                    print(f"⚠️ {package} installation had issues: {result.stderr}")
            except Exception as e:
                print(f"❌ Failed to install {package}: {e}")
    
    def download_binaries(self):
        """Download binary executables"""
        print("\n📦 Downloading binary executables...")
        
        # Download Yao binary
        try:
            yao_path = self.ai_stack_dir / "binaries" / "yao"
            yao_path.parent.mkdir(exist_ok=True)
            
            print("Downloading Yao binary...")
            subprocess.run(["wget", "-O", str(yao_path), 
                          "https://github.com/YaoApp/yao/releases/latest/download/yao"])
            subprocess.run(["chmod", "+x", str(yao_path)])
            print("✅ Yao binary downloaded and made executable")
        except Exception as e:
            print(f"❌ Failed to download Yao: {e}")
    
    def setup_ollama(self):
        """Set up Ollama for local LLM inference"""
        print("\n🤖 Setting up Ollama...")
        
        try:
            # Install Ollama
            subprocess.run(["curl", "-fsSL", "https://ollama.com/install.sh", "|", "sh"], 
                          shell=True)
            print("✅ Ollama installed")
            
            # Start Ollama service
            subprocess.run(["ollama", "serve"], background=True)
            print("✅ Ollama service started")
            
            # Pull basic models
            models = ["llama3", "mistral", "codellama"]
            for model in models:
                try:
                    print(f"Pulling {model} model...")
                    subprocess.run(["ollama", "pull", model], 
                                  capture_output=True, text=True)
                    print(f"✅ {model} model pulled")
                except Exception as e:
                    print(f"⚠️ Failed to pull {model}: {e}")
                    
        except Exception as e:
            print(f"❌ Ollama setup failed: {e}")

# Main execution for Part 2
if __name__ == "__main__":
    print("🧠 AI Stack Integration - Part 2: Repository Cloning & Package Installation")
    print("=" * 60)
    
    part2 = AIStackPart2()
    
    # Run Part 2 setup
    part2.clone_repositories()
    part2.install_python_packages()
    part2.download_binaries()
    part2.setup_ollama()
    
    print("\n✅ Part 2 Complete: Repositories and Packages")
    print("🚀 Ready for Part 3: Integration Configuration")
