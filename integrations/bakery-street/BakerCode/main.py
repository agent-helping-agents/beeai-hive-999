#!/usr/bin/env python3
"""
BakerCode Platform - Main Entry Point
Nuclear option for Railway deployment
"""

import os
import sys
import subprocess

def main():
    """Main entry point for BakerCode platform"""
    print("🍞 BakerCode Platform Starting...")
    
    # Set up environment
    port = os.environ.get('PORT', '8000')
    
    # Change to the correct directory
    os.chdir('codex-superlab-recreation')
    
    # Start the web dashboard with gunicorn
    cmd = [
        'gunicorn',
        'web_dashboard:app',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '2',
        '--timeout', '120',
        '--access-logfile', '-',
        '--error-logfile', '-',
        '--log-level', 'info'
    ]
    
    print(f"🚀 Starting gunicorn on port {port}...")
    print(f"Command: {' '.join(cmd)}")
    
    # Execute gunicorn
    subprocess.exec(cmd)

if __name__ == '__main__':
    main()