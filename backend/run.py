#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run the FastAPI server"""
import os
import sys

# Force unbuffered output
os.environ['PYTHONUNBUFFERED'] = '1'

# Change to backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)
sys.path.insert(0, '.')

def print_startup_message():
    """Print the startup message"""
    print("\n" + "="*70)
    print("[*] STARTING AUTOFILL AI SYSTEM SERVER")
    print("="*70)
    print("\n[+] Server khoi dong...")
    print("[*] Nhan CTRL+C de dung server")
    print("="*70 + "\n", flush=True)
    sys.stdout.flush()

if __name__ == "__main__":
    print_startup_message()
    
    # Import uvicorn here to avoid issues
    import uvicorn
    
    # Run the server with reload enabled for development
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )