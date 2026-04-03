# Multi-Format Upload - Quick Developer Reference

## 🎯 Core Classes

### FileParserFactory
```python
from app.services.file_parser import FileParserFactory

# Get supported extensions
supported = FileParserFactory.get_supported_extensions()
# → ['.docx', '.pdf', '.xlsx', '.xls', '.csv', '.txt']

# Check if file is supported
is_ok = FileParserFactory.is_supported('form.pdf')
# → True

# Create appropriate parser
parser = FileParserFactory.create_parser('form.pdf')
# → PdfParser instance

# Parse and get fields
fields = parser.parse()
# → List[FileField]

# Get metadata
metadata = parser.get_metadata()
# → Dict with file info
```

### FileField
```python
class FileField:
    name: str          # field name (snake_case)
    field_type: str    # 'text', 'number', 'date', 'phone', 'email'
    label: str         # Display label
    order: int         # Field order
    
    # Convert to dict
    field.to_dict()
    # → {'name': '...', 'field_type': '...', 'label': '...', 'order': 0}
```

### Individual Parsers

#### DocxParser
```python
from app.services.file_parser import DocxParser

parser = DocxParser('document.docx')
fields = parser.parse()
# Parses: Paragraphs → Tables → All Content
```

#### PdfParser
```python
from app.services.file_parser import PdfParser

parser = PdfParser('document.pdf')
fields = parser.parse()
# Extracts text from all pages and parses
```

#### XlsxParser
```python
from app.services.file_parser import XlsxParser

parser = XlsxParser('spreadsheet.xlsx')
fields = parser.parse()
# Uses: Header row → Column 1 descriptions
```

#### CsvParser
```python
from app.services.file_parser import CsvParser

parser = CsvParser('data.csv')
fields = parser.parse()
# Uses: Header row → Column 1 descriptions
# Auto-detects encoding: UTF-8 or Latin-1
```

#### TxtParser
```python
from app.services.file_parser import TxtParser

parser = TxtParser('form.txt')
fields = parser.parse()
# Parses line by line, max 20 fields
```

## 🔄 Backward Compatibility

Old code still works:
```python
from app.services.word_parser import WordParser

# Now supports ALL formats!
parser = WordParser('form.pdf')   # Works!
parser = WordParser('data.csv')   # Works!
parser = WordParser('doc.docx')   # Works!

fields = parser.parse()
metadata = parser.get_metadata()
```

## 📝 Field Type Detection

Automatic detection from field labels:

| Keyword | Detected Type |
|---------|---------------|
| năm | number |
| ngày | date |
| điện thoại | phone |
| email | email |
| địa chỉ | text |
| tên | text |
| họ | text |
| số | number |
| năm sinh | number |

## 🛠️ Custom Parser Example

To add support for new format:

```python
from app.services.file_parser import BaseFileParser, FileField

class MyFormatParser(BaseFileParser):
    SUPPORTED_EXTENSIONS = ['.myformat']
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
        # Load your format-specific library
        self.data = load_my_format(file_path)
    
    def parse(self) -> List[FileField]:
        fields = []
        order = 0
        
        for item in self.data:
            label = self.clean_field_label(item.name)
            field_name = self.create_field_name(label)
            field_type = self.detect_field_type(label)
            
            field = FileField(
                name=field_name,
                field_type=field_type,
                label=label,
                order=order
            )
            fields.append(field)
            order += 1
        
        self.fields = fields
        return fields

# Register in FileParserFactory
FileParserFactory.PARSERS['.myformat'] = MyFormatParser
```

## 🚀 API Usage Examples

### Get Supported Formats
```bash
GET /api/word/supported-formats

Response:
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

### Upload Document
```bash
POST /api/word/upload
Content-Type: multipart/form-data

file=<binary>
user_id=1

Response:
{
  "status": "success",
  "template_id": 123,
  "template_name": "My Form",
  "file_type": ".pdf",
  "fields_count": 5,
  "fields": [
    {"name": "username", "field_type": "text", "label": "Username", "order": 0},
    {"name": "email", "field_type": "email", "label": "Email", "order": 1}
  ],
  "auto_generated_fields": false,
  "message": "Upload và parse thành công"
}
```

## 📊 File Parsing Strategies

### Word (.docx)
1. Try paragraphs with separators (: . ─ etc)
2. Try tables (first column)
3. Fallback: all text content

### PDF (.pdf)
1. Extract all text
2. Parse by lines
3. Find field descriptors

### Excel (.xlsx, .xls)
1. Check first row for headers
2. If no headers, use first column
3. Limit to 20 rows max

### CSV (.csv)
1. Parse first row as headers
2. If no headers, use first column
3. Auto-detect encoding

### Text (.txt)
1. Parse line by line
2. Find field descriptors
3. Limit to 20 fields

## ⚠️ Error Handling

```python
# Unsupported format
try:
    parser = FileParserFactory.create_parser('file.xyz')
except ValueError as e:
    print(e)
    # "Không hỗ trợ định dạng file: .xyz. Các định dạng được hỗ trợ: ..."

# File not found
try:
    parser = FileParserFactory.create_parser('/path/nonexistent.pdf')
except FileNotFoundError as e:
    print(e)
    # "File không tồn tại: /path/nonexistent.pdf"

# Parse error
try:
    fields = parser.parse()
except Exception as e:
    print(f"Parse error: {e}")
```

## 🧪 Testing

```bash
# Run unit tests
python tests_debug/test_multiformat_parser.py

# Run integration tests (requires httpx)
pip install httpx
python tests_debug/test_multiformat_integration.py
```

## 📦 Dependencies

```
python-docx>=0.8.11      # .docx parsing
pypdf==4.0.1            # PDF reading
openpyxl>=3.1.2         # .xlsx parsing
pdfplumber>=0.10.3      # PDF text extraction
```

Install:
```bash
pip install -r requirements.txt
```

## 🎯 Design Principles

1. **Factory Pattern**: Single entry point for parser creation
2. **Template Method**: Base class defines parsing flow
3. **Strategy Pattern**: Different parsing strategies per format
4. **Single Responsibility**: Each parser handles one format
5. **Open/Closed**: Easy to extend with new formats
6. **Backward Compatible**: Old API still works
