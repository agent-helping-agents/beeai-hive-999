#!/usr/bin/env python3
"""
Create Minimal AIOS Package
Creates a minimal working AIOS package directly in the virtual environment
"""

import os
import sys
from pathlib import Path

def create_minimal_aios():
    """Create a minimal working AIOS package"""
    print("🔧 Creating Minimal AIOS Package...")
    
    # Get paths
    project_root = Path("/home/booze/ai-development")
    aios_env = project_root / "environments" / "aios-env"
    site_packages = aios_env / "lib" / "python3.11" / "site-packages"
    aios_dir = site_packages / "aios"
    
    print(f"Creating AIOS in: {aios_dir}")
    
    # Create AIOS directory
    aios_dir.mkdir(exist_ok=True)
    
    # Create __init__.py
    init_content = '''"""
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
'''
    
    init_file = aios_dir / "__init__.py"
    with open(init_file, 'w') as f:
        f.write(init_content)
    
    print("✅ Created __init__.py")
    
    # Create object.py
    object_content = '''"""
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
'''
    
    object_file = aios_dir / "object.py"
    with open(object_file, 'w') as f:
        f.write(object_content)
    
    print("✅ Created object.py")
    
    # Create state.py
    state_content = '''"""
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
'''
    
    state_file = aios_dir / "state.py"
    with open(state_file, 'w') as f:
        f.write(state_content)
    
    print("✅ Created state.py")
    
    # Test the installation
    print("\n🧪 Testing minimal AIOS installation...")
    
    test_code = """
import aios
from aios.object import Object
from aios.state import State

print(f"✅ AIOS {aios.__version__} imported successfully")
print(f"✅ Object class: {Object}")
print(f"✅ State class: {State}")

# Test basic functionality
obj = Object("TestAgent")
state = State(['idle', 'working', 'done'], name='status', default='idle')

print(f"✅ Object created: {obj}")
print(f"✅ State created: {state}")
print(f"✅ Current state: {state.current_state}")

# Test state change
state.change_state('working')
print(f"✅ State changed to: {state.current_state}")

state.change_state('done')
print(f"✅ State changed to: {state.current_state}")

print("🎉 Minimal AIOS installation test PASSED!")
"""
    
    # Test using the virtual environment's Python
    python_exe = aios_env / "bin" / "python"
    
    try:
        import subprocess
        result = subprocess.run([str(python_exe), "-c", test_code], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Minimal AIOS test passed!")
            print(result.stdout)
            return True
        else:
            print(f"❌ Minimal AIOS test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error testing minimal AIOS: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Minimal AIOS Package Creator")
    print("=" * 40)
    
    success = create_minimal_aios()
    
    if success:
        print("\n🎉 Minimal AIOS package created successfully!")
        print("🚀 You can now run the AIOS Builder Agent.")
        print("\nNext steps:")
        print("1. Test: python debug_aios.py")
        print("2. Run AIOS Builder: python aios_builder_agent.py")
    else:
        print("\n💥 Minimal AIOS creation failed!")
        print("Check the logs above for details.")

if __name__ == "__main__":
    main()
