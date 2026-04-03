## 🚀 Form Replacement Service - Quick Start

### 📌 What is This?

Instead of parsing complex document structure, simply **replace dot-lines with input fields**:

```
Input:
├─ Họ tên: .............................
├─ Ngày sinh: ___/___/______
└─ Địa chỉ: .............................

Output:
├─ Họ tên: [input field]
├─ Ngày sinh: [date picker]
└─ Địa chỉ: [input field]
```

---

## 🎯 Key Features

✅ Detect dot-line placeholders (`.`, `_`, `-`, `─`)  
✅ Extract fields automatically  
✅ Preserve document layout  
✅ Generate HTML form  
✅ Type-aware fields (text, number, date, email, phone)  
✅ Separate folder (no impact on existing features)  

---

## 🧪 Quick Test

```bash
cd backend
python tests_debug/test_form_replacement.py
```

**Expected Output:**
```
✅ ALL TESTS COMPLETED
  - Test 1: Dot-Line Detection ✅
  - Test 2: Field Extraction ✅
  - Test 3: HTML Rendering ✅
```

---

## 📁 File Structure

```
backend/app/services/form_replacement/
├── __init__.py                    # Imports & exports
├── dot_line_detector.py          # Core detection
├── field_replacer.py             # HTML/DOCX replacement
└── models.py                     # Data models

backend/app/api/routes/
├── form_replacement.py           # NEW API routes

backend/tests_debug/
└── test_form_replacement.py      # NEW Tests
```

---

## 🔌 API Endpoints

### 1. Upload File
```
POST /api/form-replacement/upload-with-dotlines
```
**Upload file with dot-lines → Get fields**

### 2. Render Form
```
GET /api/form-replacement/template/{template_id}/render-form
```
**Get HTML form with input fields replacing dot-lines**

### 3. List Templates
```
GET /api/form-replacement/templates-with-dotlines
```
**Get all uploaded templates**

### 4. Submit Form
```
POST /api/form-replacement/submit-dotline-form
```
**Submit form data**

---

## 💡 How It Works

### Step 1: Create Document with Dot-Lines
```
Họ tên: .............................
Ngày sinh: ___/___/______
Địa chỉ: .............................
Số điện thoại: ___________________
```

### Step 2: Upload to System
```bash
curl -X POST http://localhost:8000/api/form-replacement/upload-with-dotlines \
  -F "file=@form.docx" \
  -F "user_id=1"
```

### Step 3: Get Response
```json
{
  "status": "success",
  "template_id": 1,
  "fields_count": 4,
  "fields": [
    {"name": "ho_ten", "label": "Họ tên", "type": "text"},
    {"name": "ngay_sinh", "label": "Ngày sinh", "type": "date"},
    ...
  ]
}
```

### Step 4: Render Form
```bash
curl http://localhost:8000/api/form-replacement/template/1/render-form
```

### Step 5: Display Form (HTML)
```html
<form>
  <p>Họ tên: <input type="text" name="ho_ten" /></p>
  <p>Ngày sinh: <input type="date" name="ngay_sinh" /></p>
  <p>Địa chỉ: <input type="text" name="dia_chi" /></p>
  <p>Số điện thoại: <input type="tel" name="so_dien_thoai" /></p>
</form>
```

### Step 6: Submit
```bash
curl -X POST http://localhost:8000/api/form-replacement/submit-dotline-form \
  -H "Content-Type: application/json" \
  -d '{
    "ho_ten": "Nguyễn Văn A",
    "ngay_sinh": "1990-01-01",
    "dia_chi": "123 Đường ABC",
    "so_dien_thoai": "0901234567"
  }' \
  --url-param template_id=1
```

---

## 🎨 Supported Dot-Line Patterns

| Pattern | Example | Detected |
|---------|---------|----------|
| Dots | `Họ tên: .............................` | ✅ Yes |
| Underscores | `Ngày: ___/___/______` | ✅ Yes |
| Dashes | `Địa chỉ: --------------------` | ✅ Yes |
| Unicode | `Số điện thoại: ─────────────` | ✅ Yes |

---

## 🏷️ Field Type Detection

| Label Contains | Detected As |
|---|---|
| "năm", "năm sinh" | `number` |
| "ngày", "ngài sinh" | `date` |
| "điện thoại", "số điện thoại" | `phone` |
| "email" | `email` |
| (anything else) | `text` |

---

## ✅ Testing

### Run All Tests
```bash
cd backend
python tests_debug/test_form_replacement.py
```

### Individual Tests
```bash
# Test 1: Detection
python -c "
from tests_debug.test_form_replacement import test_dot_line_detection
test_dot_line_detection()
"

# Test 2: Extraction
python -c "
from tests_debug.test_form_replacement import test_field_extraction
test_field_extraction()
"

# Test 3: Rendering
python -c "
from tests_debug.test_form_replacement import test_dot_line_replacement
test_dot_line_replacement()
"
```

---

## 🛠️ Integration with Existing Code

### ✅ Isolated
- Separate folder: `form_replacement/`
- Separate routes: `form_replacement.py`
- No changes to existing files (except `main.py` to include routes)

### ✅ Compatible
- Uses existing database models (`WordTemplate`, etc.)
- Uses existing middleware
- Works alongside existing endpoints

### ✅ Non-Breaking
- Existing `/api/word/*` endpoints untouched
- New `/api/form-replacement/*` endpoints added
- Users choose which method to use

---

## 📊 Example Document

### Input (form.docx)
```
╔════════════════════════════════════════════════╗
║  CÔNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM         ║
║  ĐƠN XIN VIỆC                                ║
╚════════════════════════════════════════════════╝

Kính gửi: Ban lãnh đạo và phòng nhân sự Công ty
..................................................

Tôi tên là: .....................................................
Sinh ngày: ___/___/______
Chỗ ở hiện nay: .....................................................
Số điện thoại liên hệ: .....................................................

Thông qua trang website TopCV.vn, tôi biết được Quý công ty có nhân tố
tuyển dụng vị trí: ....................... Tôi cảm thấy trình độ và kỹ năng 
của mình phù hợp với vị trí này. Tôi mong muốn được làm việc và công hiến 
cho công ty.

Tôi đã tốt nghiệp loại: ...... tại trường: .....................................................................
```

### Output (Rendered Form)
```
Kính gửi: Ban lãnh đạo và phòng nhân sự Công ty
[input: company_intro]

Tôi tên là: [input: ho_ten]
Sinh ngày: [date_picker: ngay_sinh]
Chỗ ở hiện nay: [input: dia_chi]
Số điện thoại liên hệ: [tel_input: so_dien_thoai]

Thông qua trang website TopCV.vn, tôi biết được Quý công ty có nhân tố
tuyển dụng vị trí: [input: vi_tri_tuyen_dung] ...

Tôi đã tốt nghiệp loại: [input: loai_tot_nghiep]
tại trường: [input: truong_hoc]
```

---

## 🎯 Use Cases

✅ **Job Application Forms** - Common to have dot-lines for name, address  
✅ **Official Documents** - Vietnamese forms often have `______` placeholders  
✅ **Official Requests** - Permission slips, reports with structured dot-lines  
✅ **Invoice Templates** - Fields like date, customer name on dot-lines  
✅ **Survey Forms** - Questionnaires with line-based fill-ins  

---

## ⚠️ Limitations

❌ Only `.docx` files (future: `.pdf`, `.xlsx`)  
❌ Single dot-line per line (future: multi-line fields)  
❌ Basic type detection (future: ML-based)  

---

## 🔄 Comparison: Form Replacement vs Existing Upload

| Feature | Form Replacement | Traditional Upload |
|---------|-----------------|-------------------|
| **Detection** | Dot-line patterns | Structure parsing |
| **Complexity** | O(n) | O(n) + parsing |
| **Layout** | Preserved visually | Generated form |
| **Use Case** | Pre-formatted docs | Unstructured files |
| **Folder** | `form_replacement/` | `file_parser.py` |

---

## 📞 Support

**Documentation:** See `FORM_REPLACEMENT_SERVICE.md`  
**Tests:** Run `python tests_debug/test_form_replacement.py`  
**Issues:** Check server logs at `/backend/logs/`

---

**Status:** ✅ Ready to Use  
**All Tests:** 3/3 Passed  
**Isolated:** Yes (separate folder)
