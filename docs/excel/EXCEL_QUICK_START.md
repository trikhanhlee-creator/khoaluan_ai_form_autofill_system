# 🚀 EXCEL AUTO-FILL - QUICK START GUIDE

## ⚡ 30 Second Startup

### 1. Start Server
```bash
cd backend
python run.py
```

### 2. Open Browser
```
http://localhost:8000/
```

### 3. Done! 🎉

---

## 📊 First Time Usage (5 Minutes)

### Step 1: See the Menu
Visit `http://localhost:8000/` and you'll see 3 options:
- 📊 Excel Upload
- 📝 Word Upload  
- ✏️ Điền Form

### Step 2: Click Excel Upload
Go to the Excel Upload section at `http://localhost:8000/excel`

### Step 3: Upload Sample File
- **Sample file ready:** `backend/uploads/sample_data.xlsx`
- Drag & drop the file OR click "Chọn File Excel"
- System auto-detects file and parses it

### Step 4: See the Form
Form page loads automatically with:
```
Dòng 1 / 5
Ho Ten: [Nguyen Van A]
Email: [nguyenvana@email.com]
So Dien Thoai: [0901234567]
Dia Chi: [123 To Ky, Q.12, TP.HCM]
Nganh Hang: [Cong nghe]
Ghi Chu: [Nhan vien moi]

[Buttons for navigation]
```

### Step 5: Navigate Data
- Click "Dòng Tiếp Theo →" to go to row 2
- Use buttons or keyboard:
  - **Tab** = Next field
  - **Shift+Tab** = Previous field
  - **Enter** = Next row (from last field)

---

## 🎯 Features to Try

### Try These:
1. **Edit a Field** - Type something in Ho Ten field
2. **See Suggestions** - System shows related entries
3. **Use Keyboard** - Press Tab to next field
4. **Navigation** - Click buttons to jump between rows
5. **Progress Bar** - Watch it update as you move rows

---

## 📁 Where to Find Things

### URLs:
```
Menu:         http://localhost:8000/
Excel Upload: http://localhost:8000/excel
Form:         http://localhost:8000/excel-form/sample_data
API Docs:     http://localhost:8000/docs
Health Check: http://localhost:8000/health
```

### Files:
```
Sample Excel:   backend/uploads/sample_data.xlsx
Backend Code:   backend/app/api/routes/excel.py
Frontend:       backend/app/static/menu.html
                backend/app/static/excel-upload.html
                backend/app/static/excel-form.html
```

---

## 💡 Pro Tips

### Keyboard Shortcuts
```
Tab ..................... Next field
Shift+Tab ................ Previous field
Enter (last field) ....... Next row
Arrow Down ............... See suggestions
```

### Why Data Auto-Fills?
The form gets headers from Excel (row 1) and automatically creates fields. Your Excel data appears in the form fields instantly.

### Where Are Suggestions From?
They're saved from what you type previously. Next time you start typing, old entries appear as suggestions!

### Multiple Files?
You can upload multiple Excel files. Each gets its own session ID. The Sessions list shows all active files.

---

## 🆘 Troubleshooting

### Issue: "Server not running"
```bash
# Make sure you started the server
cd backend
python run.py
# Check: http://localhost:8000/health
```

### Issue: "File upload fails"
- ✅ Use .xlsx or .xls files
- ✅ Make sure row 1 has headers
- ✅ File is not corrupted

### Issue: "Form doesn't load"
- ✅ Clear browser cache (Ctrl+Shift+Del)
- ✅ Check browser console (F12)
- ✅ Make sure session ID is correct

### Issue: "No suggestions"
- ✅ Type something new first
- ✅ Suggestions will appear next session
- ✅ Also stored in browser localStorage

---

## 📊 Test Data Included

File: `backend/uploads/sample_data.xlsx`

Contains:
- **5 rows** of sample employee data
- **6 columns**: Ho Ten, Email, So Dien Thoai, Dia Chi, Nganh Hang, Ghi Chu
- **Ready to test** all features

---

## 🎨 What You're Looking For

### Menu Page
- Gradient background
- 3 colored cards with icons
- Instructions at bottom
- ← Quay Lại button

### Upload Page
- Large upload area (drag & drop)
- Recent sessions list
- Upload progress
- File validation

### Form Page
- Auto-generated input fields
- Progress bar at top
- Navigation buttons
- Suggestions dropdown (click input!)
- Row counter (e.g., "Dòng 1 / 5")

---

## 🔗 Next Steps

After testing:

1. **Read Full Guide:**
   ```
   EXCEL_FEATURE_GUIDE.md
   ```

2. **Use Your Own Excel:**
   - Create Excel with your data
   - Headers in row 1
   - Data in rows 2+
   - Upload and test!

3. **Integrate:**
   - Use API endpoints for custom apps
   - Embed form in your website
   - Automate data entry workflows

---

## 📞 Quick Reference

### API Endpoints

**Upload Excel:**
```bash
curl -X POST http://localhost:8000/api/excel/upload \
  -F "file=@your_file.xlsx"
```

**Get Data:**
```bash
curl http://localhost:8000/api/excel/data/{session_id}
```

**Get Row:**
```bash
curl http://localhost:8000/api/excel/row/{session_id}/0
```

**List Sessions:**
```bash
curl http://localhost:8000/api/excel/sessions
```

---

## 🎓 Understanding the Workflow

```
Your Excel File
    ↓
[Upload → Parse Headers & Rows]
    ↓
New Session Created
    ↓
Form Auto-Generated
(fields = headers, data = first row)
    ↓
User Fills/Views Data
    ↓
Navigate Rows
(click or keyboard)
    ↓
Data Saved in Browser
(localStorage)
    ↓
Repeat Until Done
```

---

## ✅ Checklist - First Time

- [ ] Server running: `python run.py`
- [ ] Visit: http://localhost:8000/
- [ ] See menu with 3 options
- [ ] Click "Excel Upload"
- [ ] Upload sample file
- [ ] Form loads with data
- [ ] Can navigate rows
- [ ] Can edit fields
- [ ] See suggestions when typing
- [ ] Click "← Quay Lại" to go back

---

## 🎉 You're Ready!

Everything is set up and working. Start using the Excel Auto-Fill feature now!

**Questions?** See [EXCEL_FEATURE_GUIDE.md](EXCEL_FEATURE_GUIDE.md)

**Need Help?** Check http://localhost:8000/docs for API documentation.

---

**Version:** 1.0.0  
**Last Updated:** March 1, 2026  
**Status:** ✅ Ready to Use
