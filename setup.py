#!/usr/bin/env python3
"""
ONE-CLICK SETUP - Run this first!
"""
import os
import sys
import subprocess
from pathlib import Path

def setup():
    print("🚀 SubHunterX Pro - ONE CLICK SETUP")
    
    # Create directories
    dirs = [
        'config', 'data/wordlists', 'data/screenshots', 
        'reports', 'subhunterx/core', 'subhunterx/database', 'subhunterx/utils', 'subhunterx/api',
        'frontend/static'
    ]
    
    for d in dirs:
        os.makedirs(d.replace('{', '').replace('}', ''), exist_ok=True)
    
    # Create empty __init__.py files
    init_files = [
        'subhunterx/__init__.py',
        'subhunterx/core/__init__.py',
        'subhunterx/database/__init__.py',
        'subhunterx/utils/__init__.py',
        'subhunterx/api/__init__.py',
        'config/__init__.py'
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
    
    print("✅ Structure created!")
    print("📦 Install: pip install -r requirements.txt")
    print("🎯 Run: python main.py example.com")

if __name__ == "__main__":
    setup()