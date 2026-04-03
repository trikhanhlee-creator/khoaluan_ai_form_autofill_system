#!/usr/bin/env python3
"""Test form creation and rendering with the current parser"""
import sys
import os
import json
sys.path.insert(0, '.')

from docx import Document
from docx.shared import Pt
from app.db.session import SessionLocal
from app.db.models import WordTemplate, Field
import requests
import time

# Create test file with problematic characters
doc = Document()

# Add fields with various separators/quotes
test_fields = [
    'Họ và tên.....',
    'Lớp',
    'Trường(...)',
    'Địa chỉ""',
    'Email:',
    'Số điện thoại',
]

for field_text in test_fields:
    doc.add_paragraph(field_text)

# Save file
test_file_path = 'test_form_creation.docx'
doc.save(test_file_path)
print(f"✓ Created test file: {test_file_path}\n")

# Wait for server to be ready
print("Waiting for server to start...")
time.sleep(1)

# Upload file
print("Uploading file...")
with open(test_file_path, 'rb') as f:
    response = requests.post(
        f'http://localhost:8000/api/word/upload?user_id=1',
        files={'file': f}
    )

if response.status_code != 200:
    print(f"❌ Upload failed: {response.status_code}")
    print(response.text)
    exit(1)

result = response.json()
template_id = result['template_id']
print(f"✅ Upload successful!")
print(f"   Template ID: {template_id}")
print(f"   Fields: {result['fields_count']}\n")

# Get template detail with enriched fields
print("Retrieving template details...")
response = requests.get(
    f'http://localhost:8000/api/word/template/{template_id}?user_id=1&form_id=1'
)

if response.status_code != 200:
    print(f"❌ Retrieval failed: {response.status_code}")
    print(response.text)
    exit(1)

template = response.json()
print(f"✅ Template retrieved!")
print(f"   Name: {template['name']}")
print(f"   Fields count: {len(template['fields'])}\n")

# Check fields
print("=" * 60)
print("FIELDS IN TEMPLATE:")
print("=" * 60)
for idx, field in enumerate(template['fields']):
    has_quotes = '"' in field.get('label', '')
    label_repr = repr(field.get('label', ''))
    field_id = field.get('field_id', -1)
    
    status = "❌ HAS QUOTES" if has_quotes else "✅"
    status += f" | field_id={field_id}"
    
    print(f"\n{idx+1}. {status}")
    print(f"   Label: {label_repr}")
    print(f"   Name: {field.get('name')}")
    print(f"   Field ID: {field_id}")

print("\n" + "=" * 60)

# Clean up
if os.path.exists(test_file_path):
    os.remove(test_file_path)
    print(f"\n✓ Cleaned up test file")
