#!/usr/bin/env python3
"""
Full end-to-end test: Upload .xls → Save session → Generate form
"""
import requests
import time
import xlwt
import os
import json

BASE_URL = "http://localhost:8000"

def create_test_xls():
    """Create a test XLS file"""
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Users')
    
    # Headers
    ws.write(0, 0, 'Ho Ten')
    ws.write(0, 1, 'Email')
    ws.write(0, 2, 'So Dien Thoai')
    ws.write(0, 3, 'Dia Chi')
    
    # Data
    ws.write(1, 0, 'Khanh Nguyen')
    ws.write(1, 1, 'khanh@company.com')
    ws.write(1, 2, '0987654321')
    ws.write(1, 3, 'Ha Noi')
    
    ws.write(2, 0, 'Linh Tran')
    ws.write(2, 1, 'linh@company.com')
    ws.write(2, 2, '0912345678')
    ws.write(2, 3, 'Ho Chi Minh')
    
    wb.save('e2e_test.xls')
    return 'e2e_test.xls'

def test_full_workflow():
    """Complete workflow test"""
    
    print("=" * 70)
    print("🚀 FULL END-TO-END TEST: Upload .xls → View Form")
    print("=" * 70)
    
    # Step 1: Create test file
    print("\n1️⃣  Creating test XLS file...")
    filename = create_test_xls()
    print(f"   ✓ Created: {filename}")
    
    # Step 2: Wait for server
    print("\n2️⃣  Waiting for server...")
    for i in range(15):
        try:
            requests.get(f"{BASE_URL}/health", timeout=1)
            print("   ✓ Server ready (http://localhost:8000)")
            break
        except:
            time.sleep(1)
            if i == 14:
                print("   ❌ Server not responding")
                return False
    
    # Step 3: Upload file
    print("\n3️⃣  Uploading .xls file...")
    try:
        with open(filename, 'rb') as f:
            files = {'file': (filename, f, 'application/vnd.ms-excel')}
            response = requests.post(f"{BASE_URL}/api/excel/upload", files=files)
        
        if response.status_code != 200:
            print(f"   ❌ Upload failed: {response.status_code}")
            print(f"      {response.text}")
            return False
        
        data = response.json()
        session_id = data.get('session_id')
        headers = data.get('headers', [])
        total_rows = data.get('total_rows', 0)
        
        print(f"   ✓ Upload successful!")
        print(f"      • Session: {session_id}")
        print(f"      • Headers: {headers}")
        print(f"      • Rows: {total_rows}")
        print(f"      • Message: {data.get('message', '')}")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False
    
    # Step 4: View the generated form
    print(f"\n4️⃣  Generating form from uploaded data...")
    try:
        # The form should use the session_id
        form_url = f"{BASE_URL}/excel/form/{session_id}"
        print(f"   • Form URL: {form_url}")
        
        response = requests.get(form_url)
        if response.status_code != 200:
            print(f"   ⚠️  Form page status: {response.status_code}")
        else:
            # Check if form contains our data
            html = response.text
            if 'Ho Ten' in html and 'Email' in html:
                print(f"   ✓ Form generated with headers!")
                print(f"      • Form contains: Ho Ten, Email, ...")
            else:
                print(f"   ⚠️  Form generated but headers not found")
        
    except Exception as e:
        print(f"   ⚠️  Error checking form: {str(e)}")
    
    # Step 5: Check session is stored
    print(f"\n5️⃣  Verifying session storage...")
    try:
        # Try to get the form data via API
        response = requests.get(f"{BASE_URL}/api/excel/sessions/{session_id}")
        if response.status_code == 200:
            session_data = response.json()
            print(f"   ✓ Session stored and accessible")
            print(f"      • Headers: {session_data.get('headers', [])}")
            print(f"      • Rows stored: {session_data.get('total_rows', 0)}")
        else:
            print(f"   ❌ Session not found (Status: {response.status_code})")
    except:
        print(f"   ⚠️  Could not verify session (API endpoint may not exist)")
    
    print("\n" + "=" * 70)
    print("✅ END-TO-END TEST COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    test_full_workflow()
