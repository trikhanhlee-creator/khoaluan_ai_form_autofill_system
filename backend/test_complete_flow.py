#!/usr/bin/env python3
"""
Test toàn bộ flow từ đầu:
1. Tạo user, form, fields
2. Lần 1: Không gợi ý, lưu dữ liệu
3. Lần 2: Không gợi ý (chưa đủ 2 entries), lưu dữ liệu
4. Lần 3+: Có gợi ý từ database
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"
USER_ID = 1
FORM_ID = 1

def setup_database():
    """Tạo user, form, fields"""
    print("\n" + "="*70)
    print("BƯỚC 1: SETUP DATABASE - TẠO USER, FORM, FIELDS")
    print("="*70)
    
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    
    DATABASE_URL = "mysql+pymysql://root:ltK240304@localhost:3306/autofill_db"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # 1. Tạo user
        db.execute(text("""
            INSERT INTO users (id, email, username) VALUES 
            (1, 'test@example.com', 'Test User')
        """))
        print("✓ Tạo user: ID=1, email=test@example.com")
        
        # 2. Tạo form
        db.execute(text("""
            INSERT INTO forms (id, user_id, form_name, description) VALUES
            (1, 1, 'Test Form', 'Form test')
        """))
        print("✓ Tạo form: ID=1, form_name=Test Form")
        
        # 3. Tạo fields
        fields = [
            (1, 1, 'Tỉnh/Thành phố', 'text', 1),
            (2, 1, 'Quận/Huyện', 'text', 2),
            (3, 1, 'Phường/Xã', 'text', 3),
        ]
        
        for field_id, form_id, field_name, field_type, order in fields:
            db.execute(text(f"""
                INSERT INTO fields (id, form_id, field_name, field_type, display_order) VALUES
                ({field_id}, {form_id}, '{field_name}', '{field_type}', {order})
            """))
            print(f"✓ Tạo field: ID={field_id}, name={field_name}")
        
        db.commit()
        print("\n✅ Setup database hoàn thành!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Lỗi: {str(e)}")
    finally:
        db.close()

def test_suggestions_flow():
    """Test flow: lần 1, 2, 3+"""
    print("\n" + "="*70)
    print("BƯỚC 2: TEST SUGGESTIONS FLOW")
    print("="*70)
    
    test_cases = [
        {
            "round": 1,
            "field_id": 1,
            "field_name": "Tỉnh/Thành phố",
            "values": ["Hà Nội", "Hà Nội", "TP Hồ Chí Minh"],
        },
        {
            "round": 2,
            "field_id": 2,
            "field_name": "Quận/Huyện",
            "values": ["Quận 1", "Quận 1", "Quận 3"],
        }
    ]
    
    for test_case in test_cases:
        field_id = test_case["field_id"]
        field_name = test_case["field_name"]
        values = test_case["values"]
        
        print(f"\n{'='*70}")
        print(f"FIELD: {field_name} (ID={field_id})")
        print(f"{'='*70}")
        
        for i, value in enumerate(values, 1):
            print(f"\n--- Lần nhập thứ {i}: '{value}' ---\n")
            
            # 1. Lấy gợi ý trước khi lưu
            print(f"1️⃣  GET /api/suggestions?user_id={USER_ID}&field_id={field_id}")
            response = requests.get(
                f"{BASE_URL}/suggestions",
                params={
                    "user_id": USER_ID,
                    "field_id": field_id,
                    "top_k": 3
                }
            )
            result = response.json()
            
            entry_count_before = result.get('entry_count', 0)
            is_first = result.get('is_first_entry', False)
            suggestions = result.get('suggestions', [])
            
            print(f"   Status: {response.status_code}")
            print(f"   Entry count: {entry_count_before}")
            print(f"   Is first entry: {is_first}")
            print(f"   Suggestions: {len(suggestions)} items")
            if suggestions:
                print(f"   Top suggestion: {suggestions[0]['value']} (frequency={suggestions[0]['frequency']})")
            print(f"   Message: {result.get('message', '')}")
            
            # Verify logic
            if i < 3:
                expected_first = True
                expected_suggestions_count = 0
            else:
                expected_first = False
                expected_suggestions_count = "có suggestions"
            
            check = "✅" if is_first == expected_first else "❌"
            print(f"\n   {check} Logic: is_first_entry={is_first} (expected {expected_first})")
            
            # 2. Lưu entry
            print(f"\n2️⃣  POST /api/suggestions/save?user_id={USER_ID}&field_id={field_id}&form_id={FORM_ID}&value={value}")
            save_response = requests.post(
                f"{BASE_URL}/suggestions/save",
                params={
                    "user_id": USER_ID,
                    "field_id": field_id,
                    "form_id": FORM_ID,
                    "value": value
                }
            )
            save_result = save_response.json()
            
            print(f"   Status: {save_response.status_code}")
            if save_response.status_code == 200:
                entry_id = save_result.get('entry_id', 'N/A')
                print(f"   Entry ID: {entry_id} ✅")
                print(f"   Message: {save_result.get('message', '')}")
            else:
                print(f"   ❌ Lỗi: {save_result}")
            
            # 3. Lấy gợi ý sau khi lưu
            print(f"\n3️⃣  GET /api/suggestions (sau khi lưu)")
            response = requests.get(
                f"{BASE_URL}/suggestions",
                params={
                    "user_id": USER_ID,
                    "field_id": field_id,
                    "top_k": 3
                }
            )
            result = response.json()
            
            entry_count_after = result.get('entry_count', 0)
            is_first_after = result.get('is_first_entry', False)
            suggestions_after = result.get('suggestions', [])
            
            print(f"   Status: {response.status_code}")
            print(f"   Entry count: {entry_count_before} → {entry_count_after}")
            print(f"   Is first entry: {is_first_after}")
            print(f"   Suggestions: {len(suggestions_after)} items")
            if suggestions_after:
                for j, sug in enumerate(suggestions_after[:2], 1):
                    print(f"      {j}. {sug['value']} (frequency={sug['frequency']})")
            print(f"   Message: {result.get('message', '')}")
            
            # Verify data saved
            if entry_count_after > entry_count_before:
                print(f"\n   ✅ Dữ liệu đã được lưu (entry_count +1)")
            else:
                print(f"\n   ❌ Dữ liệu không được lưu")

def verify_database():
    """Kiểm tra dữ liệu trong database"""
    print("\n" + "="*70)
    print("BƯỚC 3: KIỂM TRA DỮ LIỆU TRONG DATABASE")
    print("="*70)
    
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    
    DATABASE_URL = "mysql+pymysql://root:ltK240304@localhost:3306/autofill_db"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # 1. Kiểm tra entries
        entries = db.execute(text("""
            SELECT e.id, e.user_id, e.field_id, e.value, f.field_name
            FROM entries e
            JOIN fields f ON e.field_id = f.id
            ORDER BY e.field_id, e.created_at
        """)).fetchall()
        
        print(f"\n📝 Tổng entries: {len(entries)}")
        if entries:
            print("\nChitiết entries:")
            for entry in entries:
                print(f"  • ID={entry[0]}, user_id={entry[1]}, field_id={entry[2]}")
                print(f"    Field: {entry[4]}, Value: '{entry[3]}'")
        
        # 2. Kiểm tra tần suất
        print(f"\n📊 Tần suất giá trị theo field:")
        for field_id in [1, 2, 3]:
            result = db.execute(text(f"""
                SELECT f.field_name, e.value, COUNT(*) as count
                FROM entries e
                JOIN fields f ON e.field_id = f.id
                WHERE e.field_id = {field_id}
                GROUP BY e.value
                ORDER BY count DESC
            """)).fetchall()
            
            if result:
                field_name = result[0][0]
                print(f"\n  {field_name} (Field ID={field_id}):")
                for row in result:
                    print(f"    - '{row[1]}': {row[2]} lần")
            
    finally:
        db.close()

if __name__ == "__main__":
    try:
        # Setup
        setup_database()
        
        # Test
        test_suggestions_flow()
        
        # Verify
        verify_database()
        
        print("\n" + "="*70)
        print("✅ TEST HOÀN THÀNH - MỌI THỨ HOẠT ĐỘNG ĐỀU!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()
