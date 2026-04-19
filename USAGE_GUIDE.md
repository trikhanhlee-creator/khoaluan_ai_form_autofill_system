# Hướng dẫn Sử Dụng AutoFill AI System

## 🎯 Hai Giao Diện Chính

### 1. AutoFill Form (Gợi ý tự động)
**URL**: http://127.0.0.1:8000/static/form.html

**Cách dùng**:
1. Gõ vào các ô input (Họ tên, Email, SĐT, Thành phố, Công ty)
2. Hệ thống tự động gợi ý từ lịch sử nhập liệu
3. Click gợi ý hoặc gõ xong nhấn Enter
4. Dữ liệu được lưu vào lịch sử tự động
5. Lần nhập sau sẽ thấy gợi ý từ những lần trước

**Lưu ý**: 
- Gợi ý xuất hiện khi có ≥ 2 lần nhập trùng
- Dữ liệu được lưu khi blur input (click ra ngoài)

---

### 2. Word Upload & Form Builder
**URL**: http://127.0.0.1:8000/ui/word-upload.html

**Cách dùng**:
1. **Upload file Word**:
   - Drag & drop file .docx vào upload area
   - Hoặc click để chọn file

2. **Hệ thống tự động**:
   - Parse file → trích xuất fields
   - Phát hiện kiểu dữ liệu (text, number, date, email, phone)
   - Tạo danh sách templates

3. **Điền form**:
   - Click "✏️ Điền" để mở form
   - Điền dữ liệu
   - Click "💾 Lưu & Submit" để lưu

4. **Xem lịch sử**:
   - Bảng history hiển thị tất cả submissions
   - Có thể xóa templates

**Định dạng file Word hỗ trợ**:
```
Họ và tên:
Năm sinh:
Địa chỉ:
```

---

## 📊 Database Schema

### entries (Lịch sử nhập liệu)
- Được tạo khi người dùng nhập dữ liệu
- Lưu: user_id, field_id, form_id, value, created_at
- Dùng cho: Tính toán gợi ý

### suggestions (Gợi ý)
- Được tạo từ entries
- Lưu: user_id, field_id, suggested_value, frequency, ranking
- Tần suất = số lần value xuất hiện
- Ranking = thứ tự gợi ý

### word_templates (Templates từ Word)
- Lưu: user_id, template_name, file_path, fields_json, created_at
- fields_json = danh sách fields được parse

### word_submissions (Submissions từ Word forms)
- Lưu: template_id, user_id, submission_data (JSON), created_at
- submission_data = dữ liệu mà người dùng điền

---

## 🔧 Xem Dữ Liệu Trong Database

### Xem entries (lịch sử nhập)
```bash
cd backend
python -c "
from app.db.session import SessionLocal
from app.db.models import Entry

db = SessionLocal()
entries = db.query(Entry).filter(Entry.user_id == 1).all()
print(f'Total entries: {len(entries)}')
for e in entries[-10:]:
    print(f'  - Field {e.field_id}: {e.value}')
db.close()
"
```

### Xem suggestions (gợi ý)
```bash
python -c "
from app.db.session import SessionLocal
from app.db.models import Suggestion

db = SessionLocal()
suggs = db.query(Suggestion).filter(Suggestion.user_id == 1).all()
print(f'Total suggestions: {len(suggs)}')
for s in suggs[:5]:
    print(f'  - Field {s.field_id}: {s.suggested_value} (freq: {s.frequency})')
db.close()
"
```

### Xem word templates
```bash
python -c "
from app.db.session import SessionLocal
from app.db.models import WordTemplate

db = SessionLocal()
templates = db.query(WordTemplate).all()
print(f'Total templates: {len(templates)}')
for t in templates:
    print(f'  - {t.template_name} ({t.id})')
db.close()
"
```

---

## 🚀 Quy Trình Hoạt Động

### AutoFill Form Flow
```
User types in field
    ↓
API: /api/suggestions (GET)
    ↓
Query suggestions from database
    ↓
Return top 5 suggestions
    ↓
Display dropdown
    ↓
User selects or continues
    ↓
On blur → API: /api/suggestions/save (POST)
    ↓
Save entry to database
    ↓
Next time → suggestions will appear
```

### Word Form Flow
```
User uploads Word file
    ↓
POST /api/word/upload
    ↓
WordParser.parse()
    ↓
Extract fields (Họ tên, Năm sinh, etc)
    ↓
Save WordTemplate to DB
    ↓
Return template with fields
    ↓
UI renders dynamic form
    ↓
User fills data
    ↓
POST /api/word/submit
    ↓
Save WordSubmission to DB
    ↓
Show in history
```

---

## ⚠️ Troubleshooting

### Không thấy gợi ý
**Nguyên nhân**: Cần nhập ≥2 lần cùng value
**Giải pháp**: 
- Nhập "John" → Save
- Nhập "John" lần 2 → sẽ thấy gợi ý

### Upload Word fail
**Nguyên nhân**: 
- File không phải .docx
- File không có fields với format "Label:"

**Giải pháp**:
- Dùng Word 2007+ (.docx)
- Tạo file với format:
  ```
  Họ và tên:
  Năm sinh:
  Địa chỉ:
  ```

### Server không chạy
```bash
cd backend
python run.py
```

### Database error
```bash
cd backend
python scripts/maintenance/clean_data.py
python scripts/maintenance/setup_word_db.py
```

---

## 📈 Mở Rộng

### Thêm fields mới
Sửa form.html:
```html
<!-- Add new field in form -->
<div class="form-group">
    <label for="address">Địa chỉ</label>
    <div class="input-wrapper">
        <input type="text" id="address" placeholder="..." autocomplete="off">
        <div class="suggestions-dropdown" data-field="address"></div>
    </div>
</div>
```

Update FIELD_MAPPING:
```javascript
const FIELD_MAPPING = {
    'address': { field_id: 6, form_id: 1, label: 'Địa chỉ' },
    // ... other fields
};
```

### Import dữ liệu cũ
Tạo script import từ CSV/Excel → seed vào database

### API integrations
- Connect với CRM
- Sync với cloud storage
- Export data to Excel

---

## 📞 API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/suggestions` | Lấy gợi ý |
| POST | `/api/suggestions/save` | Lưu entry |
| POST | `/api/word/upload` | Upload Word file |
| GET | `/api/word/templates` | Danh sách templates |
| GET | `/api/word/template/{id}` | Chi tiết template |
| POST | `/api/word/submit` | Submit form data |
| GET | `/api/word/submissions` | Danh sách submissions |

---

**Version**: 1.0.0  
**Last Updated**: 27/01/2026  
**Status**: Production Ready ✅
