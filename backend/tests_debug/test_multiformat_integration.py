"""Integration tests for multi-format file upload"""

import os
import sys
import json

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from io import BytesIO
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_supported_formats_endpoint():
    """Test the /api/word/supported-formats endpoint"""
    print("\n" + "=" * 70)
    print("[*] Testing GET /api/word/supported-formats")
    print("=" * 70)
    
    response = client.get("/api/word/supported-formats")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Supported extensions: {data['supported_extensions']}")
        print(f"✓ Descriptions available: {len(data['description'])} formats")
        for ext, desc in data['description'].items():
            print(f"  - {ext}: {desc}")
        return True
    else:
        print(f"✗ Error: {response.text}")
        return False


def test_upload_with_docx_mime():
    """Test that unsupported MIME types are handled"""
    print("\n" + "=" * 70)
    print("[*] Testing upload with invalid file")
    print("=" * 70)
    
    # Create a fake binary file
    fake_content = b"This is not a real file"
    files = {'file': ('test.xyz', fake_content, 'application/octet-stream')}
    data = {'user_id': '1'}
    
    response = client.post("/api/word/upload", files=files, data=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 400:
        error = response.json()
        print(f"✓ Correctly rejected invalid format: {error['detail'][:80]}...")
        return True
    else:
        print(f"✗ Expected 400, got {response.status_code}")
        return False


def test_upload_text_file():
    """Test uploading a text file"""
    print("\n" + "=" * 70)
    print("[*] Testing upload with .txt file")
    print("=" * 70)
    
    # Create a sample text file with fields
    text_content = """FORM DETAILS
    
Họ và Tên:
Ngày sinh:
Email:
Điện thoại:
Địa chỉ:
"""
    
    files = {'file': ('contact_form.txt', text_content.encode('utf-8'), 'text/plain')}
    data = {'user_id': '1'}
    
    response = client.post("/api/word/upload", files=files, data=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Upload successful")
        print(f"  - Template ID: {result['template_id']}")
        print(f"  - File type: {result['file_type']}")
        print(f"  - Fields count: {result['fields_count']}")
        if result['fields']:
            print(f"  - First field: {result['fields'][0]['label']}")
        return True
    else:
        print(f"✗ Error: {response.text[:200]}")
        return False


def test_upload_csv_file():
    """Test uploading a CSV file"""
    print("\n" + "=" * 70)
    print("[*] Testing upload with .csv file")
    print("=" * 70)
    
    # Create a sample CSV file
    csv_content = """Họ và Tên,Tuổi,Ngày sinh,Email
Nguyễn Văn A,30,1994,a@example.com
Trần Thị B,25,1999,b@example.com
"""
    
    files = {'file': ('users.csv', csv_content.encode('utf-8'), 'text/csv')}
    data = {'user_id': '1'}
    
    response = client.post("/api/word/upload", files=files, data=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Upload successful")
        print(f"  - Template ID: {result['template_id']}")
        print(f"  - File type: {result['file_type']}")
        print(f"  - Fields count: {result['fields_count']}")
        print(f"  - Fields: {[f['label'] for f in result['fields']]}")
        return True
    else:
        print(f"✗ Error: {response.text[:200]}")
        return False


def main():
    print("\n" + "=" * 70)
    print("[*] MULTI-FORMAT UPLOAD INTEGRATION TEST")
    print("=" * 70)
    
    results = []
    
    try:
        results.append(("GET Supported Formats", test_supported_formats_endpoint()))
        results.append(("Reject Invalid Format", test_upload_with_docx_mime()))
        results.append(("Upload .txt file", test_upload_text_file()))
        results.append(("Upload .csv file", test_upload_csv_file()))
    except Exception as e:
        print(f"\n✗ Test error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # Summary
    print("\n" + "=" * 70)
    print("[*] INTEGRATION TEST SUMMARY")
    print("=" * 70)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed\n")
    
    return all(result for _, result in results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
