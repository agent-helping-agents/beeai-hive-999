#!/usr/bin/env python3
"""
🕵️ Terminal 221b API Server

Standalone API server for Terminal 221b that allows external systems
(like BeeAI Hive 999) to communicate with the detective system.

Communication Patterns:
- REST API: Synchronous requests (investigations, simulations)
- WebSocket: Real-time streaming (agent thoughts, block updates)

Usage:
    python -m terminal_221b.api.server
"""

import asyncio
import json
import os
import sys
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Set
from uuid import uuid4

# Project root setup
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel, Field
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

# Terminal 221b imports
from terminal_221b.agents.advisor_deps import get_simulation_config
from terminal_221b.agents.detective_agent import (
    create_holmes, create_watson, create_mycroft, create_irene,
)
from terminal_221b.simulation.sim_server import SimServer


# ═══════════════════════════════════════════════════════════════════════════
# Pydantic Models
# ═══════════════════════════════════════════════════════════════════════════

class InvestigationRequest(BaseModel):
    query: str = Field(..., description="What to investigate")
    personality: str = Field(default="holmes", description="Detective personality")
    context: Dict[str, Any] = Field(default_factory=dict)


class InvestigationResponse(BaseModel):
    investigation_id: str
    status: str
    personality: str
    query: str
    result: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class HiveMessage(BaseModel):
    message_type: str
    payload: Dict[str, Any]
    source: str = "terminal_221b"
    timestamp: datetime = Field(default_factory=datetime.now)


# ═══════════════════════════════════════════════════════════════════════════
# State Management
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ServerState:
    agents: Dict[str, Any] = None
    investigations: Dict[str, InvestigationResponse] = None
    websocket_connections: Set[WebSocket] = None
    sim_server: Optional[SimServer] = None
    
    def __post_init__(self):
        if self.agents is None:
            self.agents = {}
        if self.investigations is None:
            self.investigations = {}
        if self.websocket_connections is None:
            self.websocket_connections = set()


state = ServerState()


# ═══════════════════════════════════════════════════════════════════════════
# FastAPI Application
# ═══════════════════════════════════════════════════════════════════════════

if HAS_FASTAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("🚀 Starting Terminal 221b API Server...")
        
        # Initialize simulation server
        state.sim_server = SimServer(port=8899, verbose=False)
        await state.sim_server.start()
        print(f"   ✅ SimServer running")
        
        # Pre-create detective agents
        deps = get_simulation_config()
        state.agents["holmes"] = await create_holmes(deps)
        state.agents["watson"] = await create_watson(deps)
        state.agents["mycroft"] = await create_mycroft(deps)
        state.agents["irene"] = await create_irene(deps)
        print(f"   ✅ 4 detectives ready")
        
        print(f"\n🕵️  Terminal 221b API: http://localhost:22181")
        yield
        
        # Shutdown
        print("\n🛑 Shutting down...")
        if state.sim_server:
            await state.sim_server.stop()

    app = FastAPI(
        title="Terminal 221b API",
        description="Sherlock Holmes-inspired Solana AI Detective",
        version="1.0.0",
        lifespan=lifespan,
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        return {
            "name": "Terminal 221b API",
            "version": "1.0.0",
            "detectives": list(state.agents.keys()),
            "docs": "/docs",
        }

    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "agents_ready": len(state.agents),
        }

    @app.post("/investigate", response_model=InvestigationResponse)
    async def investigate(request: InvestigationRequest, background_tasks: BackgroundTasks):
        """Start a new investigation"""
        investigation_id = str(uuid4())
        
        if request.personality not in state.agents:
            raise HTTPException(status_code=404, detail=f"Detective '{request.personality}' not found")
        
        response = InvestigationResponse(
            investigation_id=investigation_id,
            status="started",
            personality=request.personality,
            query=request.query,
        )
        state.investigations[investigation_id] = response
        
        # Run in background
        background_tasks.add_task(run_investigation, investigation_id, request)
        
        return response

    @app.get("/investigate/{investigation_id}", response_model=InvestigationResponse)
    async def get_investigation(investigation_id: str):
        if investigation_id not in state.investigations:
            raise HTTPException(status_code=404, detail="Investigation not found")
        return state.investigations[investigation_id]

    @app.post("/hive/message")
    async def receive_hive_message(message: HiveMessage):
        """Receive message from Hive 999"""
        print(f"📨 From Hive: {message.message_type}")
        
        if message.message_type == "investigation_request":
            req = InvestigationRequest(**message.payload)
            investigation_id = str(uuid4())
            asyncio.create_task(run_investigation(investigation_id, req))
            return {"status": "accepted", "investigation_id": investigation_id}
        
        return {"status": "received"}

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        state.websocket_connections.add(websocket)
        
        try:
            await websocket.send_json({
                "type": "connected",
                "detectives": list(state.agents.keys()),
            })
            
            while True:
                data = await websocket.receive_text()
                message = json.loads(data)
                response = await handle_ws_message(message)
                await websocket.send_json(response)
                
        except WebSocketDisconnect:
            state.websocket_connections.discard(websocket)

    async def run_investigation(investigation_id: str, request: InvestigationRequest):
        """Run investigation in background"""
        try:
            agent = state.agents.get(request.personality)
            inv = state.investigations[investigation_id]
            inv.status = "investigating"
            
            result = await agent.investigate(request.query)
            
            inv.status = "completed"
            inv.result = result
            
            # Broadcast to all connected WebSockets
            await broadcast({
                "type": "investigation_completed",
                "investigation_id": investigation_id,
                "result": result[:200] + "..." if len(result) > 200 else result,
            })
            
        except Exception as e:
            inv = state.investigations[investigation_id]
            inv.status = "error"
            inv.result = str(e)

    async def handle_ws_message(message: Dict) -> Dict:
        msg_type = message.get("type")
        
        if msg_type == "ping":
            return {"type": "pong"}
        
        elif msg_type == "investigate":
            personality = message.get("personality", "holmes")
            query = message.get("query", "")
            
            agent = state.agents.get(personality)
            if agent:
                result = await agent.investigate(query)
                return {"type": "result", "result": result}
            else:
                return {"type": "error", "message": f"Detective '{personality}' not found"}
        
        elif msg_type == "status":
            return {
                "type": "status",
                "agents": list(state.agents.keys()),
            }
        
        return {"type": "error", "message": f"Unknown: {msg_type}"}

    async def broadcast(message: Dict):
        disconnected = set()
        for ws in state.websocket_connections:
            try:
                await ws.send_json(message)
            except:
                disconnected.add(ws)
        state.websocket_connections -= disconnected


def main():
    if not HAS_FASTAPI:
        print("❌ Run: pip install fastapi uvicorn")
        sys.exit(1)
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=22181)


if __name__ == "__main__":
    main()
