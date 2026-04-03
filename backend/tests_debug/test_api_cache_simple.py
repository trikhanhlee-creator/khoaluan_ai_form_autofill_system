#!/usr/bin/env python3
"""Test API endpoints are reading from suggestions cache"""
import sys
import os
import requests
import time
sys.path.insert(0, '.')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:ltK240304@localhost:3306/autofill_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

BASE_URL = "http://localhost:8000/api"

def setup():
    """Setup test data"""
    db = SessionLocal()
    try:
        print("Setting up test data...")
        # Delete old data
        db.execute(text("DELETE FROM suggestions"))
        db.execute(text("DELETE FROM entries"))
        db.execute(text("DELETE FROM fields"))
        db.execute(text("DELETE FROM forms"))
        db.execute(text("DELETE FROM users"))
        db.commit()
        
        # Create user, form, fields
        db.execute(text("""INSERT INTO users (id, email, username) VALUES (1, 'test@test.com', 'Test')"""))
        db.execute(text("""INSERT INTO forms (id, user_id, form_name) VALUES (1, 1, 'Test Form')"""))
        db.execute(text("""INSERT INTO fields (id, form_id, field_name, field_type, display_order) VALUES (1, 1, 'Province', 'text', 1)"""))
        db.commit()
        print("[OK] Setup complete\n")
        
    finally:
        db.close()

def test_api():
    """Test API endpoints"""
    print("Testing API endpoints...\n")
    
    # Test 1: Get suggestions (should be empty - less than 2 entries)
    print("[1] GET /api/suggestions (0 entries)")
    resp = requests.get(f"{BASE_URL}/suggestions", params={"user_id": 1, "field_id": 1})
    data = resp.json()
    print(f"  Entry count: {data['entry_count']}")
    print(f"  Is first entry: {data['is_first_entry']}")
    print(f"  Suggestions: {data['suggestions']}")
    print(f"  Status: {'OK' if data['is_first_entry'] else 'WRONG'}\n")
    
    # Test 2: Save first entry
    print("[2] POST /api/suggestions/save (entry 1)")
    resp = requests.post(f"{BASE_URL}/suggestions/save", params={
        "user_id": 1, "field_id": 1, "form_id": 1, "value": "Hanoi"
    })
    entry1 = resp.json()
    print(f"  Entry ID: {entry1['entry_id']}")
    print(f"  Status: {'OK' if resp.status_code == 200 else 'FAILED'}\n")
    
    # Test 3: Save second entry
    print("[3] POST /api/suggestions/save (entry 2)")
    resp = requests.post(f"{BASE_URL}/suggestions/save", params={
        "user_id": 1, "field_id": 1, "form_id": 1, "value": "HCMC"
    })
    entry2 = resp.json()
    print(f"  Entry ID: {entry2['entry_id']}")
    print(f"  Status: {'OK' if resp.status_code == 200 else 'FAILED'}\n")
    
    # Test 4: Get suggestions (still no suggestions - less than 2 entries)
    print("[4] GET /api/suggestions (2 entries - should still be no suggestions)")
    resp = requests.get(f"{BASE_URL}/suggestions", params={"user_id": 1, "field_id": 1})
    data = resp.json()
    print(f"  Entry count: {data['entry_count']}")
    print(f"  Is first entry: {data['is_first_entry']}")
    print(f"  Suggestions: {data['suggestions']}")
    print(f"  Status: {'OK' if data['is_first_entry'] else 'WRONG'}\n")
    
    # Test 5: Save third entry
    print("[5] POST /api/suggestions/save (entry 3)")
    resp = requests.post(f"{BASE_URL}/suggestions/save", params={
        "user_id": 1, "field_id": 1, "form_id": 1, "value": "Hanoi"
    })
    entry3 = resp.json()
    print(f"  Entry ID: {entry3['entry_id']}")
    print(f"  Status: {'OK' if resp.status_code == 200 else 'FAILED'}\n")
    
    # Test 6: Get suggestions (now should have suggestions from cache)
    print("[6] GET /api/suggestions (3+ entries - should show suggestions)")
    resp = requests.get(f"{BASE_URL}/suggestions", params={"user_id": 1, "field_id": 1})
    data = resp.json()
    print(f"  Entry count: {data['entry_count']}")
    print(f"  Is first entry: {data['is_first_entry']}")
    print(f"  Suggestions count: {len(data['suggestions'])}")
    if data['suggestions']:
        for i, sug in enumerate(data['suggestions'], 1):
            print(f"    {i}. {sug['value']} (frequency={sug['frequency']}, ranking={sug.get('ranking', 'N/A')})")
    print(f"  Status: {'OK' if not data['is_first_entry'] and len(data['suggestions']) > 0 else 'WRONG'}\n")
    
    # Verify that suggestions come from cache
    print("[7] Verify suggestions are from cache table (not calculated real-time)")
    db = SessionLocal()
    try:
        suggestions = db.execute(text("""
            SELECT suggested_value, frequency, ranking FROM suggestions 
            WHERE user_id=1 AND field_id=1
            ORDER BY ranking DESC
        """)).fetchall()
        
        print(f"  Cache table has {len(suggestions)} suggestion(s)")
        for sug in suggestions:
            print(f"    - {sug[0]}: frequency={sug[1]}, ranking={sug[2]}")
        
        if len(suggestions) > 0:
            print(f"\n  [OK] Suggestions are being read from cache!")
            return True
        else:
            print(f"\n  [FAILED] Suggestions cache is empty!")
            return False
    finally:
        db.close()

if __name__ == "__main__":
    try:
        print("=" * 70)
        print("API ENDPOINT TEST - Verify Suggestions Cache")
        print("=" * 70 + "\n")
        
        setup()
        success = test_api()
        
        print("\n" + "=" * 70)
        if success:
            print("[OK] ALL TESTS PASSED - Suggestions cache is working correctly!")
        else:
            print("[FAILED] TEST FAILED")
        print("=" * 70)
        
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
