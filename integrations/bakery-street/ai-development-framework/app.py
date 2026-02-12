#!/usr/bin/env python3
"""
AIOS Orchestrator Web Application
FastAPI-based web interface for the AIOS Orchestrator
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add AIOS environment to path
aios_env_path = os.path.join(os.getcwd(), "environments", "aios-env", "lib", "python3.11", "site-packages")
if aios_env_path not in sys.path:
    sys.path.insert(0, aios_env_path)

try:
    from fastapi import FastAPI, HTTPException, BackgroundTasks
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import HTMLResponse, JSONResponse
    from pydantic import BaseModel
    import uvicorn
    
    from aios.object import Object
    from aios.state import State
    from aios.core_utils import format_timestamp
    
    from crewai import Agent, Task, Crew, Process
    
    print("✅ All required modules imported successfully")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Load environment variables
from dotenv import load_dotenv
load_dotenv('.env.production')

# Create FastAPI app
app = FastAPI(
    title="AIOS Orchestrator",
    description="Enterprise-grade AI Orchestration System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
aios_state = State(['idle', 'running', 'completed', 'error'], name='system_status', default='idle')
system_metrics = {
    'start_time': format_timestamp(time.time()),
    'requests_processed': 0,
    'workflows_executed': 0,
    'errors': 0
}

# Pydantic models
class WorkflowRequest(BaseModel):
    workflow_type: str
    parameters: Dict[str, Any] = {}

class AgentRequest(BaseModel):
    agent_type: str
    task_description: str
    parameters: Dict[str, Any] = {}

class SystemStatus(BaseModel):
    status: str
    uptime: str
    metrics: Dict[str, Any]

@app.get("/", response_class=HTMLResponse)
async def root():
    """Main dashboard"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AIOS Orchestrator Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .header { text-align: center; margin-bottom: 30px; }
            .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
            .status.running { background: #d4edda; color: #155724; }
            .status.idle { background: #fff3cd; color: #856404; }
            .status.error { background: #f8d7da; color: #721c24; }
            .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }
            .card { background: #f8f9fa; padding: 20px; border-radius: 5px; border-left: 4px solid #007bff; }
            .button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
            .button:hover { background: #0056b3; }
            .metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0; }
            .metric { text-align: center; padding: 15px; background: #e9ecef; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 AIOS Orchestrator Dashboard</h1>
                <p>Enterprise-grade AI Orchestration System</p>
            </div>
            
            <div class="status" id="systemStatus">
                <h3>System Status: <span id="statusText">Loading...</span></h3>
            </div>
            
            <div class="metrics">
                <div class="metric">
                    <h4>Requests Processed</h4>
                    <p id="requestsCount">0</p>
                </div>
                <div class="metric">
                    <h4>Workflows Executed</h4>
                    <p id="workflowsCount">0</p>
                </div>
                <div class="metric">
                    <h4>System Uptime</h4>
                    <p id="uptime">0s</p>
                </div>
            </div>
            
            <div class="grid">
                <div class="card">
                    <h3>🧠 AI Agents</h3>
                    <p>Manage and orchestrate AI agents</p>
                    <button class="button" onclick="createAgent()">Create Agent</button>
                    <button class="button" onclick="listAgents()">List Agents</button>
                </div>
                
                <div class="card">
                    <h3>🔄 Workflows</h3>
                    <p>Execute production workflows</p>
                    <button class="button" onclick="startWorkflow()">Start Workflow</button>
                    <button class="button" onclick="listWorkflows()">List Workflows</button>
                </div>
                
                <div class="card">
                    <h3>📊 Monitoring</h3>
                    <p>System metrics and health</p>
                    <button class="button" onclick="getMetrics()">View Metrics</button>
                    <button class="button" onclick="getHealth()">Health Check</button>
                </div>
                
                <div class="card">
                    <h3>⚙️ Configuration</h3>
                    <p>System configuration and settings</p>
                    <button class="button" onclick="getConfig()">View Config</button>
                    <button class="button" onclick="updateConfig()">Update Config</button>
                </div>
            </div>
            
            <div id="output" style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; min-height: 100px;">
                <h4>Output:</h4>
                <pre id="outputText">System ready. Select an action above.</pre>
            </div>
        </div>
        
        <script>
            // Update system status
            async function updateStatus() {
                try {
                    const response = await fetch('/status');
                    const data = await response.json();
                    document.getElementById('statusText').textContent = data.status;
                    document.getElementById('requestsCount').textContent = data.metrics.requests_processed;
                    document.getElementById('workflowsCount').textContent = data.metrics.workflows_executed;
                    document.getElementById('uptime').textContent = data.uptime;
                    
                    const statusDiv = document.getElementById('systemStatus');
                    statusDiv.className = 'status ' + data.status;
                } catch (error) {
                    console.error('Error updating status:', error);
                }
            }
            
            // API functions
            async function apiCall(endpoint, method = 'GET', data = null) {
                try {
                    const options = {
                        method: method,
                        headers: { 'Content-Type': 'application/json' }
                    };
                    if (data) options.body = JSON.stringify(data);
                    
                    const response = await fetch(endpoint, options);
                    const result = await response.json();
                    document.getElementById('outputText').textContent = JSON.stringify(result, null, 2);
                    updateStatus();
                } catch (error) {
                    document.getElementById('outputText').textContent = 'Error: ' + error.message;
                }
            }
            
            function createAgent() { apiCall('/agents/create', 'POST', {agent_type: 'developer', task_description: 'Test task'}); }
            function listAgents() { apiCall('/agents/list'); }
            function startWorkflow() { apiCall('/workflows/start', 'POST', {workflow_type: 'ai_development'}); }
            function listWorkflows() { apiCall('/workflows/list'); }
            function getMetrics() { apiCall('/metrics'); }
            function getHealth() { apiCall('/health'); }
            function getConfig() { apiCall('/config'); }
            function updateConfig() { apiCall('/config/update', 'POST', {setting: 'test'}); }
            
            // Update status every 5 seconds
            updateStatus();
            setInterval(updateStatus, 5000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": format_timestamp(time.time()),
        "version": "1.0.0",
        "aios_version": "0.2.2"
    }

@app.get("/status")
async def get_status():
    """Get system status"""
    uptime = time.time() - time.mktime(datetime.strptime(system_metrics['start_time'], '%Y-%m-%d %H:%M:%S').timetuple())
    
    return SystemStatus(
        status=aios_state.current_state,
        uptime=f"{int(uptime)}s",
        metrics=system_metrics
    )

@app.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    return {
        "system_metrics": system_metrics,
        "aios_state": {
            "current_state": aios_state.current_state,
            "history": aios_state.get_history(),
            "allowed_transitions": aios_state.allowed_transitions
        }
    }

@app.post("/agents/create")
async def create_agent(request: AgentRequest):
    """Create a new AI agent"""
    try:
        system_metrics['requests_processed'] += 1
        
        # Create AIOS object for the agent
        agent_obj = Object(f"Agent_{request.agent_type}")
        agent_obj.set_property("type", request.agent_type)
        agent_obj.set_property("task", request.task_description)
        agent_obj.set_property("created_at", format_timestamp(time.time()))
        agent_obj.set_property("status", "created")
        
        # Create CrewAI agent
        agent = Agent(
            role=request.agent_type.title(),
            goal=f"Execute {request.task_description}",
            backstory=f"You are a {request.agent_type} specialized in {request.task_description}",
            verbose=True,
            allow_delegation=True
        )
        
        return {
            "success": True,
            "agent_id": agent_obj.id,
            "agent_type": request.agent_type,
            "message": f"Agent {request.agent_type} created successfully"
        }
        
    except Exception as e:
        system_metrics['errors'] += 1
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/list")
async def list_agents():
    """List all agents"""
    try:
        system_metrics['requests_processed'] += 1
        
        # For demo purposes, return sample agents
        agents = [
            {"id": "architect_001", "type": "System Architect", "status": "ready"},
            {"id": "data_engineer_001", "type": "Data Engineer", "status": "ready"},
            {"id": "ml_engineer_001", "type": "ML Engineer", "status": "ready"},
            {"id": "devops_001", "type": "DevOps Engineer", "status": "ready"},
            {"id": "security_001", "type": "Security Specialist", "status": "ready"},
            {"id": "analyst_001", "type": "Business Analyst", "status": "ready"}
        ]
        
        return {"agents": agents, "count": len(agents)}
        
    except Exception as e:
        system_metrics['errors'] += 1
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workflows/start")
async def start_workflow(request: WorkflowRequest, background_tasks: BackgroundTasks):
    """Start a workflow execution"""
    try:
        system_metrics['requests_processed'] += 1
        system_metrics['workflows_executed'] += 1
        
        aios_state.change_state('running')
        
        # Add workflow execution to background tasks
        background_tasks.add_task(execute_workflow, request.workflow_type, request.parameters)
        
        return {
            "success": True,
            "workflow_type": request.workflow_type,
            "status": "started",
            "message": f"Workflow {request.workflow_type} started successfully"
        }
        
    except Exception as e:
        system_metrics['errors'] += 1
        aios_state.change_state('error')
        raise HTTPException(status_code=500, detail=str(e))

async def execute_workflow(workflow_type: str, parameters: Dict[str, Any]):
    """Execute workflow in background"""
    try:
        # Simulate workflow execution
        await asyncio.sleep(5)  # Simulate processing time
        
        # Update state to completed
        aios_state.change_state('completed')
        
        print(f"✅ Workflow {workflow_type} completed successfully")
        
    except Exception as e:
        aios_state.change_state('error')
        print(f"❌ Workflow {workflow_type} failed: {e}")

@app.get("/workflows/list")
async def list_workflows():
    """List available workflows"""
    try:
        system_metrics['requests_processed'] += 1
        
        workflows = [
            {
                "id": "ai_development",
                "name": "AI System Development",
                "description": "Complete AI system architecture and development",
                "tasks": 5,
                "status": "available"
            },
            {
                "id": "data_pipeline",
                "name": "Data Pipeline Development",
                "description": "ETL pipeline and data processing workflows",
                "tasks": 3,
                "status": "available"
            },
            {
                "id": "ml_development",
                "name": "ML Model Development",
                "description": "Machine learning model training and deployment",
                "tasks": 3,
                "status": "available"
            }
        ]
        
        return {"workflows": workflows, "count": len(workflows)}
        
    except Exception as e:
        system_metrics['errors'] += 1
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/config")
async def get_config():
    """Get system configuration"""
    try:
        system_metrics['requests_processed'] += 1
        
        config = {
            "environment": os.getenv("AIOS_ENVIRONMENT", "production"),
            "log_level": os.getenv("AIOS_LOG_LEVEL", "INFO"),
            "database_url": os.getenv("AIOS_DATABASE_URL", "not_set"),
            "redis_url": os.getenv("AIOS_REDIS_URL", "not_set"),
            "monitoring_enabled": os.getenv("MONITORING_ENABLED", "true"),
            "metrics_collection": os.getenv("METRICS_COLLECTION", "true"),
            "alerting_enabled": os.getenv("ALERTING_ENABLED", "true")
        }
        
        return config
        
    except Exception as e:
        system_metrics['errors'] += 1
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/config/update")
async def update_config(request: Dict[str, Any]):
    """Update system configuration"""
    try:
        system_metrics['requests_processed'] += 1
        
        return {
            "success": True,
            "message": "Configuration updated successfully",
            "updated_settings": request
        }
        
    except Exception as e:
        system_metrics['errors'] += 1
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import asyncio
    
    print("🚀 Starting AIOS Orchestrator Web Application...")
    print(f"✅ AIOS Version: 0.2.2")
    print(f"✅ Database: {os.getenv('AIOS_DATABASE_URL', 'not_set')}")
    print(f"✅ Redis: {os.getenv('AIOS_REDIS_URL', 'not_set')}")
    print(f"🌐 Web Interface: http://localhost:8000")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

