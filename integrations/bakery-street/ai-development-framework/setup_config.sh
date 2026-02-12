#!/bin/bash

# AIOS Configuration Setup Script
# Sets up the basic configuration structure for AIOS agents

echo "=== AIOS Configuration Setup ==="

# Create AIOS configuration directory
mkdir -p ~/.aios
echo "✅ Created ~/.aios directory"

# Create basic configuration file
cat > ~/.aios/config.yaml << 'EOF'
# AIOS Basic Configuration
aios:
  version: "0.2.2"
  environment: "development"
  
  # Agent Configuration
  agents:
    max_concurrent: 5
    default_timeout: 300
    
  # LLM Provider Configuration
  llm_providers:
    openai:
      enabled: false
      api_key: ""
      models: ["gpt-4", "gpt-3.5-turbo"]
    
    ollama:
      enabled: true
      host: "http://localhost:11434"
      models: ["llama3", "mistral", "codellama"]
    
    huggingface:
      enabled: false
      api_key: ""
      models: ["meta-llama/Llama-2-7b-chat-hf"]
  
  # Storage Configuration
  storage:
    type: "local"
    path: "~/.aios/storage"
    
  # Logging Configuration
  logging:
    level: "INFO"
    file: "~/.aios/aios.log"
    
  # Security Configuration
  security:
    allow_local_execution: true
    require_api_keys: false
EOF

echo "✅ Created ~/.aios/config.yaml"

# Create agent templates directory
mkdir -p ~/.aios/templates
echo "✅ Created ~/.aios/templates directory"

# Create basic agent template
cat > ~/.aios/templates/productivity_agent.py << 'EOF'
#!/usr/bin/env python3
"""
AIOS Productivity Agent Template
Basic template for creating productivity agents
"""

from aios.object import Object
from aios.state import State
import logging

class ProductivityAgent:
    def __init__(self, name="ProductivityAgent"):
        self.agent = Object()
        self.name = name
        self.status = State(['idle', 'working', 'done', 'error'], 
                           name='status', default='idle')
        self.logger = logging.getLogger(f"aios.agent.{name}")
        
    def start_work(self):
        """Start the agent's work"""
        try:
            self.status.change_state('working')
            self.logger.info(f"Agent {self.name} started working")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start work: {e}")
            self.status.change_state('error')
            return False
    
    def complete_work(self):
        """Mark work as complete"""
        try:
            self.status.change_state('done')
            self.logger.info(f"Agent {self.name} completed work")
            return True
        except Exception as e:
            self.logger.error(f"Failed to complete work: {e}")
            self.status.change_state('error')
            return False
    
    def reset(self):
        """Reset agent to idle state"""
        try:
            self.status.change_state('idle')
            self.logger.info(f"Agent {self.name} reset to idle")
            return True
        except Exception as e:
            self.logger.error(f"Failed to reset: {e}")
            return False
    
    def get_status(self):
        """Get current agent status"""
        return {
            'name': self.name,
            'status': self.status.current_state,
            'available_states': self.status.states
        }

# Example usage
if __name__ == "__main__":
    agent = ProductivityAgent("TestAgent")
    print(f"Agent created: {agent.get_status()}")
    
    agent.start_work()
    print(f"Agent status: {agent.get_status()}")
    
    agent.complete_work()
    print(f"Agent status: {agent.get_status()}")
EOF

echo "✅ Created ~/.aios/templates/productivity_agent.py"

# Create AIOS launcher configuration
cat > ~/.aios/launcher_config.yaml << 'EOF'
# AIOS Launcher Configuration
launcher:
  name: "AIOS Desktop Launcher"
  version: "1.0"
  
  # Menu Options
  menu_options:
    - name: "Launch AIOS Interactive Shell"
      command: "aios_shell"
      description: "Start AIOS with interactive Python shell"
      
    - name: "Start Productivity Agent"
      command: "start_agent"
      description: "Launch a productivity agent"
      
    - name: "Check AIOS Status"
      command: "check_status"
      description: "Verify AIOS installation and configuration"
      
    - name: "Configure AIOS"
      command: "configure"
      description: "Set up API keys and LLM providers"
      
    - name: "Run AIOS Tests"
      command: "run_tests"
      description: "Execute AIOS functionality tests"

# Environment Configuration
environment:
  python_path: "environments/aios-env/bin/python"
  working_directory: "/home/booze/ai-development"
  log_level: "INFO"
EOF

echo "✅ Created ~/.aios/launcher_config.yaml"

# Create startup script
cat > ~/.aios/start_aios.sh << 'EOF'
#!/bin/bash

# AIOS Startup Script
# Activates environment and starts AIOS services

echo "🚀 Starting AIOS..."

# Activate virtual environment
source /home/booze/ai-development/environments/aios-env/bin/activate

# Check AIOS installation
python -c "import aios; print(f'✅ AIOS {aios.__version__} loaded successfully')"

# Start basic services
echo "✅ AIOS environment activated"
echo "✅ Ready for agent operations"

# Keep shell active
exec bash
EOF

chmod +x ~/.aios/start_aios.sh
echo "✅ Created ~/.aios/start_aios.sh (executable)"

echo ""
echo "🎉 AIOS Configuration Setup Complete!"
echo ""
echo "📁 Configuration files created in ~/.aios/"
echo "🚀 Ready to test agents and build full AIOS system!"
echo ""
echo "Next steps:"
echo "1. Test the agent template: python ~/.aios/templates/productivity_agent.py"
echo "2. Use the startup script: ~/.aios/start_aios.sh"
echo "3. Let agents build the full AIOS system!"
