#!/usr/bin/env python3
"""
Test XLS upload through HTTP API
"""
import requests
import time
import xlwt
import os

BASE_URL = "http://localhost:8000/api/excel"

def create_upload_test_files():
    """Create XLS files for testing"""
    
    # Normal file with headers
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Data')
    ws.write(0, 0, 'Ho Ten')
    ws.write(0, 1, 'Email')
    ws.write(0, 2, 'So Dien Thoai')
    ws.write(1, 0, 'Khanh')
    ws.write(1, 1, 'khanh@example.com')
    ws.write(1, 2, '0987654321')
    wb.save('upload_normal.xls')
    
    # File with empty first row
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Data')
    # Row 0 empty
    ws.write(1, 0, 'Ten')
    ws.write(1, 1, 'SDT')
    ws.write(1, 2, 'Dia Chi')
    ws.write(2, 0, 'Linh')
    ws.write(2, 1, '0912345678')
    ws.write(2, 2, 'Ho Chi Minh')
    wb.save('upload_empty_row.xls')

def test_upload(filename, test_name):
    """Test uploading a file"""
    print(f"\n🧪 Test: {test_name}")
    print(f"📁 File: {filename}")
    print("-" * 60)
    
    if not os.path.exists(filename):
        print(f"  ❌ File not found: {filename}")
        return False
    
    try:
        with open(filename, 'rb') as f:
            files = {'file': (filename, f, 'application/vnd.ms-excel')}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        print(f"  Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ SUCCESS")
            print(f"    • Headers: {data.get('headers', [])}")
            print(f"    • Rows: {len(data.get('rows', []))}")
            print(f"    • Message: {data.get('message', '')}")
            if data.get('rows'):
                print(f"    • First row: {data['rows'][0]}")
            return True
        else:
            print(f"  ❌ FAILED")
            print(f"    • Response: {response.text}")
            return False
    except Exception as e:
        print(f"  ❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔨 Creating test files...")
    print("=" * 60)
    create_upload_test_files()
    
    # Wait for server to start
    print("\n⏳ Waiting for server to be ready...")
    for i in range(15):
        try:
            requests.get("http://localhost:8000/health", timeout=1)
            print("✅ Server is ready!")
            break
        except:
            time.sleep(1)
            if i == 14:
                print("❌ Server didn't start in time")
                exit(1)
    
    print("\n" + "=" * 60)
    print("🚀 Testing uploads...")
    print("=" * 60)
    
    results = {}
    results['normal'] = test_upload('upload_normal.xls', 'Normal XLS with headers')
    results['empty_row'] = test_upload('upload_empty_row.xls', 'XLS with empty first row')
    
    print("\n" + "=" * 60)
    print("📊 Results:")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"✓ Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n⚠️  Some tests failed")
