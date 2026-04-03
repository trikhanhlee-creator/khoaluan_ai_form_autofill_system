"""
Test script để kiểm tra logic gợi ý với user/field mới
- Lần 1: No suggestions (< 2 entries)
- Lần 2: No suggestions (< 2 entries)  
- Lần 3+: Suggestions (>= 2 entries)
"""

import requests
import json

BASE_URL = "http://localhost:5000/api/suggestions"

# Sử dụng user_id mới (user id 1000) và field_id mới (field id 100)
USER_ID = 1000
FIELD_ID = 100
FORM_ID = 1
VALUES = ["Giá trị 1", "Giá trị 1", "Giá trị 2"]

def test_suggestions_fresh():
    """Test endpoint get_suggestions với field mới (chưa có entries)"""
    print("\n" + "="*60)
    print("TEST FRESH FIELD - NO ENTRIES YET")
    print("="*60)
    
    for i, value in enumerate(VALUES, 1):
        print(f"\n--- Lần nhập thứ {i}: '{value}' ---\n")
        
        # Step 1: Get suggestions TRƯỚC khi lưu
        print(f"1️⃣  Lấy gợi ý TRƯỚC khi lưu")
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
        
        # Verify logic
        if i < 3:  # Lần 1, 2
            expected_first = True
            expected_suggestions = []
        else:  # Lần 3+
            expected_first = False
            expected_suggestions = "có suggestions"
        
        is_correct = result.get('is_first_entry') == expected_first
        emoji = "✅" if is_correct else "❌"
        print(f"\n   {emoji} Logic check: is_first_entry={result.get('is_first_entry')} (expected {expected_first})")
        
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
        print(f"\n3️⃣  Lấy gợi ý SAU khi lưu")
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
        if result.get('suggestions'):
            print(f"   Suggestions: {json.dumps(result.get('suggestions', []), indent=6, ensure_ascii=False)}")
        else:
            print(f"   Suggestions: []")
        print(f"   Message: {result.get('message', '')}")

if __name__ == "__main__":
    try:
        test_suggestions_fresh()
        
        print("\n" + "="*60)
        print("✅ TEST HOÀN THÀNH")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()
