# 📊 Excel Auto-Fill Form - Quick Demo Guide

## How It Works (Visual Walkthrough)

```
STEP 1: Upload Excel File
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌐 http://localhost:8000/excel
  
  📤 Upload File
  ┌─────────────────────┐
  │ [Kéo file vào]      │
  │ hoặc                │
  │ [Chọn File]         │
  └─────────────────────┘
  
  ✅ Success! 5 rows detected


STEP 2: Auto-Redirect to Form
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
After 1.5 seconds → Automatic redirect to:
🌐 http://localhost:8000/excel-data-form/student_data


STEP 3: Form Page Layout
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌────────────────────────────────────────────────────────┐
│              📋 Điền Dữ Liệu Excel                     │
│  Chọn một hàng từ bảng bên dưới để tự động điền       │
└────────────────────────────────────────────────────────┘

┌──────────────────────────┬──────────────────────────────┐
│                          │                              │
│  📊 Dữ Liệu Excel        │   ✏️ Chỉnh Sửa Dữ Liệu      │
│  (5 hàng)                │                              │
│                          │   STT: [1]                   │
│  ┌──────────────────┐    │   Mã Sinh Viên: [223005]     │
│  │  # | STT | Mã   │    │   Họ Tên: [Trần Thiên N]     │
│  ├──────────────────┤    │   Giới Tính: [Nam]           │
│  │ 1 | 1  | 223005 │◄───┼─► (Select Row → Auto Fill)  │
│  │ 2 | 2  | 224703 │    │   Ngày Sinh: [05/07/2004]    │
│  │ 3 | 3  | 222683 │    │   Lớp Học: [DH22TIN07]       │
│  │ 4 | 4  | 223172 │    │                              │
│  │ 5 | 5  | 222055 │    │   [Xóa] [Đặt Lại]            │
│  └──────────────────┘    │   [💾 Lưu Thay Đổi]         │
│                          │                              │
└──────────────────────────┴──────────────────────────────┘


STEP 4: Select Row
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
User clicks on row 2 in the table:

BEFORE:
│ 2 | 2  | 224703 │          Form: [empty]

AFTER (Auto-filled):
│ 2 | 2  | 224703 │◄──────► STT: [2]
                              Mã Sinh Viên: [224703]
                              Họ Tên: [Nguyễn Hoàng Phú]
                              Giới Tính: [Nam]
                              Ngày Sinh: [27/10/2004]
                              Lớp Học: [DH22TIN07]


STEP 5: Edit & Save
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
User modifies the form:

BEFORE: Họ Tên: [Nguyễn Hoàng Phú]
        ↓ (User edits)
AFTER:  Họ Tên: [Nguyễn Hoàng Phú - Sửa Đổi]

Then click: [💾 Lưu Thay Đổi]
Result: ✅ "Dữ liệu đã được lưu!"


STEP 6: Repeat
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Click another row → Form auto-fills again
Continue editing more records...
```

---

## Feature Interaction

### Table Features
```
┌─ Row Number    (Row #)
│   ┌─ Highlighted when selected
│   │  ┌─ Hover effect
│   │  │
√  √  √  Row
    ├─ Click to select + auto-fill form
    ├─ Shows all columns with data
    └─ Color changes when active (light blue)

Sticky Headers:
When scrolling, column headers stay visible at top
```

### Form Features
```
Each field:
┌────────────────────────────┐
│ Label: "Họ Tên"            │
│ ┌──────────────────────────┤
│ │ [Input field]            │  ← Editable
│ └──────────────────────────┤
│ Focus effect: Blue border  │
│ + Subtle shadow            │
└────────────────────────────┘

Buttons:
┌─ [Xóa]  Clear all fields
├─ [Đặt Lại]  Reset + deselect
└─ [💾 Lưu]  Save changes
```

---

## Keyboard Navigation

```
Tab         → Move to next field
Shift+Tab   → Move to previous field
Enter       → Focus next field
Escape      → Deselect row (future)
Ctrl+S      → Save (future enhancement)
```

---

## Error Handling

### If file upload fails:
```
❌ Hiển thị error message
   Suggestion: Kiểm tra file, thử lại
```

### If session expired:
```
❌ "Session not found"
   Solution: Upload file lại
```

### If data API fails:
```
❌ "Không thể tải dữ liệu"
   Solution: Refresh page hoặc upload lại
```

---

## Example Scenarios

### Scenario 1: Edit Multiple Records
```
1. Upload student list (100 students)
2. Click row 1 → Edit name → Save
3. Click row 2 → Edit score → Save
4. Click row 50 → Edit address → Save
...
```

### Scenario 2: Bulk Data Review
```
1. Upload customer data (500 rows)
2. Review each row bằng clicking through
3. Spot errors and fix them
4. Save corrections one by one
```

### Scenario 3: Data Entry
```
1. Upload template (empty rows)
2. Click row 1
3. Fill all empty fields
4. Save
5. Repeat for other rows
```

---

## Performance

```
Upload        < 1 second (small file)
Parse         < 2 seconds (typical Excel)
Form Load     < 500ms
Row Select    Instant
Auto-fill     < 100ms
Save          < 1 second
```

---

## Browser Compatibility

```
✅ Chrome    Latest
✅ Firefox   Latest
✅ Safari    Latest
✅ Edge      Latest
✅ Opera     Latest
⚠️ IE 11     Not recommended
```

---

## Tips & Tricks

```
💡 After upload, form redirects automatically
💡 Click multiple rows to view different records
💡 Use Tab key to move between form fields
💡 Data persists during session (until page refresh)
💡 Form fields accept any text or number input
💡 Empty fields show as blank (no default values)
```

---

**Ready to use! Start uploading Excel files now! 🚀**
