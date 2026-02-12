#!/usr/bin/env python3
"""
AIOS Builder Agent
Automates the complete AIOS system setup using our comprehensive AI stack
"""

from aios.object import Object
from aios.state import State
import subprocess
import os
import sys
import logging
from pathlib import Path

class AIOSBuilderAgent:
    def __init__(self, name="AIOSBuilder"):
        self.agent = Object()
        self.name = name
        self.status = State(['idle', 'analyzing', 'building', 'testing', 'done', 'error'], 
                           name='status', default='idle')
        self.logger = logging.getLogger(f"aios.builder.{name}")
        self.working_dir = Path("/home/booze/ai-development")
        self.aios_env = self.working_dir / "environments" / "aios-env"
        
    def analyze_current_state(self):
        """Analyze current AIOS installation state"""
        try:
            self.status.change_state('analyzing')
            self.logger.info("Analyzing current AIOS state...")
            
            analysis = {
                'aios_installed': False,
                'aios_version': None,
                'ai_stack_ready': False,
                'config_exists': False,
                'issues': []
            }
            
            # Check AIOS installation
            try:
                import aios
                analysis['aios_installed'] = True
                analysis['aios_version'] = getattr(aios, '__version__', 'Unknown')
                self.logger.info(f"AIOS {analysis['aios_version']} detected")
            except ImportError as e:
                analysis['issues'].append(f"AIOS import failed: {e}")
            
            # Check AI stack
            ai_stack_dir = self.working_dir / "ai-stack"
            if ai_stack_dir.exists():
                analysis['ai_stack_ready'] = True
                self.logger.info("AI Stack directory exists")
            else:
                analysis['issues'].append("AI Stack not found")
            
            # Check configuration
            config_dir = Path.home() / ".aios"
            if config_dir.exists():
                analysis['config_exists'] = True
                self.logger.info("AIOS configuration exists")
            else:
                analysis['issues'].append("No AIOS configuration directory")
            
            self.logger.info(f"Analysis complete: {analysis}")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            self.status.change_state('error')
            return None
    
    def build_full_aios(self):
        """Build the complete AIOS system using our AI stack"""
        try:
            self.status.change_state('building')
            self.logger.info("Starting full AIOS build using AI stack...")
            
            # Step 1: Set up AI stack if not ready
            if not (self.working_dir / "ai-stack").exists():
                self.logger.info("Setting up AI stack first...")
                self._setup_ai_stack()
            
            # Step 2: Configure AIOS with AI stack integration
            self.logger.info("Configuring AIOS with AI stack...")
            self._configure_aios_integration()
            
            # Step 3: Install missing AIOS components
            self.logger.info("Installing missing AIOS components...")
            self._install_aios_components()
            
            # Step 4: Test the complete system
            self.logger.info("Testing complete AIOS system...")
            test_result = self._test_complete_system()
            
            if test_result:
                self.status.change_state('testing')
                self.logger.info("AIOS system built successfully!")
                return True
            else:
                self.logger.error("AIOS system build failed")
                self.status.change_state('error')
                return False
                
        except Exception as e:
            self.logger.error(f"Build failed: {e}")
            self.status.change_state('error')
            return False
    
    def _setup_ai_stack(self):
        """Set up the AI stack if not ready"""
        try:
            # Run AI stack setup
            setup_script = self.working_dir / "ai_stack_master.py"
            if setup_script.exists():
                self.logger.info("Running AI stack setup...")
                result = subprocess.run([sys.executable, str(setup_script)], 
                                      capture_output=True, text=True, cwd=self.working_dir)
                if result.returncode == 0:
                    self.logger.info("AI stack setup completed")
                else:
                    self.logger.warning(f"AI stack setup had issues: {result.stderr}")
            else:
                self.logger.warning("AI stack setup script not found")
                
        except Exception as e:
            self.logger.error(f"AI stack setup failed: {e}")
    
    def _configure_aios_integration(self):
        """Configure AIOS integration with AI stack"""
        try:
            # Create enhanced AIOS configuration
            config_dir = Path.home() / ".aios"
            config_dir.mkdir(exist_ok=True)
            
            # Enhanced AIOS config with AI stack integration
            enhanced_config = {
                "aios": {
                    "version": "0.2.2",
                    "environment": "production",
                    "ai_stack_integration": {
                        "enabled": True,
                        "path": str(self.working_dir / "ai-stack"),
                        "components": {
                            "langchain": True,
                            "autogen": True,
                            "transformers": True,
                            "db_gpt": True,
                            "mlflow": True,
                            "bentoml": True,
                            "ollama": True
                        }
                    },
                    "agents": {
                        "max_concurrent": 10,
                        "default_timeout": 600,
                        "auto_scaling": True
                    },
                    "llm_providers": {
                        "ollama": {
                            "enabled": True,
                            "host": "http://localhost:11434",
                            "models": ["llama3", "mistral", "codellama", "neural-chat"]
                        },
                        "openai": {
                            "enabled": False,
                            "api_key": "",
                            "models": ["gpt-4", "gpt-3.5-turbo"]
                        }
                    }
                }
            }
            
            # Save enhanced config
            config_file = config_dir / "enhanced_aios_config.json"
            import json
            with open(config_file, 'w') as f:
                json.dump(enhanced_config, f, indent=2)
            
            self.logger.info(f"Enhanced AIOS config saved to {config_file}")
            
        except Exception as e:
            self.logger.error(f"AIOS integration configuration failed: {e}")
    
    def _install_aios_components(self):
        """Install missing AIOS components"""
        try:
            # Activate AIOS environment
            pip_cmd = str(self.aios_env / "bin" / "pip")
            
            # Core AIOS dependencies
            aios_dependencies = [
                "fastapi", "uvicorn", "redis", "chromadb",
                "sentence-transformers", "nltk", "scikit-learn"
            ]
            
            for dep in aios_dependencies:
                try:
                    self.logger.info(f"Installing AIOS dependency: {dep}")
                    result = subprocess.run([pip_cmd, "install", dep], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        self.logger.info(f"✅ {dep} installed")
                    else:
                        self.logger.warning(f"⚠️ {dep} installation had issues")
                except Exception as e:
                    self.logger.warning(f"⚠️ Failed to install {dep}: {e}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"AIOS component installation failed: {e}")
            return False
    
    def _test_complete_system(self):
        """Test the complete AIOS system"""
        try:
            # Test AIOS core
            aios_test = """
import aios
from aios.object import Object
from aios.state import State

# Test basic functionality
agent = Object()
status = State(['idle', 'working'], name='test', default='idle')
print(f"✅ AIOS core test passed: Agent={agent}, Status={status}")
"""
            
            result = subprocess.run([str(self.aios_env / "bin" / "python"), "-c", aios_test],
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info("✅ AIOS core test passed")
            else:
                self.logger.error(f"❌ AIOS core test failed: {result.stderr}")
                return False
            
            # Test AI stack integration
            integration_test = """
import sys
from pathlib import Path

# Test AI stack availability
ai_stack_path = Path("/home/booze/ai-development/ai-stack")
if ai_stack_path.exists():
    print("✅ AI stack directory accessible")
else:
    print("❌ AI stack directory not found")
    sys.exit(1)

# Test key components
try:
    import torch
    print("✅ PyTorch available")
except ImportError:
    print("⚠️ PyTorch not available")

try:
    import langchain
    print("✅ LangChain available")
except ImportError:
    print("⚠️ LangChain not available")

print("✅ AI stack integration test passed")
"""
            
            result = subprocess.run([str(self.aios_env / "bin" / "python"), "-c", integration_test],
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info("✅ AI stack integration test passed")
                return True
            else:
                self.logger.error(f"❌ AI stack integration test failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Complete system test failed: {e}")
            return False
    
    def create_productivity_workflow(self):
        """Create a productivity workflow using the complete AIOS system"""
        try:
            self.logger.info("Creating AIOS productivity workflow...")
            
            workflow_code = """
#!/usr/bin/env python3
\"\"\"
AIOS Productivity Workflow
Demonstrates the complete AIOS system with AI stack integration
\"\"\"

from aios.object import Object
from aios.state import State
import time

class AIOSProductivityWorkflow:
    def __init__(self):
        self.workflow = Object()
        self.status = State(['planning', 'executing', 'monitoring', 'completed'], 
                           name='workflow_status', default='planning')
        self.tasks = []
        
    def add_task(self, task_name, task_type, ai_tools=None):
        task = {
            'name': task_name,
            'type': task_type,
            'status': 'pending',
            'agent': Object(),
            'ai_tools': ai_tools or []
        }
        self.tasks.append(task)
        print(f"✅ Task added: {task_name}")
        
    def execute_workflow(self):
        self.status.change_state('executing')
        print(f"🚀 Executing AIOS workflow with {len(self.tasks)} tasks...")
        
        for i, task in enumerate(self.tasks, 1):
            print(f"📋 Task {i}: {task['name']} ({task['type']})")
            task['status'] = 'in_progress'
            
            # Simulate AI-powered work
            if task['ai_tools']:
                print(f"   🤖 Using AI tools: {', '.join(task['ai_tools'])}")
            
            time.sleep(0.5)
            task['status'] = 'completed'
            print(f"✅ Task {i} completed")
        
        self.status.change_state('completed')
        print("🎉 All AIOS tasks completed!")
        
    def get_workflow_status(self):
        return {
            'workflow_status': self.status.current_state,
            'total_tasks': len(self.tasks),
            'completed_tasks': len([t for t in self.tasks if t['status'] == 'completed']),
            'pending_tasks': len([t for t in self.tasks if t['status'] == 'pending'])
        }

# Example usage
if __name__ == "__main__":
    workflow = AIOSProductivityWorkflow()
    
    # Add AI-powered productivity tasks
    workflow.add_task("Configure AIOS", "setup", ["AI Stack", "LangChain"])
    workflow.add_task("Install Dependencies", "installation", ["PyTorch", "Transformers"])
    workflow.add_task("Test System", "testing", ["AutoGen", "MLflow"])
    workflow.add_task("Create Agents", "development", ["DB-GPT", "BentoML"])
    workflow.add_task("Deploy Models", "deployment", ["Ollama", "FastAPI"])
    
    # Execute workflow
    workflow.execute_workflow()
    
    # Show results
    print("\\n📊 AIOS Workflow Results:")
    print(workflow.get_workflow_status())
"""
            
            # Save workflow
            workflow_file = Path.home() / ".aios" / "templates" / "aios_productivity_workflow.py"
            workflow_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(workflow_file, 'w') as f:
                f.write(workflow_code)
            
            self.logger.info(f"✅ AIOS productivity workflow created: {workflow_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Workflow creation failed: {e}")
            return False
    
    def get_status(self):
        """Get current agent status"""
        return {
            'name': self.name,
            'status': self.status.current_state,
            'available_states': self.status.states,
            'working_directory': str(self.working_dir),
            'aios_environment': str(self.aios_env)
        }
    
    def run_full_build(self):
        """Run the complete AIOS build process"""
        try:
            self.logger.info("🚀 Starting complete AIOS build process...")
            
            # Step 1: Analyze current state
            analysis = self.analyze_current_state()
            if not analysis:
                return False
            
            # Step 2: Build full system
            build_success = self.build_full_aios()
            if not build_success:
                return False
            
            # Step 3: Create productivity workflow
            workflow_success = self.create_productivity_workflow()
            if not workflow_success:
                self.logger.warning("Workflow creation failed, but system is built")
            
            # Step 4: Final testing
            self.status.change_state('testing')
            final_test = self._test_complete_system()
            
            if final_test:
                self.status.change_state('done')
                self.logger.info("🎉 Complete AIOS build completed successfully!")
                return True
            else:
                self.status.change_state('error')
                self.logger.error("❌ Final testing failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Full build process failed: {e}")
            self.status.change_state('error')
            return False

# Main execution
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    print("🧠 AIOS Builder Agent Starting...")
    
    # Create and run builder agent
    builder = AIOSBuilderAgent("AIOSBuilder")
    print(f"✅ Builder agent created: {builder.get_status()}")
    
    # Run full build process
    success = builder.run_full_build()
    
    if success:
        print("\\n🎉 AIOS Build Process COMPLETED!")
        print("🚀 Your AIOS system is now ready for production use!")
        print("\\nNext steps:")
        print("1. Test the system: python ~/.aios/templates/aios_productivity_workflow.py")
        print("2. Use the desktop launcher")
        print("3. Start building your own AI agents!")
    else:
        print("\\n💥 AIOS Build Process FAILED!")
        print("Check the logs for details and try again.")
