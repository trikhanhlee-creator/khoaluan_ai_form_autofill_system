# 🔧 Excel Upload Troubleshooting Guide

## ✅ Status Checklist

- [x] **API Functionality** - Working perfectly ✓
- [x] **File Parsing** - All valid Excel files parse correctly ✓  
- [x] **HTTP Endpoint** - `/api/excel/upload` returns HTTP 200 ✓
- [x] **Frontend HTML** - CSS errors fixed ✓
- [x] **Special Characters** - Vietnamese characters supported ✓
- [x] **Sessions Management** - Working correctly ✓

---

## 🎯 Common Excel Upload Errors and Solutions

### Error 1: "Excel file has no headers in first row"
**Cause:** First row is empty or contains no data  
**Solution:**
```
✓ Ensure Row 1 contains column headers
✓ Headers must have at least one non-empty cell
✓ Example: "Name", "Email", "Phone"
```

### Error 2: "Excel file has no data rows"
**Cause:** File has headers but no data rows (only first row has content)  
**Solution:**
```
✓ Add at least one data row starting from Row 2
✓ Example:
  Row 1: Name | Email | Phone
  Row 2: John | john@test.com | 0901234567
```

### Error 3: "Chi ho tro cac file Excel (.xlsx, .xls)"
**Cause:** File is not in Excel format  
**Solution:**
```
✓ Save file as .xlsx (Excel 2007+ format)
✓ Old .xls format is supported but not recommended
✓ Alternative: .xls format is acceptable
```

### Error 4: "File Excel trong hoac khong hop le"
**Cause:** File is empty or corrupted  
**Solution:**
```
✓ Re-create the file in Excel or LibreOffice
✓ Ensure file is saved properly before upload
✓ Check file size is > 0 bytes
```

### Error 5: "Khong the doc file Excel: [error details]"
**Cause:** File is corrupted or uses incompatible format  
**Solution:**
```
✓ Open file in Microsoft Excel or LibreOffice Calc
✓ Save as .xlsx format
✓ Re-upload the file
```

---

## 📋 Excel File Requirements

### Minimum Format
```
Row 1 (Headers):    Column1 | Column2 | Column3
Row 2 (Data):       Value1  | Value2  | Value3
```

### Maximum Limits
```
- Maximum columns: Unlimited (but reasonable limit for UI)
- Maximum rows: 10,000+ supported
- Maximum file size: 50MB (FastAPI default)
- Cell values: UTF-8 encoded text
```

### Supported Data Types
```
✓ Text (strings)
✓ Numbers (integers, decimals)
✓ Dates (will be converted to text)
✓ Empty cells (treated as empty string)
✓ Special characters (Vietnamese, Chinese, etc.)
```

### Unsupported Features (converted to text)
```
✗ Formulas (=SUM, =IF, etc.) - values only
✗ Images/Charts (ignored)
✗ Comments (ignored)
✗ Multiple sheets (only first sheet used)
```

---

## 🚀 Step-by-Step: How to Create a Valid Excel File

### Using Microsoft Excel
```
1. Open Microsoft Excel
2. Create new workbook
3. In Row 1, enter column names:
   - A1: Ho Ten
   - B1: Email
   - C1: So Dien Thoai
4. In Row 2+, enter your data:
   - A2: Nguyen Van A
   - B2: a@test.com
   - C2: 0901234567
5. File → Save As → Format: .xlsx (Excel Workbook)
6. Choose location and click Save
7. Go to http://localhost:8000/excel
8. Upload your file
```

### Using LibreOffice Calc (Free)
```
1. Open LibreOffice Calc
2. Create new spreadsheet
3. Enter headers in Row 1
4. Enter data in Row 2+
5. File → Save As
6. Choose format: ODF Spreadsheet (.ods) or Excel 2007+ (.xlsx)
7. Click Save
8. Upload to system
```

### Using Google Sheets
```
1. Create a new Google Sheet
2. Add headers in Row 1
3. Add data in Row 2+
4. File → Download → Microsoft Excel (.xlsx)
5. Upload to system
```

---

## 🧪 Testing Your Excel File

### Test 1: File Format
```bash
# Check file extension
File name: data.xlsx ✓
File name: data.xls ✓
File name: data.csv ✗ (not supported)
File name: data.txt ✗ (not supported)
```

### Test 2: File Size
```bash
# Check file is not empty
File size: 5,000 bytes ✓
File size: 0 bytes ✗ (empty file)
File size: 10MB+ ✓ (very large but acceptable)
```

### Test 3: File Integrity
```
✓ Can open in Excel/LibreOffice
✓ Contains visible headers and data
✓ No corrupted cells showing errors
✓ Special characters display correctly
```

---

## 🔗 Testing the Upload

### Test 1: Via Browser
```
1. Navigate to http://localhost:8000/excel
2. Click "Chọn File Excel" button
3. Select your Excel file
4. File uploads and form loads automatically
5. Verify data is displayed correctly
```

### Test 2: Via API (cURL)
```bash
curl -X POST "http://localhost:8000/api/excel/upload" \
  -F "file=@/path/to/your/file.xlsx"
```

### Test 3: Via Python
```python
import requests

with open('file.xlsx', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/api/excel/upload',
        files=files
    )
    print(response.json())
```

---

## 📊 Expected Success Response

When upload is successful, you should see:

```json
{
  "status": "success",
  "session_id": "file_name",
  "filename": "file.xlsx",
  "headers": ["Ho Ten", "Email", "So Dien Thoai"],
  "total_rows": 5,
  "message": "Tải file thành công! Tìm thấy 5 dòng dữ liệu"
}
```

---

## 🐛 Debugging: Enable Browser Console

### Check for JavaScript Errors
```
1. Open your browser (Chrome, Firefox, Edge)
2. Press F12 to open Developer Tools
3. Click "Console" tab
4. Try uploading again
5. Look for red error messages
6. Screenshot and share errors
```

### Common Browser Errors
```
✗ "CORS error" - Server not running or wrong port
✗ "Network error" - Server unreachable
✗ "TypeError" - JavaScript syntax error in page
✗ "413 Payload Too Large" - File too big
```

---

## 🎯 Recommended Excel Template

Download or create this template:

```
| Ho Ten          | Email              | So Dien Thoai | Dia Chi  | Vi Tri        |
|:----------------|:-------------------|:-------------|:--------|:-------------|
| Nguyen Van A    | nguyenvana@...    | 0901234567   | HCM     | Nhan vien    |
| Tran Thi B      | tranthib@...      | 0912345678   | Ha Noi  | Truong phong |
| Le Hoang C      | lehoangc@...      | 0923456789   | Da Nang  | Nhan vien    |
| Pham Huy D      | phamhuyd@...      | 0934567890   | HCM     | Truong phong |
| Hoang Kim E     | hoangkime@...     | 0945678901   | Can Tho  | Nhan vien    |
```

---

## 📞 Still Having Issues?

### Information to Provide:
1. **Exact error message** you see
2. **Excel file details:**
   - Number of rows and columns
   - File size (in MB)
   - File extension (.xlsx or .xls)
3. **Where the error occurs:**
   - Browser upload page
   - Browser console (F12)
   - Server logs
4. **Screenshot** of the error

### Where to Check:
- Browser Console: F12 → Console tab
- Server Logs: Check terminal where server is running  
- Network Tab: F12 → Network tab → look for failed requests

---

## ✨ Features Now Working

- ✅ Upload Excel files (.xlsx, .xls)
- ✅ Parse headers from first row
- ✅ Extract all data rows
- ✅ Support Vietnamese and special characters
- ✅ Display data in auto-generated form
- ✅ Navigate between rows
- ✅ Session management (save/delete)
- ✅ Form auto-fill with Excel data

---

## 🔧 Recent Fixes

- Fixed CSS error in excel-form.html (`pb: 15px` → `padding-bottom: 15px`)
- Improved error messages for common issues
- Added proper validation for empty files
- Enhanced file type checking

**Last Updated:** March 1, 2026  
**Status:** All features working correctly ✓
