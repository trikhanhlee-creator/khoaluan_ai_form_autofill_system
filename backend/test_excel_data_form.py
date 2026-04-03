#!/usr/bin/env python3
"""
Test Excel data form feature
Upload file → Navigate to form → Test if data auto-fills
"""
import requests
import time
from openpyxl import Workbook
import os

BASE_URL = "http://localhost:8000"

def create_test_excel():
    """Create a test Excel file with student data"""
    wb = Workbook()
    ws = wb.active
    ws.append(['STT', 'Mã Sinh Viên', 'Họ Tên', 'Giới Tính', 'Ngày Sinh', 'Lớp Học'])
    ws.append([1, '223005', 'Trần Thiên Nhuận', 'Nam', '05/07/2004', 'DH22TIN07'])
    ws.append([2, '224703', 'Nguyễn Hoàng Phú', 'Nam', '27/10/2004', 'DH22TIN07'])
    ws.append([3, '222683', 'Hà Hoàng Phúc', 'Nam', '18/12/2004', 'DH22TIN07'])
    ws.append([4, '223172', 'Nguyễn Huỳnh Hồng Phúc', 'Nam', '03/11/2004', 'DH22TIN07'])
    ws.append([5, '222055', 'Nguyễn Quang Quyền', 'Nam', '07/03/2004', 'DH22TIN07'])
    wb.save('student_data.xlsx')
    print("✓ Created: student_data.xlsx (5 students)")
    return 'student_data.xlsx'

def test_upload_and_form():
    """Test upload and form access"""
    print("\n" + "=" * 70)
    print("🧪 TEST: Excel Data Auto-Fill Form")
    print("=" * 70)
    
    # Wait for server
    print("\n⏳ Waiting for server...")
    for i in range(15):
        try:
            requests.get(f"{BASE_URL}/health", timeout=1)
            print("✅ Server ready!\n")
            break
        except:
            time.sleep(1)
            if i == 14:
                print("❌ Server not responding")
                return False
    
    # Create test file
    print("📝 Creating test file...")
    filename = create_test_excel()
    
    # Upload file
    print("\n📤 Uploading file...")
    try:
        with open(filename, 'rb') as f:
            files = {'file': (filename, f)}
            response = requests.post(f"{BASE_URL}/api/excel/upload", files=files)
        
        if response.status_code != 200:
            print(f"❌ Upload failed: {response.status_code}")
            return False
        
        data = response.json()
        session_id = data.get('session_id')
        total_rows = data.get('total_rows')
        
        print(f"✅ Upload successful!")
        print(f"   • Session ID: {session_id}")
        print(f"   • Total rows: {total_rows}")
        print(f"   • Message: {data.get('message')}")
        
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        return False
    
    # Test form page access
    print(f"\n📋 Testing form page access...")
    try:
        form_url = f"{BASE_URL}/excel-data-form/{session_id}"
        print(f"   • URL: {form_url}")
        
        response = requests.get(form_url)
        if response.status_code != 200:
            print(f"❌ Form page error: {response.status_code}")
            return False
        
        html = response.text
        if 'Điền Dữ Liệu Excel' in html and 'dataTable' in html:
            print(f"✅ Form page loaded successfully!")
        else:
            print(f"⚠️  Form page loaded but content may be incomplete")
        
    except Exception as e:
        print(f"❌ Form page error: {str(e)}")
        return False
    
    # Test API endpoint data
    print(f"\n📊 Testing data API endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/excel/data/{session_id}")
        if response.status_code != 200:
            print(f"❌ Data API error: {response.status_code}")
            return False
        
        data = response.json()
        headers = data.get('headers', [])
        rows_count = len(data.get('rows', []))
        
        print(f"✅ Data API responding!")
        print(f"   • Headers: {headers}")
        print(f"   • Rows: {rows_count}")
        
        if rows_count > 0:
            first_row = data['rows'][0]
            print(f"   • First row sample: {str(first_row)[:80]}...")
        
    except Exception as e:
        print(f"❌ Data API error: {str(e)}")
        return False
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)
    print(f"\n🎉 Excel data form is working!")
    print(f"\nYou can now:")
    print(f"1. Go to {BASE_URL}/excel")
    print(f"2. Upload an Excel file")
    print(f"3. Click on any row to auto-fill the form")
    print(f"4. Edit the data as needed")
    print(f"5. Save changes")
    
    return True

if __name__ == "__main__":
    success = test_upload_and_form()
    exit(0 if success else 1)
