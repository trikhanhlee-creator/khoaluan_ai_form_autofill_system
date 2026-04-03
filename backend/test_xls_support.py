#!/usr/bin/env python
"""Test XLS file upload support"""
import requests
from io import BytesIO
import time

def create_test_xls():
    """Create a test XLS file"""
    # Use xlwt to create .xls file
    try:
        import xlwt
    except ImportError:
        print("Installing xlwt...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'xlwt', '-q'])
        import xlwt
    
    # Create workbook
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Sheet1')
    
    # Add headers
    headers = ['Ho Ten', 'Email', 'So Dien Thoai', 'Dia Chi']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)
    
    # Add data rows
    data = [
        ['Nguyen Van A', 'a@test.com', '0901234567', 'HCM'],
        ['Tran Thi B', 'b@test.com', '0912345678', 'Ha Noi'],
        ['Le Hoang C', 'c@test.com', '0923456789', 'Da Nang'],
    ]
    
    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, value in enumerate(row_data):
            worksheet.write(row_idx, col_idx, value)
    
    # Save to file
    workbook.save('test_file.xls')
    print("✓ Test XLS file created: test_file.xls")

def test_xls_upload():
    """Test XLS file upload"""
    print("\n" + "="*70)
    print("TEST: XLS File Upload Support")
    print("="*70 + "\n")
    
    # Create test file
    create_test_xls()
    
    # Upload file
    print("1. Testing XLS file upload...")
    with open('test_file.xls', 'rb') as f:
        files = {'file': ('test_file.xls', f, 'application/vnd.ms-excel')}
        response = requests.post('http://127.0.0.1:8000/api/excel/upload', files=files)
    
    print(f"   Status Code: {response.status_code}")
    data = response.json()
    print(f"   Response: {data}")
    
    if response.status_code == 200 and data.get('status') == 'success':
        print(f"\n✓ SUCCESS!")
        print(f"   Session ID: {data.get('session_id')}")
        print(f"   Headers: {data.get('headers')}")
        print(f"   Total Rows: {data.get('total_rows')}")
        print(f"   Message: {data.get('message')}")
    else:
        print(f"\n✗ FAILED!")
        print(f"   Error: {data.get('detail', 'Unknown error')}")

if __name__ == "__main__":
    time.sleep(2)  # Wait for server
    try:
        test_xls_upload()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
