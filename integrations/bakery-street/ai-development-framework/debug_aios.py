#!/usr/bin/env python3
"""
AIOS Debug and Test Script
Comprehensive testing of AIOS installation and functionality
"""

import sys
import os

# Add the AIOS environment to the path
aios_env_path = os.path.join(os.getcwd(), "environments", "aios-env", "lib", "python3.11", "site-packages")
if aios_env_path not in sys.path:
    sys.path.insert(0, aios_env_path)

def test_aios_imports():
    """Test basic AIOS imports"""
    print("🧪 Testing AIOS imports...")
    
    try:
        import aios
        print(f"✅ AIOS {aios.__version__} imported successfully")
        
        from aios.object import Object
        print(f"✅ Object class imported: {Object}")
        
        from aios.state import State
        print(f"✅ State class imported: {State}")
        
        from aios.core_utils import create_agent, create_agent_from_template
        print(f"✅ Core utilities imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_object_functionality():
    """Test Object class functionality"""
    print("\n🧪 Testing Object class...")
    
    try:
        from aios.object import Object
        
        # Test basic creation
        obj = Object("TestAgent")
        print(f"✅ Object created: {obj}")
        
        # Test properties
        obj.set_property("type", "research")
        obj.set_property("capabilities", ["search", "analyze"])
        print(f"✅ Properties set: {obj.get_all_properties()}")
        
        # Test property retrieval
        agent_type = obj.get_property("type")
        print(f"✅ Property retrieved: type = {agent_type}")
        
        # Test property checking
        has_type = obj.has_property("type")
        print(f"✅ Property check: has_type = {has_type}")
        
        # Test cloning
        clone = obj.clone("TestAgentClone")
        print(f"✅ Object cloned: {clone}")
        
        # Test info export
        info = obj.get_info()
        print(f"✅ Object info exported: {len(info)} fields")
        
        return True
    except Exception as e:
        print(f"❌ Object test failed: {e}")
        return False

def test_state_functionality():
    """Test State class functionality"""
    print("\n🧪 Testing State class...")
    
    try:
        from aios.state import State
        
        # Test basic creation
        state = State(['idle', 'working', 'done'], name='status', default='idle')
        print(f"✅ State created: {state}")
        print(f"✅ Current state: {state.current_state}")
        
        # Test state transitions
        state.change_state('working')
        print(f"✅ State changed to: {state.current_state}")
        
        state.change_state('done')
        print(f"✅ State changed to: {state.current_state}")
        
        # Test history
        history = state.get_history()
        print(f"✅ State history: {len(history)} transitions")
        
        # Test validation
        valid_states = state.get_valid_states()
        print(f"✅ Valid states: {valid_states}")
        
        # Test transition stats
        stats = state.get_transition_stats()
        print(f"✅ Transition stats: {stats}")
        
        # Test state info
        info = state.get_current_state_info()
        print(f"✅ State info exported: {len(info)} fields")
        
        # Test reset
        state.reset()
        print(f"✅ State reset to: {state.current_state}")
        
        return True
    except Exception as e:
        print(f"❌ State test failed: {e}")
        return False

def test_utility_functions():
    """Test utility functions"""
    print("\n🧪 Testing utility functions...")
    
    try:
        from aios.core_utils import (
            create_agent, create_agent_from_template, 
            validate_state_transition, format_timestamp,
            generate_agent_id, validate_agent_config
        )
        
        # Test agent creation
        agent = create_agent("TestAgent", "research", ["search", "analyze"])
        print(f"✅ Agent created: {agent['name']} ({agent['type']})")
        
        # Test template agent
        template_agent = create_agent_from_template("researcher", name="ResearchAgent")
        print(f"✅ Template agent: {template_agent['name']} ({template_agent['type']})")
        
        # Test state transition validation
        allowed_transitions = [['idle', 'working'], ['working', 'done']]
        is_valid = validate_state_transition('idle', 'working', allowed_transitions)
        print(f"✅ Transition validation: idle->working = {is_valid}")
        
        # Test timestamp formatting
        timestamp = format_timestamp(1756635133.0)
        print(f"✅ Timestamp formatted: {timestamp}")
        
        # Test agent ID generation
        agent_id = generate_agent_id("test")
        print(f"✅ Agent ID generated: {agent_id}")
        
        # Test config validation
        config_valid = validate_agent_config(agent)
        print(f"✅ Config validation: {config_valid}")
        
        return True
    except Exception as e:
        print(f"❌ Utility test failed: {e}")
        return False

def test_advanced_features():
    """Test advanced AIOS features"""
    print("\n🧪 Testing advanced features...")
    
    try:
        from aios.object import Object
        from aios.state import State
        from aios.core_utils import export_agent_state
        
        # Create complex agent
        agent = Object("AdvancedAgent")
        agent.set_property("type", "multi-purpose")
        agent.set_property("capabilities", ["planning", "execution", "monitoring"])
        agent.set_property("metadata", {"version": "2.0", "author": "AIOS"})
        
        # Create state with allowed transitions
        state = State(['planning', 'executing', 'monitoring', 'completed'])
        state.set_allowed_transitions([
            ['planning', 'executing'],
            ['executing', 'monitoring'],
            ['monitoring', 'completed'],
            ['monitoring', 'executing']  # Allow going back
        ])
        
        # Test complex state machine
        print(f"✅ Complex agent created: {agent}")
        print(f"✅ Complex state created: {state}")
        
        # Test state machine flow
        state.change_state('executing')
        state.change_state('monitoring')
        state.change_state('executing')  # Go back
        state.change_state('monitoring')
        state.change_state('completed')
        
        print(f"✅ State machine flow completed: {state.current_state}")
        print(f"✅ Total transitions: {len(state.get_history())}")
        
        # Test export functionality
        exported = export_agent_state(agent, state)
        print(f"✅ State exported: {len(exported)} sections")
        
        return True
    except Exception as e:
        print(f"❌ Advanced features test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 AIOS Comprehensive Test Suite")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_aios_imports),
        ("Object Functionality", test_object_functionality),
        ("State Functionality", test_state_functionality),
        ("Utility Functions", test_utility_functions),
        ("Advanced Features", test_advanced_features)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! AIOS is working perfectly!")
        print("\n🚀 Your AIOS system is ready for:")
        print("   • Building AI agents")
        print("   • Running the AIOS Builder Agent")
        print("   • Advanced AI development")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
