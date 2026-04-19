#!/usr/bin/env python3
"""
Quick test script for Excel parsing with demo file
Run this to verify the parser is working correctly
"""
import sys
import os

# Add backend to path
sys.path.insert(0, '.')

from app.api.routes.excel import parse_excel_with_openpyxl, extract_field_metadata
from io import BytesIO

def main():
    """Quick test"""
    file_path = r"c:\Users\KHANH\Downloads\demoexcel.xlsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print("\n" + "="*70)
    print("[QUICK TEST] Excel Parser - demoexcel.xlsx")
    print("="*70)
    
    try:
        # Load and parse
        with open(file_path, 'rb') as f:
            excel_file = BytesIO(f.read())
        
        headers, rows, msg = parse_excel_with_openpyxl(excel_file)
        metadata = extract_field_metadata(headers)
        
        # Display results
        print(f"\n✅ {msg}")
        print(f"\n📋 Headers ({len(headers)} columns):")
        for i, h in enumerate(headers, 1):
            print(f"   {i}. {h}")
        
        print(f"\n📊 First student data:")
        for k, v in list(rows[0].items())[:5]:
            print(f"   {k}: {v}")
        
        print(f"\n✅ SUCCESS - Parser working correctly!")
        print("="*70 + "\n")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
