#!/usr/bin/env python3
"""
Debug script to analyze XLS file structure and help troubleshoot parsing issues
"""
import sys
import os
import xlrd
from pathlib import Path

def analyze_xls_file(file_path):
    """Detailed analysis of XLS file structure"""
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    print(f"\n📄 Analyzing: {file_path}")
    print("=" * 60)
    
    try:
        # Open workbook
        workbook = xlrd.open_workbook(file_path, on_demand=True)
        
        print(f"✓ Successfully opened XLS file")
        print(f"  • Number of sheets: {workbook.nsheets}")
        
        if workbook.nsheets == 0:
            print("❌ No sheets found!")
            return
        
        # Analyze first sheet
        sheet = workbook.sheet_by_index(0)
        print(f"\n📊 Sheet 0: '{sheet.name}'")
        print(f"  • Rows: {sheet.nrows}")
        print(f"  • Columns: {sheet.ncols}")
        
        if sheet.nrows == 0:
            print("❌ Sheet is empty!")
            return
        
        # Analyze first row (headers)
        print(f"\n🔍 First Row Analysis (Row 0):")
        print("-" * 60)
        
        first_row_data = []
        empty_cells = 0
        non_empty_cells = 0
        
        for col_idx in range(sheet.ncols):
            cell_value = sheet.cell_value(0, col_idx)
            cell_type = sheet.cell_type(0, col_idx)
            
            type_name = xlrd.sheet.ctype_text.get(cell_type, "UNKNOWN")
            
            if cell_value or cell_value == 0:
                non_empty_cells += 1
                first_row_data.append(str(cell_value).strip())
                print(f"  Col {col_idx}: '{cell_value}' (Type: {type_name})")
            else:
                empty_cells += 1
                first_row_data.append("")
                print(f"  Col {col_idx}: [EMPTY] (Type: {type_name})")
        
        print(f"\n📈 First Row Summary:")
        print(f"  • Total cells: {sheet.ncols}")
        print(f"  • Non-empty cells: {non_empty_cells}")
        print(f"  • Empty cells: {empty_cells}")
        
        if non_empty_cells == 0:
            print("  ⚠️  WARNING: First row is completely empty!")
            print("  💡 SUGGESTION: Try to use first row with data as headers")
        
        # Show data rows
        print(f"\n📋 Data Rows (Rows 1-{min(5, sheet.nrows-1)}):")
        print("-" * 60)
        
        for row_idx in range(1, min(6, sheet.nrows)):
            row_values = []
            for col_idx in range(sheet.ncols):
                cell_value = sheet.cell_value(row_idx, col_idx)
                row_values.append(str(cell_value) if cell_value or cell_value == 0 else "")
            
            # Show first few columns
            display_values = row_values[:4]
            if len(row_values) > 4:
                display_values.append(f"... +{len(row_values)-4} more")
            
            print(f"  Row {row_idx}: {display_values}")
        
        if sheet.nrows > 6:
            print(f"  ... and {sheet.nrows - 5} more rows")
        
        # Statistics
        print(f"\n📊 Statistics:")
        print(f"  • Total data rows (if first is header): {sheet.nrows - 1}")
        print(f"  • Total data rows (if first is data): {sheet.nrows}")
        
        workbook.release_resources()
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if non_empty_cells == 0:
            print("  1. The first row appears to be empty")
            print("  2. Consider using the first data row as headers")
            print("  3. Or check if the file format is correct")
        else:
            print("  ✓ Headers found in first row")
            print("  ✓ File structure looks valid")
        
    except Exception as e:
        print(f"❌ Error analyzing file: {str(e)}")
        import traceback
        traceback.print_exc()

def test_create_and_analyze():
    """Create a test XLS and analyze it"""
    import xlwt
    
    print("\n\n🔨 Creating Test XLS File...")
    print("=" * 60)
    
    # Create test file with headers
    test_file = "debug_test_with_headers.xls"
    
    try:
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Sheet1')
        
        # Write headers
        headers = ['Ho Ten', 'Email', 'So Dien Thoai', 'Dia Chi']
        for col, header in enumerate(headers):
            sheet.write(0, col, header)
        
        # Write data
        sheet.write(1, 0, 'Nguyen Van A')
        sheet.write(1, 1, 'a@example.com')
        sheet.write(1, 2, '0123456789')
        sheet.write(1, 3, 'Ha Noi')
        
        workbook.save(test_file)
        print(f"✓ Created: {test_file}")
        
        # Now analyze it
        analyze_xls_file(test_file)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Analyze provided file
        file_path = sys.argv[1]
        analyze_xls_file(file_path)
    else:
        # Create and analyze test file
        test_create_and_analyze()
        
        # Also try to analyze sample_data.xlsx
        if os.path.exists("sample_data.xlsx"):
            print("\n\n" + "=" * 60)
            print("Also analyzing existing sample_data.xlsx...")
            analyze_xls_file("sample_data.xlsx")
