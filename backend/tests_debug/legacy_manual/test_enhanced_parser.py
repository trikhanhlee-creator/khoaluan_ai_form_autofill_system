#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test enhanced field detection logic"""

import os
import sys
sys.path.insert(0, '.')

from app.services.file_parser import FileParserFactory
from pprint import pprint

def test_parser(file_path):
    """Test parser with a file"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    print(f"\n{'='*70}")
    print(f"Testing: {os.path.basename(file_path)}")
    print(f"{'='*70}\n")
    
    try:
        parser = FileParserFactory.create_parser(file_path)
        fields = parser.parse()
        metadata = parser.get_metadata()
        
        print(f"✅ Parse successful!")
        print(f"   File type: {metadata.get('file_type')}")
        print(f"   Fields found: {len(fields)}\n")
        
        if fields:
            print("📋 Extracted Fields:")
            print("-" * 70)
            for idx, field in enumerate(fields, 1):
                print(f"{idx}. Label: '{field.label}'")
                print(f"   Name: {field.name}")
                print(f"   Type: {field.field_type}")
                print()
        else:
            print("⚠️  No fields found!")
    
    except Exception as e:
        print(f"❌ Error parsing file: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Test with files in uploads directory
    uploads_dir = "uploads"
    
    if os.path.exists(uploads_dir):
        files = [f for f in os.listdir(uploads_dir) if f.endswith(('.docx', '.pdf', '.xlsx', '.csv', '.txt'))]
        
        if files:
            for file in files[:3]:  # Test first 3 files
                file_path = os.path.join(uploads_dir, file)
                test_parser(file_path)
        else:
            print("No test files found in uploads/ directory")
    else:
        print("uploads/ directory not found")
    
    print("\n" + "="*70)
    print("✅ Enhanced parser test completed!")
    print("="*70)
