#!/usr/bin/env python3
"""Test secure API"""
import asyncio
import aiohttp

async def test():
    base_url = "http://localhost:22181"
    
    async with aiohttp.ClientSession() as session:
        # 1. Health check
        print("1. Health check...")
        async with session.get(f"{base_url}/health") as resp:
            print(f"   Status: {resp.status}")
            print(f"   Body: {await resp.json()}")
        
        # 2. Login
        print("\n2. Login...")
        async with session.post(
            f"{base_url}/token",
            json={"username": "hive", "password": "HiveConnect2024!"}
        ) as resp:
            print(f"   Status: {resp.status}")
            data = await resp.json()
            print(f"   Got token: {data.get('access_token', 'ERROR')[:50]}...")
            token = data.get('access_token')
        
        # 3. Get detectives
        print("\n3. Get detectives...")
        async with session.get(
            f"{base_url}/detectives",
            headers={"Authorization": f"Bearer {token}"}
        ) as resp:
            print(f"   Status: {resp.status}")
            print(f"   Body: {await resp.json()}")
        
        # 4. Try admin endpoint (should fail)
        print("\n4. Try admin endpoint (should fail)...")
        async with session.get(
            f"{base_url}/admin/stats",
            headers={"Authorization": f"Bearer {token}"}
        ) as resp:
            print(f"   Status: {resp.status}")
            print(f"   Body: {await resp.text()}")
        
        # 5. Try investigation
        print("\n5. Start investigation...")
        try:
            async with session.post(
                f"{base_url}/investigate",
                headers={"Authorization": f"Bearer {token}"},
                json={"query": "Test query", "personality": "holmes"}
            ) as resp:
                print(f"   Status: {resp.status}")
                text = await resp.text()
                print(f"   Body: {text[:200]}")
        except Exception as e:
            print(f"   Error: {e}")

asyncio.run(test())
