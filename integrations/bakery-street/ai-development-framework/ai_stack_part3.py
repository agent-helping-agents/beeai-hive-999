#!/usr/bin/env python3
"""
AI Development Stack Integration Script - Part 3
Integration configuration and usage examples
"""

import json
from pathlib import Path

class AIStackPart3:
    def __init__(self):
        self.project_root = Path("/home/booze/ai-development")
        self.ai_stack_dir = self.project_root / "ai-stack"
        
    def create_integration_config(self):
        """Create integration configuration files"""
        print("\n⚙️ Creating integration configuration...")
        
        # Create main configuration
        config = {
            "ai_stack": {
                "version": "1.0",
                "description": "Comprehensive AI Development Stack",
                "integration": {
                    "aios": {
                        "enabled": True,
                        "path": str(self.project_root / "environments" / "aios-env"),
                        "integration_type": "core_orchestration"
                    },
                    "crewai": {
                        "enabled": True,
                        "integration_type": "agent_orchestration"
                    },
                    "ollama": {
                        "enabled": True,
                        "host": "http://localhost:11434",
                        "integration_type": "local_llm"
                    }
                }
            }
        }
        
        config_file = self.ai_stack_dir / "ai_stack_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Configuration saved to {config_file}")
        
        # Create integration script
        integration_script = self.ai_stack_dir / "integrate_with_aios.py"
        with open(integration_script, 'w') as f:
            f.write(self._generate_integration_script())
        
        print(f"✅ Integration script created: {integration_script}")
    
    def _generate_integration_script(self):
        """Generate the AIOS integration script"""
        return '''#!/usr/bin/env python3
"""
AIOS Integration Script
Integrates all AI stack components with AIOS
"""

import sys
import os
from pathlib import Path

# Add AI stack to Python path
ai_stack_path = Path(__file__).parent
sys.path.insert(0, str(ai_stack_path))

def integrate_components():
    """Integrate all AI stack components with AIOS"""
    print("🔗 Integrating AI Stack with AIOS...")
    
    # Import AIOS
    try:
        import aios
        print(f"✅ AIOS {aios.__version__} loaded")
    except ImportError as e:
        print(f"❌ AIOS import failed: {e}")
        return False
    
    # Test integrations
    integrations = [
        ("LangChain", "langchain"),
        ("AutoGen", "pyautogen"),
        ("Transformers", "transformers"),
        ("DB-GPT", "dbgpt"),
        ("MLflow", "mlflow"),
        ("BentoML", "bentoml")
    ]
    
    for name, module in integrations:
        try:
            __import__(module)
            print(f"✅ {name} integration successful")
        except ImportError:
            print(f"⚠️ {name} not available")
    
    print("🎉 AI Stack integration complete!")
    return True

if __name__ == "__main__":
    integrate_components()
'''
    
    def create_usage_examples(self):
        """Create usage examples and documentation"""
        print("\n📚 Creating usage examples...")
        
        examples_dir = self.ai_stack_dir / "examples"
        examples_dir.mkdir(exist_ok=True)
        
        # Create basic usage examples
        examples = {
            "aios_langchain_integration.py": self._create_langchain_example(),
            "aios_autogen_integration.py": self._create_autogen_example(),
            "aios_transformers_integration.py": self._create_transformers_example(),
            "aios_db_gpt_integration.py": self._create_db_gpt_example()
        }
        
        for filename, content in examples.items():
            example_file = examples_dir / filename
            with open(example_file, 'w') as f:
                f.write(content)
            print(f"✅ Created example: {filename}")
    
    def _create_langchain_example(self):
        """Create LangChain integration example"""
        return '''#!/usr/bin/env python3
"""
AIOS + LangChain Integration Example
Shows how to use LangChain with AIOS agents
"""

from aios.object import Object
from aios.state import State

try:
    from langchain.agents import initialize_agent, AgentType
    from langchain.llms import Ollama
    from langchain.tools import Tool
    
    class AIOSLangChainAgent:
        def __init__(self):
            self.agent = Object()
            self.status = State(['idle', 'working', 'done'], name='status', default='idle')
            self.llm = Ollama(model="llama3")
            
        def create_tools(self):
            """Create LangChain tools"""
            tools = [
                Tool(
                    name="aios_status",
                    func=lambda x: f"AIOS Agent Status: {self.status.current_state}",
                    description="Get AIOS agent status"
                )
            ]
            return tools
        
        def run_agent(self, query):
            """Run LangChain agent with AIOS integration"""
            self.status.change_state('working')
            
            tools = self.create_tools()
            agent = initialize_agent(tools, self.llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
            
            result = agent.run(query)
            
            self.status.change_state('done')
            return result
    
    # Example usage
    if __name__ == "__main__":
        agent = AIOSLangChainAgent()
        result = agent.run_agent("What is the current AIOS agent status?")
        print(f"Result: {result}")
        
except ImportError:
    print("LangChain not available. Install with: pip install langchain")
'''
    
    def _create_autogen_example(self):
        """Create AutoGen integration example"""
        return '''#!/usr/bin/env python3
"""
AIOS + AutoGen Integration Example
Shows how to use AutoGen with AIOS agents
"""

from aios.object import Object
from aios.state import State

try:
    import autogen
    
    class AIOSAutoGenAgent:
        def __init__(self):
            self.agent = Object()
            self.status = State(['idle', 'working', 'done'], name='status', default='idle')
            
        def create_autogen_agents(self):
            """Create AutoGen agents"""
            config_list = [
                {
                    "model": "llama3",
                    "api_base": "http://localhost:11434/v1",
                    "api_type": "open_ai",
                    "api_key": "ollama"
                }
            ]
            
            llm_config = {"config_list": config_list}
            
            # Create agents
            user_proxy = autogen.UserProxyAgent(
                name="user_proxy",
                human_input_mode="NEVER",
                max_consecutive_auto_reply=10,
                is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
                code_execution_config={"work_dir": "workspace"},
                llm_config=llm_config
            )
            
            coder = autogen.AssistantAgent(
                name="coder",
                llm_config=llm_config
            )
            
            return user_proxy, coder
        
        def run_conversation(self, message):
            """Run AutoGen conversation with AIOS integration"""
            self.status.change_state('working')
            
            user_proxy, coder = self.create_autogen_agents()
            
            # Start conversation
            user_proxy.initiate_chat(
                coder,
                message=message
            )
            
            self.status.change_state('done')
            return "Conversation completed"
    
    # Example usage
    if __name__ == "__main__":
        agent = AIOSAutoGenAgent()
        result = agent.run_conversation("Create a simple Python function to calculate fibonacci numbers")
        print(f"Result: {result}")
        
except ImportError:
    print("AutoGen not available. Install with: pip install pyautogen")
'''
    
    def _create_transformers_example(self):
        """Create Transformers integration example"""
        return '''#!/usr/bin/env python3
"""
AIOS + Transformers Integration Example
Shows how to use Transformers with AIOS agents
"""

from aios.object import Object
from aios.state import State

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    
    class AIOSTransformersAgent:
        def __init__(self):
            self.agent = Object()
            self.status = State(['idle', 'working', 'done'], name='status', default='idle')
            
        def load_model(self, model_name="microsoft/DialoGPT-medium"):
            """Load a Transformers model"""
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForCausalLM.from_pretrained(model_name)
                print(f"✅ Model {model_name} loaded successfully")
                return True
            except Exception as e:
                print(f"❌ Failed to load model: {e}")
                return False
        
        def generate_response(self, input_text):
            """Generate response using loaded model"""
            if not hasattr(self, 'model'):
                return "No model loaded"
            
            self.status.change_state('working')
            
            try:
                # Encode input
                input_ids = self.tokenizer.encode(input_text + self.tokenizer.eos_token, return_tensors='pt')
                
                # Generate response
                response_ids = self.model.generate(
                    input_ids,
                    max_length=1000,
                    pad_token_id=self.tokenizer.eos_token_id,
                    do_sample=True,
                    temperature=0.7
                )
                
                # Decode response
                response = self.tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
                
                self.status.change_state('done')
                return response
                
            except Exception as e:
                print(f"❌ Generation failed: {e}")
                return f"Error: {e}"
    
    # Example usage
    if __name__ == "__main__":
        agent = AIOSTransformersAgent()
        if agent.load_model():
            response = agent.generate_response("Hello, how are you?")
            print(f"Response: {response}")
        
except ImportError:
    print("Transformers not available. Install with: pip install transformers")
'''
    
    def _create_db_gpt_example(self):
        """Create DB-GPT integration example"""
        return '''#!/usr/bin/env python3
"""
AIOS + DB-GPT Integration Example
Shows how to use DB-GPT with AIOS agents
"""

from aios.object import Object
from aios.state import State

try:
    from dbgpt import DBGPT
    
    class AIOSDBGPTAgent:
        def __init__(self):
            self.agent = Object()
            self.status = State(['idle', 'working', 'done'], name='status', default='idle')
            
        def connect_to_db_gpt(self, host="localhost", port=5000):
            """Connect to DB-GPT instance"""
            try:
                self.db_gpt = DBGPT(host=host, port=port)
                print(f"✅ Connected to DB-GPT at {host}:{port}")
                return True
            except Exception as e:
                print(f"❌ Failed to connect to DB-GPT: {e}")
                return False
        
        def run_query(self, query):
            """Run a query using DB-GPT"""
            if not hasattr(self, 'db_gpt'):
                return "Not connected to DB-GPT"
            
            self.status.change_state('working')
            
            try:
                # Execute query
                result = self.db_gpt.query(query)
                
                self.status.change_state('done')
                return result
                
            except Exception as e:
                print(f"❌ Query failed: {e}")
                return f"Error: {e}"
    
    # Example usage
    if __name__ == "__main__":
        agent = AIOSDBGPTAgent()
        if agent.connect_to_db_gpt():
            result = agent.run_query("Show me the database schema")
            print(f"Result: {result}")
        
except ImportError:
    print("DB-GPT not available. Install with: pip install db-gpt")
'''
    
    def create_master_script(self):
        """Create master script to run all parts"""
        print("\n🎯 Creating master integration script...")
        
        master_script = self.ai_stack_dir / "run_full_integration.py"
        with open(master_script, 'w') as f:
            f.write(self._generate_master_script())
        
        print(f"✅ Master script created: {master_script}")
    
    def _generate_master_script(self):
        """Generate the master integration script"""
        return '''#!/usr/bin/env python3
"""
Master AI Stack Integration Script
Runs all parts of the AI stack integration
"""

import subprocess
import sys
from pathlib import Path

def run_part(part_name, script_path):
    """Run a specific part of the integration"""
    print(f"\\n🚀 Running {part_name}...")
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
    print("\\n" + "=" * 50)
    print(f"🎯 Integration Summary: {success_count}/{len(parts)} parts completed")
    
    if success_count == len(parts):
        print("🎉 All parts completed successfully!")
        print("🚀 Your AI Development Stack is ready!")
        print("\\nNext steps:")
        print("1. Test integration: python ai-stack/integrate_with_aios.py")
        print("2. Run examples: python ai-stack/examples/aios_langchain_integration.py")
        print("3. Start building with AIOS!")
    else:
        print("⚠️ Some parts failed. Check the logs above.")
        print("💡 You can run individual parts manually.")

if __name__ == "__main__":
    main()
'''

# Main execution for Part 3
if __name__ == "__main__":
    print("🧠 AI Stack Integration - Part 3: Configuration & Examples")
    print("=" * 60)
    
    part3 = AIStackPart3()
    
    # Run Part 3 setup
    part3.create_integration_config()
    
    print("\n✅ Part 3 Complete: Configuration and Examples")
    print("🎯 All parts ready! Run: python ai-stack/run_full_integration.py")
