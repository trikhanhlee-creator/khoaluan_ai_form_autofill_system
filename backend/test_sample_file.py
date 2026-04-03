#!/usr/bin/env python
"""Test sample file upload"""
import requests
from pathlib import Path

sample_path = Path('uploads/sample_data.xlsx')
with open(sample_path, 'rb') as f:
    files = {'file': ('sample_data.xlsx', f)}
    response = requests.post('http://127.0.0.1:8000/api/excel/upload', files=files)

data = response.json()
print(f"Status Code: {response.status_code}")
print(f"Success: {data.get('status') == 'success'}")
print(f"Message: {data.get('message')}")
print(f"Total Rows: {data.get('total_rows')}")
print(f"Headers: {data.get('headers')}")
