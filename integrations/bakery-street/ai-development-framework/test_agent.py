#!/usr/bin/env python3
"""
Simple AIOS Agent Test
Testing basic agent creation and state management
"""

from aios.object import Object
from aios.state import State

def test_basic_agent():
    """Test basic agent creation"""
    try:
        agent = Object()
        print(f"✅ Agent created: {agent}")
        return agent
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return None

def test_state_management():
    """Test state management"""
    try:
        status = State(['idle', 'working', 'done'], name='status', default='idle')
        print(f"✅ Status created: {status}")
        print(f"   Current state: {status.current_state}")
        print(f"   Available states: {status.states}")
        return status
    except Exception as e:
        print(f"❌ State creation failed: {e}")
        return None

def test_agent_workflow():
    """Test basic agent workflow"""
    try:
        agent = test_basic_agent()
        status = test_state_management()
        
        if agent and status:
            print("\n🚀 Basic AIOS Agent Ready!")
            print("   Agent:", agent)
            print("   Status:", status)
            return True
        else:
            print("\n❌ Agent setup incomplete")
            return False
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== AIOS Agent Test ===")
    success = test_agent_workflow()
    if success:
        print("\n🎉 AIOS Agent Test PASSED!")
    else:
        print("\n💥 AIOS Agent Test FAILED!")
