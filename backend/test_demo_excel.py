#!/usr/bin/env python3
"""
Test Excel file from Downloads folder
"""
import sys
import os

sys.path.insert(0, '.')

from app.api.routes.excel import parse_excel_with_openpyxl, extract_field_metadata

def test_demo_excel():
    """Test the demo Excel file"""
    print("\n" + "="*70)
    print("[TEST] Demo Excel File Analysis")
    print("="*70)
    
    # File path
    file_path = r"c:\Users\KHANH\Downloads\demoexcel.xlsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"\n📁 File: {file_path}")
    print(f"📊 File size: {os.path.getsize(file_path)} bytes")
    
    try:
        with open(file_path, 'rb') as f:
            excel_file = f.read()
        
        from io import BytesIO
        excel_file = BytesIO(excel_file)
        
        print("\n[1/4] Parsing Excel file...")
        headers, rows, msg = parse_excel_with_openpyxl(excel_file)
        
        print(f"\n✅ {msg}")
        print(f"\n📋 Headers ({len(headers)} columns):")
        for idx, header in enumerate(headers, 1):
            print(f"   {idx:2d}. {header}")
        
        # Test field metadata extraction
        print("\n[2/4] Extracting field metadata...")
        field_metadata = extract_field_metadata(headers)
        
        print(f"\n🔍 Field Metadata Analysis:")
        for idx, header in enumerate(headers, 1):
            if header in field_metadata:
                meta = field_metadata[header]
                field_type = meta.get('type', 'unknown')
                keywords = meta.get('keywords', [])
                normalized = meta.get('normalized', header)
                print(f"\n   {idx:2d}. {header}")
                print(f"       Type: {field_type}")
                print(f"       Normalized: {normalized}")
                print(f"       Keywords: {keywords if keywords else 'None'}")
        
        print(f"\n📊 Data Summary:")
        print(f"   Total data rows: {len(rows)}")
        
        if rows:
            print(f"\n[3/4] First row data:")
            for header, value in list(rows[0].items())[:10]:
                print(f"   {header:<30s} → {str(value)[:50]}")
            
            if len(rows) > 1:
                print(f"\n[4/4] Last row data:")
                for header, value in list(rows[-1].items())[:10]:
                    print(f"   {header:<30s} → {str(value)[:50]}")
        
        print("\n" + "="*70)
        print(f"✅ TEST PASSED - File analyzed successfully!")
        print(f"   Headers: {len(headers)} columns")
        print(f"   Data rows: {len(rows)}")
        print("="*70 + "\n")
        
        return True
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("="*70 + "\n")
        return False

if __name__ == "__main__":
    success = test_demo_excel()
    sys.exit(0 if success else 1)
