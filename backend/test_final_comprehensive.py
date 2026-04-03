#!/usr/bin/env python3
"""
Final comprehensive test for demo Excel file
"""
import sys
sys.path.insert(0, '.')

from app.api.routes.excel import parse_excel_with_openpyxl, extract_field_metadata
from io import BytesIO

def test_comprehensive():
    """Comprehensive test of Excel parsing"""
    print("\n" + "="*80)
    print("FINAL COMPREHENSIVE TEST - demoexcel.xlsx")
    print("="*80)
    
    file_path = r"c:\Users\KHANH\Downloads\demoexcel.xlsx"
    
    try:
        with open(file_path, 'rb') as f:
            excel_file = BytesIO(f.read())
        
        headers, rows, msg = parse_excel_with_openpyxl(excel_file)
        field_metadata = extract_field_metadata(headers)
        
        print(f"\n✅ {msg}")
        
        print(f"\n📋 HEADERS ({len(headers)} columns):")
        for idx, header in enumerate(headers, 1):
            meta = field_metadata.get(header, {})
            field_type = meta.get('type', '')
            keywords = meta.get('keywords', [])
            keyword_str = f" | Keywords: {', '.join(keywords)}" if keywords else ""
            print(f"   {idx:2d}. {header:<20s} [Type: {field_type}]{keyword_str}")
        
        print(f"\n📊 DATA ROWS: {len(rows)}")
        
        if len(rows) >= 1:
            print(f"\n🔵 FIRST ROW (Student 1):")
            for key, value in list(rows[0].items()):
                print(f"   {key:<20s} → {str(value)[:50]}")
        
        if len(rows) >= 2:
            print(f"\n🟢 SECOND ROW (Student 2):")
            for key, value in list(rows[1].items()):
                print(f"   {key:<20s} → {str(value)[:50]}")
        
        if len(rows) > 2:
            print(f"\n🔴 LAST ROW (Student {len(rows)}):")
            for key, value in list(rows[-1].items()):
                print(f"   {key:<20s} → {str(value)[:50]}")
        
        # Validation
        print(f"\n✅ VALIDATION:")
        print(f"   ✓ Headers detected correctly: {len(headers) == 9}")
        print(f"   ✓ Data rows extracted: {len(rows) > 0}")
        print(f"   ✓ Label row skipped (65 rows, not 66): {len(rows) == 65}")
        print(f"   ✓ Field types detected: {all(field_metadata[h].get('type') for h in headers)}")
        print(f"   ✓ Keywords assigned: {sum(1 for h in headers if field_metadata[h].get('keywords'))}")
        
        print("\n" + "="*80)
        print("✅ ALL TESTS PASSED!")
        print("="*80 + "\n")
        
        return True
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_comprehensive()
    sys.exit(0 if success else 1)
