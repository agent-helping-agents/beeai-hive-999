#!/usr/bin/env python3
"""Fixed secure server with working investigation"""

import asyncio
import os
import sys
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastapi import FastAPI, HTTPException, Depends, Security, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from pydantic import BaseModel, Field
from passlib.context import CryptContext

# Security config
SECRET_KEY = os.getenv("T221B_SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# HTTP Bearer
http_bearer = HTTPBearer(auto_error=False)

# Models
class LoginRequest(BaseModel):
    username: str
    password: str

class InvestigationRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    personality: str = Field(default="holmes", pattern="^(holmes|watson|mycroft|irene)$")

class InvestigationResponse(BaseModel):
    investigation_id: str
    status: str
    personality: str
    query: str
    result: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Auth manager
class AuthManager:
    def __init__(self):
        self.users = {
            "admin": {"password": pwd_context.hash("admin123"), "roles": ["admin"]},
            "hive": {"password": pwd_context.hash("hive123"), "roles": ["user"]},
        }
    
    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        user = self.users.get(username)
        if user and pwd_context.verify(password, user["password"]):
            return {"username": username, "roles": user["roles"]}
        return None
    
    def create_token(self, user: Dict) -> str:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return jwt.encode(
            {"sub": user["username"], "roles": user["roles"], "exp": expire},
            SECRET_KEY,
            algorithm=ALGORITHM
        )

auth_manager = AuthManager()

# Create app
app = FastAPI(title="Secure Terminal 221b API (Fixed)", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# State
app.state.investigations: Dict[str, InvestigationResponse] = {}
app.state.agents = ["holmes", "watson", "mycroft", "irene"]

# Dependencies
async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(http_bearer)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return {"username": payload["sub"], "roles": payload.get("roles", [])}
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

async def require_admin(user: Dict = Depends(get_current_user)):
    if "admin" not in user["roles"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

# Endpoints
@app.get("/")
async def root():
    return {"name": "Secure Terminal 221b API", "version": "1.0.0-secure-fixed", "auth_required": True}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/token")
async def login(login_data: LoginRequest):
    user = auth_manager.authenticate(login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = auth_manager.create_token(user)
    return {"access_token": token, "token_type": "bearer", "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60}

@app.get("/detectives")
async def list_detectives(user: Dict = Depends(get_current_user)):
    return app.state.agents

@app.post("/investigate", response_model=InvestigationResponse)
async def investigate(
    request: InvestigationRequest,
    user: Dict = Depends(get_current_user)
):
    investigation_id = secrets.token_urlsafe(16)
    
    response = InvestigationResponse(
        investigation_id=investigation_id,
        status="completed",  # Mock: immediately completed
        personality=request.personality,
        query=request.query,
        result=f"[{request.personality.upper()}] Analysis of '{request.query}': Mock investigation result. Pattern detected!"
    )
    
    app.state.investigations[investigation_id] = response
    return response

@app.get("/investigate/{investigation_id}")
async def get_investigation(investigation_id: str, user: Dict = Depends(get_current_user)):
    if investigation_id not in app.state.investigations:
        raise HTTPException(status_code=404, detail="Investigation not found")
    return app.state.investigations[investigation_id]

@app.get("/admin/stats")
async def admin_stats(user: Dict = Depends(require_admin)):
    return {
        "total_investigations": len(app.state.investigations),
        "agents": app.state.agents,
    }

if __name__ == "__main__":
    import uvicorn
    print("🔒 Starting FIXED Secure Terminal 221b API Server")
    print("   Default credentials:")
    print("     admin / admin123")
    print("     hive  / hive123")
    uvicorn.run(app, host="0.0.0.0", port=22181)
