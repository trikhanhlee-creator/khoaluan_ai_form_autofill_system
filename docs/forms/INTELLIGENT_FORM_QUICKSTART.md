# Intelligent Form Detection - Quick Start Guide

## 🚀 Quick Start (5 mins)

### 1. Prepare Your Document

Create a Word document with:
- **Titles/Headers** (e.g., "ĐƠN XIN VIỆC")
- **Field Labels** ending with `:` (e.g., "Tôi tên là:")
- **Placeholders** (dots, underscores, dashes: `......`, `_____`, `-----`)

Example:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
ĐƠN XIN VIỆC

Tôi tên là: ........................................................
Sinh ngày: ___/___/_______
Số điện thoại: __________________
```

### 2. Upload Document

```bash
curl -X POST "http://localhost:8000/api/form-replacement/upload-with-intelligent-detection" \
  -F "file=@form.docx" \
  -F "user_id=1"
```

Response:
```json
{
  "status": "success",
  "template_id": 123,
  "fields_count": 3,
  "fields": [
    {"name": "toi_ten_la", "label": "Tôi tên là", "field_type": "text"},
    {"name": "sinh_ngay", "label": "Sinh ngày", "field_type": "date"},
    {"name": "so_dien_thoai", "label": "Số điện thoại", "field_type": "phone"}
  ]
}
```

### 3. Render Form (Structured)

```bash
curl "http://localhost:8000/api/form-replacement/template/123/render-form-structured"
```

HTML Output:
```html
<div class="form-container">
  <div class="form-title-main">CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM</div>
  <div class="form-title-main">ĐƠN XIN VIỆC</div>
  
  <div class="form-field">
    <label for="toi_ten_la">Tôi tên là:</label>
    <input type="text" name="toi_ten_la" />
  </div>
  
  <div class="form-field">
    <label for="sinh_ngay">Sinh ngày:</label>
    <input type="date" name="sinh_ngay" />
  </div>
  ...
</div>
```

### 4. Render Form (Inline - Preserve Layout)

```bash
curl "http://localhost:8000/api/form-replacement/template/123/render-form-inline"
```

HTML Output:
```html
<div class="form-document">
  <p>CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM</p>
  <p>ĐƠN XIN VIỆC</p>
  
  <p>Tôi tên là: <input type="text" name="toi_ten_la" /></p>
  <p>Sinh ngày: <input type="date" name="sinh_ngay" /></p>
  ...
</div>
```

---

## 🎯 API Endpoints

### Upload
- **POST** `/api/form-replacement/upload-with-intelligent-detection`
- Params: `file`, `user_id` (optional)
- Returns: Template ID + fields detected

### Render (Organized)
- **GET** `/api/form-replacement/template/{template_id}/render-form-structured`
- Params: `user_id` (optional)
- Returns: HTML form with sections organized

### Render (Original Layout)
- **GET** `/api/form-replacement/template/{template_id}/render-form-inline`
- Params: `user_id` (optional)
- Returns: HTML form with original layout preserved

---

## 📝 Field Type Detection

| Label Contains | Auto Type | HTML Input |
|---|---|---|
| ngày, sinh | date | `<input type="date">` |
| điện thoại, liên hệ | phone | `<input type="tel">` |
| email | email | `<input type="email">` |
| số, năm, tuổi | number | `<input type="number">` |
| ghi chú, mô tả, kinh nghiệm | textarea | `<textarea>` |
| (default) | text | `<input type="text">` |

---

## 💻 Python Integration

```python
from docx import Document
from app.services.form_replacement import IntelligentDetector, SmartFormRenderer

# Load document
doc = Document("form.docx")

# Parse
parsed_form = IntelligentDetector.parse_document(doc)

# Get fields
fields = IntelligentDetector.extract_field_list(parsed_form)
print(f"Found {len(fields)} fields")

# Render
html = SmartFormRenderer.render_form_html(parsed_form)
print(html)
```

---

## 🔍 What Gets Detected

✅ **Titles**
- All caps: `CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM`
- Form titles: `ĐƠN XIN VIỆC`

✅ **Field Labels**
- Colon format: `Tôi tên là:`
- Chinese colon: `Tôi tên là：`
- With context: `Sinh ngày: ___/___/_______`

✅ **Placeholders**
- Dots: `......`
- Underscores: `_____`
- Dashes: `-----`
- Unicode: `─────`

✅ **Sections**
- Headerและ
- Main content
- Organized structure

---

## ❌ Common Issues

### No fields detected
**Problem:** Document has no placeholders
**Solution:** Add `......` or `_____` after field labels

### Wrong field type
**Problem:** Label doesn't match keywords
**Solution:** 
- For dates, include "ngày" or "sinh"
- For phones, include "điện thoại"
- For email, include "email"

### Layout not preserved
**Problem:** Using structured rendering
**Solution:** Use inline rendering instead
```bash
/template/123/render-form-inline  # Preserves layout
/template/123/render-form-structured  # Organized view
```

---

## 📊 Examples

### Example 1: Job Application Form
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN XIN VIỆC

Kính gửi: Ban lãnh đạo Công ty ..........................................

Tôi tên là: ........................................................

Sinh ngày: ___/___/__________

Chỗ ở hiện nay: ........................................................

Số điện thoại: __________________

Tôi cảm thấy trình độ và kỹ năng của mình phù hợp với vị trí này.
Tôi mong muốn được làm việc cho công ty.
```

→ **Result:** 5 fields detected + 2 sections + proper structure

### Example 2: Customer Form
```
FORM THÔNG TIN KHÁCH HÀNG

Họ tên: ................................................

Email: ................................................

Số điện thoại: __________________

Các ghi chú: ................................................
```

→ **Result:** 4 fields detected + correct types (email, phone, textarea)

---

## 🧪 Testing

```bash
# Run unit test
cd backend
python tests_debug/test_intelligent_detector.py

# Run integration test
python tests_debug/test_integration_intelligent_form.py

# Check API
python -c "from app.main import app; print('✅ API OK')"
```

Expected: `✅ ALL TESTS PASSED`

---

## 📚 Files Reference

| File | Purpose |
|------|---------|
| `intelligent_detector.py` | Phát hiện cấu trúc form |
| `smart_form_renderer.py` | Render form HTML |
| `form_replacement.py` (API) | REST endpoints |

---

## 🎨 Customization

### Change field type for specific label
Edit `FIELD_TYPE_KEYWORDS` in `intelligent_detector.py`:
```python
FIELD_TYPE_KEYWORDS = {
    'custom_label': 'custom_type',  # Add here
    ...
}
```

### Change HTML styling
Modify style attributes in `smart_form_renderer.py`:
```python
base_style = "padding: 10px; border: 2px solid red;"  # Your style
```

---

## ✨ Features

- ✅ Smart title detection
- ✅ Label extraction from context
- ✅ Auto field type detection
- ✅ Document structure preservation
- ✅ Both structured & inline rendering
- ✅ Full Vietnamese support
- ✅ Section organization

---

## 🚀 Next Steps

1. Prepare your .docx file with titles and field labels
2. Upload via API
3. Choose rendering mode (structured or inline)
4. Receive interactive HTML form
5. Integrate into your application

---

## 📞 Support

For detailed API documentation, see: [INTELLIGENT_FORM_DETECTION.md](../INTELLIGENT_FORM_DETECTION.md)
