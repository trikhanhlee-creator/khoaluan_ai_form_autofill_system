#!/usr/bin/env python
"""
Test script để simulate suggestions flow
"""
import json
import requests

API_BASE = "http://127.0.0.1:8000/api"
USER_ID = 1
FORM_ID = 1

print("=" * 60)
print("TESTING SUGGESTIONS FLOW (WITHOUT FILE UPLOAD)")
print("=" * 60)

# First create mock template by submitting to a fake template
# Or test with direct API calls

# Create test data that simulates form submission
print("\n[1] Simulating form submission with test data...")
print("    (Assuming template_id = 1 exists)")

template_id = 1
submission_data_1 = {
    "họ_và_tên": "Nguyễn Văn A",
    "năm_sinh": "1990",
    "địa_chỉ": "123 Đường ABC"
}

# Test direct API submission
print("\n[2] First form submission...")
response = requests.post(
    f"{API_BASE}/word/submit?template_id={template_id}&user_id={USER_ID}&form_id={FORM_ID}",
    json=submission_data_1
)

print(f"   Response: {response.status_code}")
if response.ok:
    data = response.json()
    print(f"   ✅ Submission success: {data}")
else:
    print(f"   ❌ Failed: {response.json()}")

# Check database
print("\n[2.1] Database state after first submission...")
from app.db.session import SessionLocal
from app.db.models import Entry, Suggestion, Field, WordTemplate

db = SessionLocal()

# Check if template exists
templates = db.query(WordTemplate).all()
print(f"   Templates: {len(templates)}")
for t in templates:
    print(f"     - Template {t.id}: {t.template_name}")

entries = db.query(Entry).all()
suggestions = db.query(Suggestion).all()
fields = db.query(Field).all()

print(f"   Entries: {len(entries)}")
for e in entries:
    field_obj = db.query(Field).filter(Field.id == e.field_id).first()
    field_name = field_obj.field_name if field_obj else "???"
    print(f"     - Entry {e.id}: Field '{field_name}' = '{e.value}'")

print(f"   Fields: {len(fields)}")
for f in fields:
    print(f"     - Field {f.id}: {f.field_name} (Form {f.form_id})")

print(f"   Suggestions: {len(suggestions)}")

# Test getting suggestions
print("\n[3] Getting suggestions for 'họ_và_tên' (should be empty - only 1 entry)...")
response = requests.get(
    f"{API_BASE}/suggestions/by-name?user_id={USER_ID}&field_name=họ_và_tên&form_id={FORM_ID}"
)

if response.ok:
    data = response.json()
    suggestions_list = data.get("suggestions", [])
    print(f"   Found {len(suggestions_list)} suggestions")
    for s in suggestions_list:
        print(f"     - '{s['value']}' (frequency: {s['frequency']})")
else:
    print(f"   ❌ Error: {response.json()}")

# Second submission with SAME data
print("\n[4] Second form submission (SAME DATA)...")
response = requests.post(
    f"{API_BASE}/word/submit?template_id={template_id}&user_id={USER_ID}&form_id={FORM_ID}",
    json=submission_data_1
)

if response.ok:
    print(f"   ✅ Submission success")
else:
    print(f"   ❌ Failed: {response.json()}")

# Check database again
print("\n[4.1] Database state after second submission...")
db.expire_all()
entries = db.query(Entry).all()
suggestions = db.query(Suggestion).all()

print(f"   Entries: {len(entries)}")
for e in entries:
    field_obj = db.query(Field).filter(Field.id == e.field_id).first()
    field_name = field_obj.field_name if field_obj else "???"
    print(f"     - Entry {e.id}: Field '{field_name}' = '{e.value}'")

print(f"   Suggestions: {len(suggestions)}")
for s in suggestions:
    field_obj = db.query(Field).filter(Field.id == s.field_id).first()
    field_name = field_obj.field_name if field_obj else "???"
    print(f"     - Suggestion {s.id}: Field '{field_name}' = '{s.suggested_value}' (freq: {s.frequency})")

# Test getting suggestions again
print("\n[5] Getting suggestions for 'họ_và_tên' (should have suggestions now)...")
response = requests.get(
    f"{API_BASE}/suggestions/by-name?user_id={USER_ID}&field_name=họ_và_tên&form_id={FORM_ID}"
)

if response.ok:
    data = response.json()
    suggestions_list = data.get("suggestions", [])
    print(f"   Found {len(suggestions_list)} suggestions")
    for s in suggestions_list:
        print(f"     - '{s['value']}' (frequency: {s['frequency']})")
    if len(suggestions_list) > 0:
        print("   ✅ SUCCESS! Suggestions appear after 2 submissions")
    else:
        print("   ❌ ERROR: Should have suggestions by now")
else:
    print(f"   ❌ Error: {response.json()}")

db.close()

print("\n" + "=" * 60)
print("TEST COMPLETE!")
print("=" * 60)
