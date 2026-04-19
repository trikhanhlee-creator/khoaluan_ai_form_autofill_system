#!/usr/bin/env python3
"""
Test specifically for the user's reported issue:
"Không thể đọc file .xls: XLS parsing failed: No headers in first row"

This test creates scenarios that would have caused this error and verifies the fix
"""
import requests
import time
import xlwt
import os

BASE_URL = "http://localhost:8000"

def create_problematic_xls_files():
    """Create XLS files that previously would have failed"""
    
    files_created = {}
    
    # Scenario 1: Empty first row (common export issue)
    print("   • Creating: empty_first_row_scenario.xls")
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Data')
    # Row 0 is intentionally empty
    ws.write(1, 0, 'Tên Nhân Viên')
    ws.write(1, 1, 'Email')
    ws.write(1, 2, 'Phòng Ban')
    ws.write(2, 0, 'Nguyễn Văn A')
    ws.write(2, 1, 'a@company.vn')
    ws.write(2, 2, 'Kỹ Thuật')
    wb.save('empty_first_row_scenario.xls')
    files_created['empty_first_row_scenario.xls'] = {
        'name': 'Scenario 1: Empty first row',
        'description': 'File with empty row 0, headers in row 1'
    }
    
    # Scenario 2: Headers are in first row (normal case, to verify we didn't break it)
    print("   • Creating: normal_headers_scenario.xls")
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Data')
    ws.write(0, 0, 'Mã Sinh Viên')
    ws.write(0, 1, 'Tên')
    ws.write(0, 2, 'Lớp')
    ws.write(1, 0, 'SV001')
    ws.write(1, 1, 'Trần Thị B')
    ws.write(1, 2, 'D21CQCN01-N')
    wb.save('normal_headers_scenario.xls')
    files_created['normal_headers_scenario.xls'] = {
        'name': 'Scenario 2: Normal headers (row 0)',
        'description': 'File with headers in first row (standard format)'
    }
    
    # Scenario 3: Headers with Vietnamese characters and numbers mixed
    print("   • Creating: vietnamese_mixed_scenario.xls")
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Data')
    ws.write(0, 0, 'Tên Khách Hàng')
    ws.write(0, 1, 'Điện Thoại')
    ws.write(0, 2, 'Năm Sinh')
    ws.write(0, 3, 'Địa Chỉ')
    ws.write(1, 0, 'Phạm Văn C')
    ws.write(1, 1, '0912345678')
    ws.write(1, 2, 1995)  # Number
    ws.write(1, 3, '123 Đường ABC, Hà Nội')
    wb.save('vietnamese_mixed_scenario.xls')
    files_created['vietnamese_mixed_scenario.xls'] = {
        'name': 'Scenario 3: Vietnamese + numbers',
        'description': 'File with Vietnamese headers, mixed data types'
    }
    
    return files_created

def test_upload(filename, detailed_info):
    """Test uploading a problematic file"""
    
    scenario_name = detailed_info['name']
    description = detailed_info['description']
    
    print(f"\n  📋 Testing: {scenario_name}")
    print(f"     Description: {description}")
    print(f"     File: {filename}")
    print("     " + "-" * 56)
    
    try:
        with open(filename, 'rb') as f:
            files = {'file': (filename, f, 'application/vnd.ms-excel')}
            response = requests.post(f"{BASE_URL}/api/excel/upload", files=files)
        
        print(f"     HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            headers = data.get('headers', [])
            total_rows = data.get('total_rows', 0)
            message = data.get('message', '')
            
            print(f"     ✅ SUCCESS!")
            print(f"        Headers found: {len(headers)} - {headers}")
            print(f"        Data rows: {total_rows}")
            print(f"        Message: {message}")
            return True
        else:
            error_text = response.text[:200]  # First 200 chars
            print(f"     ❌ FAILED!")
            print(f"        Error: {error_text}")
            return False
    
    except Exception as e:
        print(f"     ❌ EXCEPTION!")
        print(f"        Error: {str(e)}")
        return False

def main():
    print("\n" + "=" * 70)
    print("🔧 FIX VERIFICATION TEST")
    print("Issue: Cannot read .xls files - 'No headers in first row' error")
    print("=" * 70)
    
    # Wait for server
    print("\nWaiting for server to start...")
    for i in range(15):
        try:
            requests.get(f"{BASE_URL}/health", timeout=1)
            print("✅ Server is ready!\n")
            break
        except:
            time.sleep(1)
            if i == 14:
                print("❌ Server not responding")
                return False
    
    # Create test files
    print("Creating test files...")
    test_files = create_problematic_xls_files()
    print(f"✅ Created {len(test_files)} test files\n")
    
    # Run tests
    print("=" * 70)
    print("🧪 TESTING PREVIOUSLY FAILING SCENARIOS")
    print("=" * 70)
    
    results = {}
    for filename, details in test_files.items():
        results[filename] = test_upload(filename, details)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    for filename, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}: {filename}")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED!")
        print("\n🎉 FIX VERIFIED: XLS files can now be read even with empty first rows!")
        return True
    else:
        print(f"\n⚠️  Some tests failed ({total - passed} failures)")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
