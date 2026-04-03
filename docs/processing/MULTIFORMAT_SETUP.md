# Multi-Format File Upload - Implementation Guide

## Tổng Quan
Hệ thống đã được nâng cấp để hỗ trợ upload và parse các định dạng file khác nhau, không chỉ riêng `.docx` nữa.

## Các Định Dạng Được Hỗ Trợ

| Định Dạng | Phần Mở Rộng | Mô Tả | Cách Parse |
|-----------|------------|-------|-----------|
| Word Document | `.docx` | Microsoft Word 2007+ | Paragraphs, Tables |
| PDF | `.pdf` | Portable Document Format | Text extraction |
| Excel | `.xlsx` | Microsoft Excel 2007+ | Header row hoặc Column 1 |
| Excel Cũ | `.xls` | Microsoft Excel 97-2003 | Header row hoặc Column 1 |
| CSV | `.csv` | Comma-Separated Values | Header row hoặc Column 1 |
| Text | `.txt` | Plain Text File | Line-by-line parsing |

## Cấu Trúc Kỹ Thuật

### Thư Mục Chính

```
backend/app/services/
├── file_parser.py          [NEW] Multi-format parser with factory pattern
├── word_parser.py          [UPDATED] Backward compatibility wrapper
└── ...
```

### File Parser Architecture

#### Base Class: `BaseFileParser`
- Các hàm chung: `clean_field_label()`, `detect_field_type()`, `create_field_name()`
- Abstract method: `parse()`

#### Concrete Implementations
- `DocxParser`: Parse Word documents
- `PdfParser`: Extract text from PDF files
- `XlsxParser`: Parse Excel spreadsheets
- `CsvParser`: Parse CSV files
- `TxtParser`: Parse plain text files

#### Factory Class: `FileParserFactory`
```python
# Cách sử dụng
parser = FileParserFactory.create_parser(file_path)
fields = parser.parse()
metadata = parser.get_metadata()

# Kiểm tra định dạng
supported_exts = FileParserFactory.get_supported_extensions()
is_supported = FileParserFactory.is_supported(file_path)
```

## API Endpoints

### 1. Upload File
**POST** `/api/word/upload`

**Hỗ trợ tất cả định dạng:** `.docx`, `.pdf`, `.xlsx`, `.xls`, `.csv`, `.txt`

**Request:**
```json
{
  "file": <binary>,
  "user_id": 1
}
```

**Response:**
```json
{
  "status": "success",
  "template_id": 123,
  "template_name": "Form Name",
  "file_type": ".pdf",
  "fields_count": 5,
  "fields": [
    {
      "name": "username",
      "field_type": "text",
      "label": "Username",
      "order": 0
    }
  ],
  "auto_generated_fields": false,
  "message": "Upload và parse thành công"
}
```

### 2. Lấy Định Dạng Được Hỗ Trợ
**GET** `/api/word/supported-formats`

**Response:**
```json
{
  "supported_extensions": [".docx", ".pdf", ".xlsx", ".xls", ".csv", ".txt"],
  "description": {
    ".docx": "Word Document",
    ".pdf": "PDF File",
    ".xlsx": "Excel Spreadsheet (2007+)",
    ".xls": "Excel Spreadsheet (97-2003)",
    ".csv": "Comma-Separated Values",
    ".txt": "Plain Text File"
  }
}
```

## Cách Parse Các Định Dạng

### Word (.docx)
1. **Priority 1**: Parse from paragraphs (methods có ":" hoặc dòng ngắn)
2. **Priority 2**: Parse from tables (cột đầu tiên)
3. **Fallback**: Extract tất cả text content

### PDF (.pdf)
- Extract text từ tất cả trang
- Parse theo dòng, tìm các field descriptor (có ":" hoặc dòng ngắn)

### Excel (.xlsx, .xls)
1. **Header row**: Nếu dòng đầu tiên có data, sử dụng làm header
2. **Column 1**: Nếu không có header, lấy các cell từ cột đầu tiên
3. Giới hạn: 20 dòng đầu tiên

### CSV (.csv)
1. **Header row**: Nếu dòng đầu tiên không rỗng, sử dụng làm header
2. **Column 1**: Nếu không có header, lấy từ cột đầu tiên
3. Auto-detect encoding (UTF-8 hoặc Latin-1)

### Text (.txt)
- Parse theo dòng
- Tìm các field descriptor (có ":" hoặc dòng ngắn)
- Giới hạn: 20 fields

## Field Type Detection

Hệ thống tự động phát hiện kiểu field dựa trên từ khóa trong nhãn:

```python
FIELD_TYPE_KEYWORDS = {
    'năm': 'number',
    'ngày': 'date',
    'điện thoại': 'phone',
    'email': 'email',
    'địa chỉ': 'text',
    'tên': 'text',
    'họ': 'text',
    'số': 'number',
    'năm sinh': 'number',
}
```

## Backward Compatibility

Lớp `WordParser` vẫn có thể sử dụng như trước:

```python
from app.services.word_parser import WordParser

parser = WordParser('file.pdf')  # Giờ đây support tất cả format!
fields = parser.parse()
metadata = parser.get_metadata()
```

## Dependencies

```
python-docx>=0.8.11       # Word document parsing
pypdf==4.0.1             # PDF reading
openpyxl>=3.1.2          # Excel file reading
pdfplumber>=0.10.3       # PDF text extraction
```

## Error Handling

### Unsupported Format
```
Status: 400
Detail: "Không hỗ trợ định dạng file: .xyz. Các định dạng được hỗ trợ: .docx, .pdf, .xlsx, .xls, .csv, .txt"
```

### File Not Found
```
Status: 500
Detail: "Lỗi: File không tồn tại: /path/to/file"
```

### Parse Error
```
Status: 500
Detail: "Lỗi: [specific error message]"
```

## Testing

Chạy test script để verify implementation:

```bash
python tests_debug/test_multiformat_parser.py
```

Expected output:
```
✓ Supported Formats
✓ Parser Creation
✓ Format Rejection
Total: 3/3 tests passed
```

## Lợi Ích

1. ✅ **Hỗ trợ nhiều định dạng**: Người dùng có thể upload từ các nguồn khác nhau
2. ✅ **Tương thích ngược**: Code cũ vẫn hoạt động
3. ✅ **Mở rộng dễ dàng**: Thêm format mới chỉ cần tạo class mới
4. ✅ **Lỗi rõ ràng**: Thông báo lỗi chi tiết cho người dùng
5. ✅ **Extraction thông minh**: Phát hiện tự động field types

## Ví Dụ Sử Dụng

### Upload từ HTML Form
```html
<form action="/api/word/upload" method="POST" enctype="multipart/form-data">
  <input type="file" name="file" accept=".docx,.pdf,.xlsx,.csv,.txt">
  <input type="hidden" name="user_id" value="1">
  <button type="submit">Upload</button>
</form>
```

### Upload từ Python
```python
import requests

files = {'file': open('form.pdf', 'rb')}
data = {'user_id': 1}
response = requests.post('http://localhost:8000/api/word/upload', 
                        files=files, data=data)
print(response.json())
```

### Upload từ JavaScript/Fetch
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('user_id', 1);

const response = await fetch('/api/word/upload', {
  method: 'POST',
  body: formData
});
const result = await response.json();
```

## Khắc Phục Sự Cố

### PDF không parse được
- Đảm bảo PDF có text (không chỉ hình ảnh)
- Kiểm tra encoding của text trong PDF

### Excel không tìm được fields
- Kiểm tra xem file có header row không
- Hoặc cột đầu tiên phải có field descriptors

### CSV parse không đúng
- Kiểm tra delimiter (phải là comma)
- Kiểm tra encoding (UTF-8 hoặc Latin-1)

## Tương Lai

Có thể mở rộng hỗ trợ thêm các format:
- `.odt` - LibreOffice Writer
- `.pptx` - PowerPoint
- `.json` - JSON files
- `.xml` - XML files
- Database connects
