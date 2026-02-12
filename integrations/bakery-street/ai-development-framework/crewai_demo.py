#!/usr/bin/env python3
"""
CrewAI Demonstration - Multi-Agent Orchestration
Shows how CrewAI can orchestrate multiple AI agents to work together
"""

import os
import sys
from pathlib import Path

# Add AIOS environment to path
aios_env_path = os.path.join(os.getcwd(), "environments", "aios-env", "lib", "python3.11", "site-packages")
if aios_env_path not in sys.path:
    sys.path.insert(0, aios_env_path)

try:
    from crewai import Agent, Task, Crew, Process
    from aios.object import Object
    from aios.state import State
    print("✅ CrewAI and AIOS imported successfully")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

def create_ai_development_crew():
    """Create a crew of AI agents for development tasks"""
    
    print("🧠 Creating AI Development Crew...")
    print("=" * 50)
    
    # Create AIOS objects for our agents
    project_manager = Object("ProjectManager")
    project_manager.set_property("role", "Project Manager")
    project_manager.set_property("expertise", "Project planning and coordination")
    
    developer = Object("Developer")
    developer.set_property("role", "Software Developer")
    developer.set_property("expertise", "Python, AI, and system development")
    
    tester = Object("Tester")
    tester.set_property("role", "Quality Assurance")
    tester.set_property("expertise", "Testing and validation")
    
    # Create CrewAI agents
    project_manager_agent = Agent(
        role="Project Manager",
        goal="Plan and coordinate AI development projects",
        backstory="""You are an experienced project manager specializing in AI development projects. 
        You excel at breaking down complex projects into manageable tasks and coordinating team efforts.""",
        verbose=True,
        allow_delegation=True
    )
    
    developer_agent = Agent(
        role="Software Developer",
        goal="Develop high-quality AI systems and applications",
        backstory="""You are a skilled software developer with expertise in Python, AI frameworks, 
        and system architecture. You love solving complex problems and building robust solutions.""",
        verbose=True,
        allow_delegation=True
    )
    
    tester_agent = Agent(
        role="Quality Assurance Engineer",
        goal="Ensure the quality and reliability of AI systems",
        backstory="""You are a meticulous QA engineer who specializes in testing AI systems. 
        You have a keen eye for detail and ensure everything works perfectly before deployment.""",
        verbose=True,
        allow_delegation=True
    )
    
    # Create tasks for the crew
    planning_task = Task(
        description="""Analyze the current AI development stack and create a project plan for 
        building an advanced AI orchestration system. Include:
        1. Current capabilities assessment
        2. Missing components identification
        3. Development roadmap
        4. Resource requirements""",
        agent=project_manager_agent,
        expected_output="A comprehensive project plan document"
    )
    
    development_task = Task(
        description="""Based on the project plan, design and implement a core component of the 
        AI orchestration system. Focus on:
        1. System architecture design
        2. Core functionality implementation
        3. Integration with existing AIOS components
        4. Documentation and examples""",
        agent=developer_agent,
        expected_output="Working code with documentation"
    )
    
    testing_task = Task(
        description="""Test the developed component thoroughly. Create a comprehensive testing plan 
        and execute it. Focus on:
        1. Functionality testing
        2. Integration testing
        3. Performance testing
        4. Security testing""",
        agent=tester_agent,
        expected_output="Testing report with results and recommendations"
    )
    
    # Create the crew
    crew = Crew(
        agents=[project_manager_agent, developer_agent, tester_agent],
        tasks=[planning_task, development_task, testing_task],
        process=Process.sequential,
        verbose=True
    )
    
    return crew

def run_aios_integration_demo():
    """Demonstrate AIOS integration with CrewAI"""
    
    print("\n🔧 AIOS Integration Demo...")
    print("=" * 50)
    
    # Create AIOS state for the demo
    demo_state = State(['planning', 'development', 'testing', 'complete'], 
                      name='demo_status', default='planning')
    
    print(f"✅ Demo state created: {demo_state}")
    
    # Simulate workflow progression
    print("\n📋 Simulating AIOS-CrewAI workflow...")
    
    demo_state.change_state('development')
    print(f"✅ State changed to: {demo_state.current_state}")
    
    demo_state.change_state('testing')
    print(f"✅ State changed to: {demo_state.current_state}")
    
    demo_state.change_state('complete')
    print(f"✅ State changed to: {demo_state.current_state}")
    
    # Show state information
    info = demo_state.get_current_state_info()
    print(f"\n📊 Demo workflow completed in {info['uptime']:.2f} seconds")
    print(f"   Total transitions: {len(demo_state.get_history())}")
    
    return True

def main():
    """Main demonstration function"""
    
    print("🚀 CrewAI + AIOS Integration Demonstration")
    print("=" * 60)
    
    try:
        # Demo 1: AIOS Integration
        print("\n🎯 Demo 1: AIOS State Management")
        aios_success = run_aios_integration_demo()
        
        # Demo 2: CrewAI Setup (without running full crew to avoid API calls)
        print("\n🎯 Demo 2: CrewAI Agent Setup")
        crew = create_ai_development_crew()
        print(f"✅ Crew created with {len(crew.agents)} agents")
        print(f"✅ {len(crew.tasks)} tasks defined")
        
        # Show agent details
        for i, agent in enumerate(crew.agents, 1):
            print(f"   Agent {i}: {agent.role}")
            print(f"      Goal: {agent.goal}")
        
        # Show task details
        for i, task in enumerate(crew.tasks, 1):
            print(f"   Task {i}: {task.agent.role}")
            print(f"      Description: {task.description[:100]}...")
        
        print("\n" + "=" * 60)
        print("🎉 Demonstration Complete!")
        print("\n🚀 What You Can Do Next:")
        print("1. Run the full crew: crew.kickoff()")
        print("2. Create custom agents for specific tasks")
        print("3. Integrate with your existing AIOS workflows")
        print("4. Build production AI orchestration systems")
        
        return True
        
    except Exception as e:
        print(f"❌ Demonstration failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 Your AI development stack is now ready for advanced multi-agent orchestration!")
    else:
        print("\n💥 There were issues with the demonstration.")
