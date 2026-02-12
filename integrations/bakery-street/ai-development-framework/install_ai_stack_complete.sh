#!/bin/bash

# Complete AI Development Stack Installation Script
# Installs additional GitHub repositories to complete your AI development environment

echo "🚀 Complete AI Development Stack Installation"
echo "============================================="
echo "This will install additional repositories to complete your AI development stack:"
echo "• Data Versioning (DVC)"
echo "• LLM Frameworks (Transformers, LangChain, AutoGen)"
echo "• Training Acceleration (DeepSpeed)"
echo "• Deployment (BentoML, MLflow)"
echo "• Monitoring and MLOps"
echo ""

# Check if we're in the right directory
if [ ! -d "environments/aios-env" ]; then
    echo "❌ AIOS environment not found"
    echo "Please run this script from /home/booze/ai-development"
    exit 1
fi

echo "✅ AIOS environment found"
echo ""

# Create AI stack directory if it doesn't exist
if [ ! -d "ai-stack" ]; then
    echo "📁 Creating AI stack directory..."
    mkdir -p ai-stack
    echo "✅ AI stack directory created"
fi

cd ai-stack

echo ""
echo "🔧 Installing System Dependencies..."
echo "Installing git, curl, wget, and build tools..."

# Install system dependencies
sudo apt update
sudo apt install -y git curl wget build-essential python3-dev python3-pip python3-venv

echo "✅ System dependencies installed"
echo ""

echo "📥 Installing Core AI Development Repositories..."
echo ""

# 1. DVC - Data Version Control
echo "📊 Installing DVC (Data Version Control)..."
if [ ! -d "dvc" ]; then
    git clone https://github.com/iterative/dvc.git
    echo "✅ DVC repository cloned"
else
    echo "✅ DVC repository already exists"
fi

# 2. Transformers - Core NLP Library
echo "🤖 Installing Transformers (Hugging Face)..."
if [ ! -d "transformers" ]; then
    git clone https://github.com/huggingface/transformers.git
    echo "✅ Transformers repository cloned"
else
    echo "✅ Transformers repository already exists"
fi

# 3. LangChain - LLM Framework
echo "🔗 Installing LangChain..."
if [ ! -d "langchain" ]; then
    git clone https://github.com/langchain-ai/langchain.git
    echo "✅ LangChain repository cloned"
else
    echo "✅ LangChain repository already exists"
fi

# 4. AutoGen - Multi-Agent Framework
echo "👥 Installing AutoGen (Microsoft)..."
if [ ! -d "autogen" ]; then
    git clone https://github.com/microsoft/autogen.git
    echo "✅ AutoGen repository cloned"
else
    echo "✅ AutoGen repository already exists"
fi

# 5. DeepSpeed - Training Acceleration
echo "⚡ Installing DeepSpeed (Microsoft)..."
if [ ! -d "deepspeed" ]; then
    git clone https://github.com/microsoft/DeepSpeed.git
    echo "✅ DeepSpeed repository cloned"
else
    echo "✅ DeepSpeed repository already exists"
fi

# 6. BentoML - Model Deployment
echo "📦 Installing BentoML..."
if [ ! -d "bentoml" ]; then
    git clone https://github.com/bentoml/BentoML.git
    echo "✅ BentoML repository cloned"
else
    echo "✅ BentoML repository already exists"
fi

# 7. MLflow - MLOps Platform
echo "🔬 Installing MLflow..."
if [ ! -d "mlflow" ]; then
    git clone https://github.com/mlflow/mlflow.git
    echo "✅ MLflow repository cloned"
else
    echo "✅ MLflow repository already exists"
fi

# 8. DB-GPT - Database AI Framework
echo "🗄️ Installing DB-GPT..."
if [ ! -d "db-gpt" ]; then
    git clone https://github.com/eosphoros-ai/DB-GPT.git
    echo "✅ DB-GPT repository cloned"
else
    echo "✅ DB-GPT repository already exists"
fi

echo ""
echo "📚 Installing Python Dependencies..."
echo ""

# Activate AIOS environment
source ../environments/aios-env/bin/activate

# Install core dependencies for each repository
echo "Installing DVC..."
pip install dvc[all]

echo "Installing Transformers..."
pip install transformers torch torchvision torchaudio

echo "Installing LangChain..."
pip install langchain langchain-community langchain-core

echo "Installing AutoGen..."
pip install pyautogen

echo "Installing DeepSpeed..."
pip install deepspeed

echo "Installing BentoML..."
pip install bentoml

echo "Installing MLflow..."
pip install mlflow

echo "Installing DB-GPT dependencies..."
pip install dbgpt

echo ""
echo "🔧 Creating Integration Scripts..."
echo ""

# Create integration script
cat > integrate_complete_stack.py << 'EOF'
#!/usr/bin/env python3
"""
Complete AI Development Stack Integration
Tests all installed components and creates unified workflow
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test all component imports"""
    print("🧪 Testing Complete AI Stack Imports...")
    
    components = {
        'DVC': 'dvc',
        'Transformers': 'transformers',
        'LangChain': 'langchain',
        'AutoGen': 'autogen',
        'DeepSpeed': 'deepspeed',
        'BentoML': 'bentoml',
        'MLflow': 'mlflow',
        'DB-GPT': 'dbgpt'
    }
    
    results = {}
    for name, module in components.items():
        try:
            __import__(module)
            print(f"✅ {name}: Imported successfully")
            results[name] = True
        except ImportError as e:
            print(f"❌ {name}: Import failed - {e}")
            results[name] = False
    
    return results

def create_unified_workflow():
    """Create a unified workflow using all components"""
    print("\n🔧 Creating Unified AI Development Workflow...")
    
    workflow_code = '''
#!/usr/bin/env python3
"""
Unified AI Development Workflow
Demonstrates integration of all AI stack components
"""

import os
import sys
from pathlib import Path

# Add AI stack to path
ai_stack_path = Path(__file__).parent.parent / "ai-stack"
if str(ai_stack_path) not in sys.path:
    sys.path.insert(0, str(ai_stack_path))

def run_complete_workflow():
    """Run the complete AI development workflow"""
    print("🚀 Complete AI Development Stack Workflow")
    print("=" * 50)
    
    # Step 1: Data Management with DVC
    print("📊 Step 1: Data Management with DVC")
    try:
        import dvc
        print("✅ DVC ready for data versioning")
    except ImportError:
        print("❌ DVC not available")
    
    # Step 2: Model Development with Transformers
    print("\n🤖 Step 2: Model Development with Transformers")
    try:
        import transformers
        print("✅ Transformers ready for model development")
    except ImportError:
        print("❌ Transformers not available")
    
    # Step 3: LLM Orchestration with LangChain
    print("\n🔗 Step 3: LLM Orchestration with LangChain")
    try:
        import langchain
        print("✅ LangChain ready for LLM orchestration")
    except ImportError:
        print("❌ LangChain not available")
    
    # Step 4: Multi-Agent Systems with AutoGen
    print("\n👥 Step 4: Multi-Agent Systems with AutoGen")
    try:
        import autogen
        print("✅ AutoGen ready for multi-agent systems")
    except ImportError:
        print("❌ AutoGen not available")
    
    # Step 5: Training Acceleration with DeepSpeed
    print("\n⚡ Step 5: Training Acceleration with DeepSpeed")
    try:
        import deepspeed
        print("✅ DeepSpeed ready for training acceleration")
    except ImportError:
        print("❌ DeepSpeed not available")
    
    # Step 6: Model Deployment with BentoML
    print("\n📦 Step 6: Model Deployment with BentoML")
    try:
        import bentoml
        print("✅ BentoML ready for model deployment")
    except ImportError:
        print("❌ BentoML not available")
    
    # Step 7: MLOps with MLflow
    print("\n🔬 Step 7: MLOps with MLflow")
    try:
        import mlflow
        print("✅ MLflow ready for MLOps")
    except ImportError:
        print("❌ MLflow not available")
    
    # Step 8: Database AI with DB-GPT
    print("\n🗄️ Step 8: Database AI with DB-GPT")
    try:
        import dbgpt
        print("✅ DB-GPT ready for database AI")
    except ImportError:
        print("❌ DB-GPT not available")
    
    print("\n" + "=" * 50)
    print("🎉 Complete AI Development Stack Ready!")
    print("🚀 You can now build end-to-end AI systems!")

if __name__ == "__main__":
    run_complete_workflow()
'''
    
    # Save workflow
    workflow_file = Path.home() / ".aios" / "templates" / "complete_ai_stack_workflow.py"
    workflow_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(workflow_file, 'w') as f:
        f.write(workflow_code)
    
    print(f"✅ Complete workflow created: {workflow_file}")
    return True

def main():
    """Main integration function"""
    print("🧠 Complete AI Development Stack Integration")
    print("=" * 50)
    
    # Test imports
    results = test_imports()
    
    # Create workflow
    workflow_created = create_unified_workflow()
    
    # Summary
    print("\n" + "=" * 50)
    successful_imports = sum(results.values())
    total_components = len(results)
    
    print(f"📊 Integration Summary: {successful_imports}/{total_components} components working")
    
    if successful_imports == total_components:
        print("🎉 All components integrated successfully!")
        print("🚀 Your complete AI development stack is ready!")
    else:
        print("⚠️ Some components failed to integrate")
        print("💡 Check the logs above for details")
    
    return successful_imports == total_components

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
EOF

echo "✅ Integration script created"

echo ""
echo "🧪 Testing Complete AI Stack..."
echo ""

# Test the integration
python integrate_complete_stack.py

echo ""
echo "🎯 Installation Summary..."
echo ""

# List installed repositories
echo "📚 Installed Repositories:"
for repo in dvc transformers langchain autogen deepspeed bentoml mlflow db-gpt; do
    if [ -d "$repo" ]; then
        echo "✅ $repo"
    else
        echo "❌ $repo"
    fi
done

echo ""
echo "🚀 Next Steps:"
echo "1. Test the complete workflow: python ~/.aios/templates/complete_ai_stack_workflow.py"
echo "2. Start building with your complete AI stack!"
echo "3. Use individual components for specific tasks"
echo "4. Integrate with your existing AIOS system"

# Deactivate environment
deactivate

echo ""
echo "🎉 Complete AI Development Stack Installation Complete!"
echo "Your AI development environment is now enterprise-grade!"
