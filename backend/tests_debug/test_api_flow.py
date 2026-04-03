#!/usr/bin/env python
"""
Test API suggestions flow
"""
import requests
import json
import time
from datetime import datetime

API_BASE = "http://127.0.0.1:8000/api"
USER_ID = 1
FORM_ID = 1

print("=" * 80)
print("API SUGGESTIONS FLOW TEST")
print("=" * 80)
print(f"API Base: {API_BASE}")
print(f"User ID: {USER_ID}, Form ID: {FORM_ID}")

# Test 1: Check if API is responding
print("\n[1] Testing API connectivity...")
try:
    response = requests.get(f"{API_BASE}/suggestions?user_id={USER_ID}&field_id=1", timeout=5)
    print(f"✓ API is responding (status: {response.status_code})")
except Exception as e:
    print(f"✗ API not responding: {e}")
    print("  Make sure server is running: python run.py")
    exit(1)

# Test 2: Get current suggestions (should be empty)
print("\n[2] Getting current suggestions (should be empty)...")
response = requests.get(f"{API_BASE}/suggestions?user_id={USER_ID}&field_id=1")
data = response.json()
print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
print(f"Current suggestions count: {data.get('total_count', 0)}")

# Test 3: Get suggestions by field name
print("\n[3] Getting suggestions by field name...")
response = requests.get(f"{API_BASE}/suggestions/by-name?user_id={USER_ID}&field_name=name&form_id={FORM_ID}")
if response.ok:
    data = response.json()
    print(f"✓ Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
else:
    print(f"✗ Error: {response.text}")

# Test 4: Try to save an entry directly
print("\n[4] Saving test entry directly...")
response = requests.post(
    f"{API_BASE}/suggestions/save",
    params={"user_id": USER_ID, "field_id": 1, "form_id": FORM_ID, "value": "Test Name 1"}
)
if response.ok:
    data = response.json()
    print(f"✓ Entry saved: {data}")
else:
    print(f"✗ Error: {response.text}")

# Test 5: Save second entry with same value
print("\n[5] Saving second entry with same value...")
response = requests.post(
    f"{API_BASE}/suggestions/save",
    params={"user_id": USER_ID, "field_id": 1, "form_id": FORM_ID, "value": "Test Name 1"}
)
if response.ok:
    data = response.json()
    print(f"✓ Entry saved: {data}")
else:
    print(f"✗ Error: {response.text}")

# Test 6: Get suggestions again (should show suggestions now)
print("\n[6] Getting suggestions after saving 2 entries...")
response = requests.get(f"{API_BASE}/suggestions?user_id={USER_ID}&field_id=1")
if response.ok:
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
    print(f"Suggestions count: {data.get('total_count', 0)}")
    if data.get('total_count', 0) > 0:
        print("✓ Suggestions returned!")
    else:
        print("✗ No suggestions returned")
else:
    print(f"✗ Error: {response.text}")

print("\n" + "=" * 80)
print("API TEST COMPLETED")
print("=" * 80)
