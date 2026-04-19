#!/usr/bin/env python
"""Test both XLSX and XLS support"""
import requests
from pathlib import Path

print("\n" + "="*70)
print("TEST: Both XLSX and XLS Support")
print("="*70 + "\n")

# Test 1: XLSX
print("1. Testing XLSX file (sample_data.xlsx)...")
sample_path = Path('uploads/sample_data.xlsx')
if sample_path.exists():
    with open(sample_path, 'rb') as f:
        files = {'file': ('sample_data.xlsx', f)}
        response = requests.post('http://127.0.0.1:8000/api/excel/upload', files=files)
    
    print(f"   Status: {response.status_code}")
    data = response.json()
    if response.status_code == 200:
        print(f"   ✓ SUCCESS")
        print(f"   Rows: {data.get('total_rows')}")
    else:
        print(f"   ✗ ERROR: {data.get('detail')}")
else:
    print(f"   ! File not found")

# Test 2: XLS
print("\n2. Testing XLS file (test_file.xls)...")
xls_path = Path('test_file.xls')
if xls_path.exists():
    with open(xls_path, 'rb') as f:
        files = {'file': ('test_file.xls', f)}
        response = requests.post('http://127.0.0.1:8000/api/excel/upload', files=files)
    
    print(f"   Status: {response.status_code}")
    data = response.json()
    if response.status_code == 200:
        print(f"   ✓ SUCCESS")
        print(f"   Rows: {data.get('total_rows')}")
    else:
        print(f"   ✗ ERROR: {data.get('detail')}")
else:
    print(f"   ! File not found")

print("\n" + "="*70 + "\n")
