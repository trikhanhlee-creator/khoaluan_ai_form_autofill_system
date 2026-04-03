#!/usr/bin/env python3
"""
Test XLS files with different formats to ensure robust parsing
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.api.routes.excel import parse_xls_file
import xlwt

def create_test_files():
    """Create various XLS test files"""
    
    # Test 1: Normal XLS with headers in row 0
    print("📝 Creating: normal_headers.xls (headers in row 0)")
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Data')
    ws.write(0, 0, 'Ho Ten')
    ws.write(0, 1, 'Email')
    ws.write(0, 2, 'So Dien Thoai')
    ws.write(1, 0, 'Nguyen Van A')
    ws.write(1, 1, 'a@example.com')
    ws.write(1, 2, '0123456789')
    wb.save('normal_headers.xls')
    print("  ✓ Created")
    
    # Test 2: Empty row 0, headers in row 1
    print("📝 Creating: empty_first_row.xls (headers in row 1)")
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Data')
    # Row 0 is empty
    ws.write(1, 0, 'Ho Ten')
    ws.write(1, 1, 'Email')
    ws.write(1, 2, 'So Dien Thoai')
    ws.write(2, 0, 'Nguyen Van A')
    ws.write(2, 1, 'a@example.com')
    ws.write(2, 2, '0123456789')
    wb.save('empty_first_row.xls')
    print("  ✓ Created")
    
    # Test 3: Headers in row 0, data with mixed types
    print("📝 Creating: mixed_types.xls (numbers and text)")
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Data')
    ws.write(0, 0, 'Name')
    ws.write(0, 1, 'Age')
    ws.write(0, 2, 'Score')
    ws.write(1, 0, 'Khanh')
    ws.write(1, 1, 25)  # Number
    ws.write(1, 2, 85.5)  # Float
    ws.write(2, 0, 'Linh')
    ws.write(2, 1, 23)  # Number
    ws.write(2, 2, 90.0)  # Float that looks like int
    wb.save('mixed_types.xls')
    print("  ✓ Created")

def test_parse(filename):
    """Test parsing a file"""
    print(f"\n🧪 Testing: {filename}")
    print("-" * 60)
    
    try:
        with open(filename, 'rb') as f:
            content = f.read()
        
        headers, rows, msg = parse_xls_file(content)
        
        print(f"  ✅ SUCCESS: {msg}")
        print(f"  • Headers: {headers}")
        print(f"  • Data rows: {len(rows)}")
        if rows:
            print(f"  • First row: {rows[0]}")
        return True
    except Exception as e:
        print(f"  ❌ FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔨 Creating test XLS files...")
    print("=" * 60)
    create_test_files()
    
    print("\n" + "=" * 60)
    print("🧪 Testing XLS parsing...")
    print("=" * 60)
    
    results = {}
    for test_file in ['normal_headers.xls', 'empty_first_row.xls', 'mixed_types.xls']:
        if os.path.exists(test_file):
            results[test_file] = test_parse(test_file)
    
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print("=" * 60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"  Passed: {passed}/{total}")
    
    for test_file, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"    {status}: {test_file}")
