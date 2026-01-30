"""
Test script để kiểm tra logic gợi ý mới:
- Lần đầu (< 2 entries): không gợi ý
- Lần 2+ (>= 2 entries): gợi ý từ database
"""

import requests
import json

BASE_URL = "http://localhost:5000/api/suggestions"

# Test parameters
USER_ID = 1
FIELD_ID = 1
FORM_ID = 1
VALUES = ["Hà Nội", "Hà Nội", "TP Hồ Chí Minh"]

def test_suggestions():
    """Test endpoint get_suggestions"""
    print("\n" + "="*60)
    print("TEST SUGGESTIONS - FIRST vs LATER ENTRIES")
    print("="*60)
    
    for i, value in enumerate(VALUES, 1):
        print(f"\n--- Lần nhập thứ {i}: '{value}' ---\n")
        
        # Step 1: Get suggestions TRƯỚC khi lưu
        print(f"1️⃣  Lấy gợi ý TRƯỚC khi lưu (entry count: {i-1})")
        response = requests.get(
            BASE_URL,
            params={
                "user_id": USER_ID,
                "field_id": FIELD_ID,
                "top_k": 5
            }
        )
        result = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Entry count: {result.get('entry_count', 'N/A')}")
        print(f"   Is first entry: {result.get('is_first_entry', 'N/A')}")
        print(f"   Suggestions: {result.get('suggestions', [])}")
        print(f"   Message: {result.get('message', '')}")
        
        # Step 2: Save entry
        print(f"\n2️⃣  Lưu dữ liệu: '{value}'")
        save_response = requests.post(
            f"{BASE_URL}/save",
            params={
                "user_id": USER_ID,
                "field_id": FIELD_ID,
                "form_id": FORM_ID,
                "value": value
            }
        )
        save_result = save_response.json()
        print(f"   Status: {save_response.status_code}")
        print(f"   Entry ID: {save_result.get('entry_id', 'N/A')}")
        print(f"   Message: {save_result.get('message', '')}")
        
        # Step 3: Get suggestions SAU khi lưu
        print(f"\n3️⃣  Lấy gợi ý SAU khi lưu (entry count: {i})")
        response = requests.get(
            BASE_URL,
            params={
                "user_id": USER_ID,
                "field_id": FIELD_ID,
                "top_k": 5
            }
        )
        result = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Entry count: {result.get('entry_count', 'N/A')}")
        print(f"   Is first entry: {result.get('is_first_entry', 'N/A')}")
        print(f"   Suggestions: {json.dumps(result.get('suggestions', []), indent=6, ensure_ascii=False)}")
        print(f"   Message: {result.get('message', '')}")

def test_by_name():
    """Test endpoint get_suggestions/by-name"""
    print("\n" + "="*60)
    print("TEST BY-NAME ENDPOINT")
    print("="*60)
    
    response = requests.get(
        f"{BASE_URL}/by-name",
        params={
            "user_id": USER_ID,
            "field_name": "tỉnh/thành phố",  # Cần tìm đúng field name trong database
            "form_id": FORM_ID,
            "top_k": 5
        }
    )
    
    result = response.json()
    print(f"\nStatus: {response.status_code}")
    print(f"Entry count: {result.get('entry_count', 'N/A')}")
    print(f"Is first entry: {result.get('is_first_entry', 'N/A')}")
    print(f"Suggestions: {json.dumps(result.get('suggestions', []), indent=2, ensure_ascii=False)}")
    print(f"Message: {result.get('message', '')}")

if __name__ == "__main__":
    try:
        # Test suggestions endpoint
        test_suggestions()
        
        # Test by-name endpoint
        # test_by_name()
        
        print("\n" + "="*60)
        print("✅ TEST HOÀN THÀNH")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()
