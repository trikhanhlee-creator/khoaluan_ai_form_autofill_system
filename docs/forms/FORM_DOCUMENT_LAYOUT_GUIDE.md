# Form Document Layout Rendering - Complete Guide

## 🎯 Giải pháp cho Vấn đề

Khi upload một form đã có cấu trúc định dạng sẵn, form tạo ra sẽ:
- ✅ **Giữ nguyên layout document** - Tiêu đề ở centro, fields phía dưới
- ✅ **Phân biệt tiêu đề vs trường** - Tiêu đề là text không editable, trường là input boxes
- ✅ **Hiển thị giống hình ảnh** - Layout chính xác như document gốc

---

## API Endpoints

### 1. Upload Form

```bash
curl -X POST "http://localhost:8000/api/form-replacement/upload-with-intelligent-detection" \
  -F "file=@form.docx" \
  -F "user_id=1"
```

**Response:**
```json
{
  "status": "success",
  "template_id": 123,
  "fields_count": 5,
  "sections_count": 2,
  "fields": [...]
}
```

### 2. Render as Document Layout (RECOMMENDED)

```bash
curl "http://localhost:8000/api/form-replacement/template/123/render-form-document"
```

**Response:**
```json
{
  "status": "success",
  "template_id": 123,
  "render_type": "document",
  "html_form": "<div class=\"form-document-style\">...</div>"
}
```

**Characteristics:**
- ✅ Tiêu đề centered, bold, uppercase
- ✅ Cada field có label + input box
- ✅ Input box có border (giống form trong hình)
- ✅ Layout chính xác

### 3. Render as Complete Page

```bash
curl "http://localhost:8000/api/form-replacement/template/123/render-form-page"
```

**Response:**
```json
{
  "status": "success",
  "render_type": "page",
  "html_page": "<!DOCTYPE html><html>...</html>"
}
```

**Characteristics:**
- ✅ Complete HTML page with CSS
- ✅ JavaScript functionality
- ✅ Submit/Reset buttons
- ✅ Ready to display directly

---

## HTML Output Example

### Document Layout Rendering

```html
<div class="form-document-style">
  <!-- Title (non-editable) -->
  <div style="text-align: center; font-weight: bold; ...">
    CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
  </div>
  
  <!-- Subtitle -->
  <div style="text-align: center; font-style: italic; ...">
    Độc lập - Tự do - Hạnh phúc
  </div>
  
  <!-- Main Form Title -->
  <div style="text-align: center; font-weight: bold; ...">
    ĐƠN XIN VIỆC
  </div>
  
  <!-- Fields with input boxes -->
  <p>
    <span>Tôi tên là:</span>
    <input type="text" style="border: 1.5px solid #000; ..." />
  </p>
  
  <p>
    <span>Sinh ngày:</span>
    <input type="date" style="border: 1.5px solid #000; ..." />
  </p>
  
  <!-- More fields... -->
</div>
```

---

## Integration Example

### Python

```python
import requests

# 1. Upload
response = requests.post(
    "http://localhost:8000/api/form-replacement/upload-with-intelligent-detection",
    files={"file": open("form.docx", "rb")},
    params={"user_id": 1}
)

template_id = response.json()["template_id"]

# 2. Get Document Layout
response = requests.get(
    f"http://localhost:8000/api/form-replacement/template/{template_id}/render-form-document"
)

html_form = response.json()["html_form"]

# 3. Display in web page
print(html_form)
```

### JavaScript

```javascript
// Get form HTML
fetch(`/api/form-replacement/template/123/render-form-document`)
  .then(r => r.json())
  .then(d => {
    // Insert into page
    document.getElementById("form-container").innerHTML = d.html_form;
  });
```

---

## Key Features

### 1. Tiêu Đề (Title) - Non-Editable
```html
<div style="text-align: center; font-weight: bold; font-size: 22px; text-transform: uppercase;">
  CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
</div>
```

### 2. Trường (Field) - Editable with Input Box
```html
<div>
  <span>Tôi tên là:</span>
  <input type="text" style="border: 1.5px solid #000; padding: 8px; ..." 
    data-field-label="Tôi tên là" 
    data-field-type="text" />
</div>
```

### 3. Field Types
System tự động detect kiểu field:
- **Date:** Contains "ngày", "sinh" → `<input type="date">`
- **Phone:** Contains "điện thoại" → `<input type="tel">`
- **Email:** Contains "email" → `<input type="email">`
- **Number:** Contains "số", "năm" → `<input type="number">`
- **Text:** Default → `<input type="text">`

---

## Rendering Modes Comparison

| Aspect | Structured | Inline | Document | Page |
|--------|-----------|--------|----------|------|
| Layout | Organized | Original | Document | Complete |
| Titles | Visible | In text | Centered | Centered |
| Fields | Listed | Inline | Labeled boxes | With buttons |
| CSS | Minimal | Minimal | Full styling | Complete page |
| Use Case | Clean form | Original look | Like image | Ready display |

---

## Step-by-Step Usage

### Step 1: Prepare Document
Create `.docx` with:
- **Titles:** All-caps text (centered optional)
- **Labels:** Text ending with `:` (e.g., "Tôi tên là:")
- **Placeholders:** Dots/underscores/dashes (`.....`, `_____`, `-----`)

Example:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN XIN VIỆC

Tôi tên là: ................
Sinh ngày: ___/___/______
```

### Step 2: Upload
```bash
curl -X POST "http://localhost:8000/api/form-replacement/upload-with-intelligent-detection" \
  -F "file=@form.docx"
```

### Step 3: Get Template ID
```json
{
  "template_id": 123,
  "fields_count": 2
}
```

### Step 4: Render Document
```bash
curl "http://localhost:8000/api/form-replacement/template/123/render-form-document"
```

### Step 5: Display in UI
Insert `html_form` into your web page

### Step 6: Collect Data
Get form values:
```javascript
const fields = document.querySelectorAll('[data-field-label]');
const data = {};
fields.forEach(f => {
  data[f.name] = f.value;
});
```

---

## Styling Options

### Modify Input Box Style
Edit `form_layout_renderer.py`:
```python
box_style = """
    border: 1.5px solid #000;        # ← Border color/thickness
    padding: 8px 10px;                # ← Spacing inside
    font-family: 'Arial', sans-serif;  # ← Font
    font-size: 13px;                  # ← Font size
"""
```

### Modify Label Style
```python
label_style = """
    font-weight: 500;      # ← Bold level
    margin-right: 8px;     # ← Space between label and input
"""
```

---

## Testing

Run test:
```bash
python tests_debug/test_form_layout_renderer.py
```

Expected output:
```
✅ Generated 5136 characters
✅ Contains 5 input elements
✅ ALL TESTS PASSED!
```

---

## API Response Structure

```json
{
  "status": "success",
  "template_id": 123,
  "template_name": "Don_Xin_Viec",
  "fields_count": 5,
  "sections_count": 2,
  "fields": [
    {
      "order": 0,
      "name": "toi_ten_la",
      "label": "Tôi tên là",
      "field_type": "text",
      "section_index": 1,
      "required": true
    },
    ...
  ],
  "html_form": "<div class=\"form-document-style\">...</div>",
  "render_type": "document",
  "message": "Form render thành công (document layout)"
}
```

---

## Troubleshooting

### No fields detected
**Problem:** Input placeholders not recognized
**Solution:** Use `.....`, `_____`, or `-----` (2+ characters)

### Wrong layout
**Problem:** Use inline rendering instead of document
**Solution:** Use `/template/{id}/render-form-document` endpoint

### Fields overlap
**Problem:** CSS styling issue
**Solution:** Adjust padding/margin in FormLayoutRenderer

### Vietnamese characters broken
**Problem:** Encoding issue
**Solution:** Ensure file encoded as UTF-8

---

## Next Steps

1. Upload your form document
2. Call document layout endpoint
3. Insert HTML into your web page
4. Collect form data
5. Submit to your backend

---

## More Options

- **Structured Form:** `/render-form-structured` - Organized view
- **Inline Form:** `/render-form-inline` - Original layout
- **Complete Page:** `/render-form-page` - Ready to display

Choose the one that best fits your needs!
