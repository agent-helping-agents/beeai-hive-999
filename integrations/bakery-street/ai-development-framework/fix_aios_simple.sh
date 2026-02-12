#!/bin/bash

# Simple AIOS Fix Script
# Fixes the AIOS installation step by step

echo "🔧 Simple AIOS Fix Script"
echo "=========================="

# Check if we're in the right directory
if [ ! -d "environments/aios-env" ]; then
    echo "❌ AIOS environment not found"
    echo "Please run this script from /home/booze/ai-development"
    exit 1
fi

# Step 1: Create AIOS directory in site-packages
echo "📁 Step 1: Creating AIOS directory..."
AIOS_DIR="environments/aios-env/lib/python3.11/site-packages/aios"
mkdir -p "$AIOS_DIR"

if [ -d "$AIOS_DIR" ]; then
    echo "✅ AIOS directory created: $AIOS_DIR"
else
    echo "❌ Failed to create AIOS directory"
    exit 1
fi

# Step 2: Create __init__.py
echo "📝 Step 2: Creating __init__.py..."
cat > "$AIOS_DIR/__init__.py" << 'EOF'
"""
AIOS - AGI Research Agent Orchestration System
Minimal working package
"""

__version__ = "0.2.2"

class Object:
    """AIOS Object class for agent representation"""
    def __init__(self, name=None, properties=None):
        self.name = name or "AIOS_Object"
        self.properties = properties or {}
        self.id = id(self)
    
    def __str__(self):
        return f"AIOS_Object({self.name}, id={self.id})"
    
    def __repr__(self):
        return self.__str__()
    
    def set_property(self, key, value):
        """Set a property on the object"""
        self.properties[key] = value
    
    def get_property(self, key, default=None):
        """Get a property from the object"""
        return self.properties.get(key, default)

class State:
    """AIOS State class for state management"""
    def __init__(self, states, name="state", default=None):
        self.states = list(states)
        self.name = name
        self.current_state = default or states[0] if states else None
        self.history = []
    
    def __str__(self):
        return f"AIOS_State({self.name}: {self.current_state})"
    
    def __repr__(self):
        return self.__str__()
    
    def change_state(self, new_state):
        """Change to a new state"""
        if new_state in self.states:
            old_state = self.current_state
            self.current_state = new_state
            self.history.append({
                'from': old_state,
                'to': new_state,
                'timestamp': __import__('time').time()
            })
            return True
        else:
            raise ValueError(f"Invalid state: {new_state}. Valid states: {self.states}")
    
    def get_history(self):
        """Get state change history"""
        return self.history.copy()
    
    def reset(self):
        """Reset to initial state"""
        if self.states:
            self.current_state = self.states[0]
            self.history.clear()

# Export main classes
__all__ = ["Object", "State"]
EOF

if [ -f "$AIOS_DIR/__init__.py" ]; then
    echo "✅ __init__.py created"
else
    echo "❌ Failed to create __init__.py"
    exit 1
fi

# Step 3: Create object.py
echo "📝 Step 3: Creating object.py..."
cat > "$AIOS_DIR/object.py" << 'EOF'
"""
AIOS Object Module
"""

class Object:
    """AIOS Object class for agent representation"""
    def __init__(self, name=None, properties=None):
        self.name = name or "AIOS_Object"
        self.properties = properties or {}
        self.id = id(self)
    
    def __str__(self):
        return f"AIOS_Object({self.name}, id={self.id})"
    
    def __repr__(self):
        return self.__str__()
    
    def set_property(self, key, value):
        """Set a property on the object"""
        self.properties[key] = value
    
    def get_property(self, key, default=None):
        """Get a property from the object"""
        return self.properties.get(key, default)
EOF

if [ -f "$AIOS_DIR/object.py" ]; then
    echo "✅ object.py created"
else
    echo "❌ Failed to create object.py"
    exit 1
fi

# Step 4: Create state.py
echo "📝 Step 4: Creating state.py..."
cat > "$AIOS_DIR/state.py" << 'EOF'
"""
AIOS State Module
"""

import time

class State:
    """AIOS State class for state management"""
    def __init__(self, states, name="state", default=None):
        self.states = list(states)
        self.name = name
        self.current_state = default or states[0] if states else None
        self.history = []
    
    def __str__(self):
        return f"AIOS_State({self.name}: {self.current_state})"
    
    def __repr__(self):
        return self.__str__()
    
    def change_state(self, new_state):
        """Change to a new state"""
        if new_state in self.states:
            old_state = self.current_state
            self.current_state = new_state
            self.history.append({
                'from': old_state,
                'to': new_state,
                'timestamp': time.time()
            })
            return True
        else:
            raise ValueError(f"Invalid state: {new_state}. Valid states: {self.states}")
    
    def get_history(self):
        """Get state change history"""
        return self.history.copy()
    
    def reset(self):
        """Reset to initial state"""
        if self.states:
            self.current_state = self.states[0]
            self.history.clear()
EOF

if [ -f "$AIOS_DIR/state.py" ]; then
    echo "✅ state.py created"
else
    echo "❌ Failed to create state.py"
    exit 1
fi

# Step 5: Test the installation
echo "🧪 Step 5: Testing AIOS installation..."
echo ""

# Activate environment and test
source environments/aios-env/bin/activate

python -c "
import aios
from aios.object import Object
from aios.state import State

print(f'✅ AIOS {aios.__version__} imported successfully')
print(f'✅ Object class: {Object}')
print(f'✅ State class: {State}')

# Test basic functionality
obj = Object('TestAgent')
state = State(['idle', 'working', 'done'], name='status', default='idle')

print(f'✅ Object created: {obj}')
print(f'✅ State created: {state}')
print(f'✅ Current state: {state.current_state}')

# Test state change
state.change_state('working')
print(f'✅ State changed to: {state.current_state}')

state.change_state('done')
print(f'✅ State changed to: {state.current_state}')

print('🎉 AIOS installation test PASSED!')
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 AIOS Installation Fixed Successfully!"
    echo "🚀 You can now run the AIOS Builder Agent."
    echo ""
    echo "Next steps:"
    echo "1. Test: python debug_aios.py"
    echo "2. Run AIOS Builder: python aios_builder_agent.py"
    echo "3. Or use the launcher: ./run_aios_builder.sh"
else
    echo ""
    echo "💥 AIOS installation test failed!"
    echo "Check the logs above for details."
    exit 1
fi

# Deactivate environment
deactivate
