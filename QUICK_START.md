# 🎯 Quick Start - AutoFill AI System

## ✅ Database Status: CLEAN

Database hiện tại **không có dữ liệu lịch sử** - đây là trạng thái sạch để bạn test từ đầu.

---

## 🚀 Flow Hoàn Chỉnh (Clean Database)

### Scenario 1: Upload Word File & Fill Form

#### Step 1: Upload File Word
```
URL: http://127.0.0.1:8000/ui/word-upload.html
```
1. Drag & drop `testform.docx` vào upload area
2. Hệ thống parse file → tìm 3 fields:
   - Họ và tên (text)
   - Năm sinh (number)
   - Địa chỉ (text)
3. Template được lưu vào database

#### Step 2: Điền Form Lần Thứ Nhất
1. Click "✏️ Điền" trên template
2. Form hiển thị
3. Nhập dữ liệu:
   - Họ và tên: `Nguyễn Văn A`
   - Năm sinh: `1990`
   - Địa chỉ: `123 Đường ABC`
4. Click "💾 Lưu & Submit"
5. **Entry được lưu vào database** (Entry 1)
6. Form quay lại danh sách

**Database State After Step 2:**
```
Entries: 1
  - ID 1: Field "họ_và_tên" = "Nguyễn Văn A"
  - (Plus 2 more entries for other fields)
```

#### Step 3: Điền Form Lần Thứ Hai (Gợi Ý Xuất Hiện)
1. Click "✏️ Điền" lại
2. **Gõ chữ cái đầu** trong ô "Họ và tên"
3. **✨ Suggestions xuất hiện!**
   - "Nguyễn Văn A" được gợi ý
4. Click để chọn hoặc tiếp tục gõ
5. Lúc này gợi ý từ lần nhập thứ nhất

**Lý do**: Cần ≥ 2 lần nhập cùng value để có gợi ý

---

### Scenario 2: AutoFill Form (Không Upload Word)

#### URL: http://127.0.0.1:8000/static/form.html

**Step 1: Nhập lần 1**
1. Gõ tên: `John Doe`
2. Gõ email: `john@example.com`
3. Click button "💾 Lưu Dữ Liệu"
4. Message: "✅ Đã lưu 2 trường"

**Step 2: Nhập lần 2 (Gợi ý Xuất Hiện)**
1. Click vào ô tên → gõ "J"
2. **💡 Gợi ý: "John Doe"** xuất hiện
3. Click để chọn
4. Hiển thị: "Sử dụng 2 lần, Lần cuối: hôm nay"

---

## 📊 Database Flow

```
[Clean Database]
     ↓
User enters data + Submit
     ↓
API: POST /api/word/submit  (Word forms)
   OR POST /api/suggestions/save  (AutoFill form)
     ↓
Entry saved to database
     ↓
Next time user enters
     ↓
API: GET /api/suggestions → Check database
     ↓
Suggestions displayed if frequency >= 2
```

---

## 🔄 Data Lifecycle

### AutoFill Form:
```
Input → Blur → API /suggestions/save 
   ↓
Entry created in `entries` table
   ↓
Next input → API /suggestions (GET)
   ↓
Query entries, count frequency
   ↓
If frequency >= 2 → Create/update suggestion
   ↓
Display suggestion dropdown
```

### Word Upload:
```
Upload file → Parse → Create WordTemplate
   ↓
API /api/word/upload
   ↓
wordTemplate saved in `word_templates` table
   ↓
User fills form → Submit
   ↓
API /api/word/submit
   ↓
wordSubmission saved in `word_submissions` table
   ↓
Check if can generate suggestions for next form
```

---

## 📈 Expected Behavior

### First Entry
- ❌ No suggestions (need 2+ same values)
- ✅ Data saved

### Second Entry (Same Value)
- ✅ Suggestions appear
- ✅ Frequency counter: 2
- ✅ Data saved

### Third Entry (Same Value)
- ✅ Same suggestion, frequency: 3
- ✅ Data saved

---

## 🎯 Testing Checklist

- [ ] Upload testform.docx successfully
- [ ] Template created with 3 fields
- [ ] Form opens with correct fields
- [ ] Fill form 1st time → no suggestions
- [ ] Fill form 2nd time with same data → suggestions appear
- [ ] Click suggestion → data filled
- [ ] View history with timestamps
- [ ] Delete template → submissions auto-delete

---

## 🔧 Database Commands

### Check entries count
```bash
cd backend
python -c "
from app.db.session import SessionLocal
from app.db.models import Entry
db = SessionLocal()
entries = db.query(Entry).count()
print(f'Entries: {entries}')
db.close()
"
```

### View entries detail
```bash
python -c "
from app.db.session import SessionLocal
from app.db.models import Entry
db = SessionLocal()
for e in db.query(Entry).all():
    print(f'ID {e.id}: Field {e.field_id} = {e.value}')
db.close()
"
```

### Clean database again
```bash
python clean_data.py
```

---

## 🐛 Troubleshooting

### Suggestions not appearing
- Need to fill with same value 2+ times
- Check browser console (F12) for errors
- Check server logs for API errors

### Upload fails
- Ensure file is .docx (not .doc)
- Ensure file has correct format (Label:)

### Form not saving
- Check network tab (F12) for failed requests
- Check server is running
- Check MySQL connection

---

## 📞 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/suggestions` | GET | Get suggestions for field |
| `/api/suggestions/save` | POST | Save entry |
| `/api/word/upload` | POST | Upload Word file |
| `/api/word/template/{id}` | GET | Get template detail |
| `/api/word/submit` | POST | Submit form data |

---

## 🎨 UI Features

### Word Upload UI
- 📤 Upload area (drag & drop)
- 📋 Template list (name, fields count, submissions)
- 📊 Statistics (total templates, submissions, last update)
- ✏️ Fill form button
- 🗑️ Delete template button
- 📜 History table (template, submission ID, timestamp)

### AutoFill Form UI
- 👤 5 input fields (name, email, phone, city, company)
- 💡 Suggestions dropdown (click to select)
- 📊 Frequency indicator
- 💾 Save button
- 🔄 Reset button

---

## ✨ Key Features

✅ **Automatic Field Extraction** - Parse Word files
✅ **Smart Type Detection** - Text, Number, Date, Email, Phone
✅ **Dynamic Form Rendering** - Create forms from templates
✅ **History Tracking** - All submissions saved with timestamp
✅ **Suggestion System** - Auto-suggest from history (2+ entries)
✅ **Multi-Template Support** - Upload multiple Word files
✅ **Cascade Delete** - Delete template → auto-delete submissions

---

**Status**: ✅ Ready for Testing  
**Database**: 🧹 Clean (No Historical Data)  
**Data**: 📊 Will be created as you use the system
