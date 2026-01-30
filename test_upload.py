#!/usr/bin/env python3
"""Test script to upload Word file"""

import requests
import os

API_BASE = "http://127.0.0.1:8000/api"
USER_ID = 1

# Test file
test_file = r"C:\Users\KHANH\Downloads\testform.docx"

if not os.path.exists(test_file):
    print(f"❌ File not found: {test_file}")
    exit(1)

print(f"📤 Uploading {os.path.basename(test_file)}...")

try:
    with open(test_file, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f"{API_BASE}/word/upload?user_id={USER_ID}",
            files=files
        )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    
    if response.ok:
        print(f"✅ Upload successful!")
        print(f"   Template ID: {data.get('template_id')}")
        print(f"   Fields found: {data.get('fields_count')}")
        print(f"   Fields: {[f['label'] for f in data.get('fields', [])]}")
    else:
        print(f"❌ Error: {data.get('detail')}")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
