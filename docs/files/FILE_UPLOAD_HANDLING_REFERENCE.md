# 📤 File Upload Handling & Display Logic - Complete Reference

## 📋 Overview
This document maps all file upload handling, filename prefixing, and display logic across the system.

---

## 🔧 Part 1: FILE UPLOAD WITH PREFIX NAMING

### 1.1 Word File Upload Route
**File:** [backend/app/api/routes/word.py](backend/app/api/routes/word.py#L29)

**Endpoint:** `POST /api/word/upload`

**Prefix Pattern:**
```python
file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{datetime.now().timestamp()}_{file.filename}")
```

**Breakdown:**
- `{user_id}` - User ID (e.g., `1`)
- `_` - Separator
- `{datetime.now().timestamp()}` - Unix timestamp to ensure uniqueness (e.g., `1710916234.5678`)
- `_` - Separator
- `{file.filename}` - Original filename (e.g., `form.docx`)

**Example Result:**
```
uploads/1_1710916234.5678_form.docx
```

**Code Location:** [backend/app/api/routes/word.py](backend/app/api/routes/word.py#L63-L67)
```python
# Lưu file
file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{datetime.now().timestamp()}_{file.filename}")
with open(file_path, "wb") as f:
    content = await file.read()
    f.write(content)
```

---

### 1.2 Form Replacement Upload Route (Intelligent Detection)
**File:** [backend/app/api/routes/form_replacement.py](backend/app/api/routes/form_replacement.py#L41)

**Endpoint:** `POST /api/form-replacement/upload-with-intelligent-detection`

**Same Prefix Pattern:**
```python
file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{datetime.now().timestamp()}_{file.filename}")
```

**Code Location:** [backend/app/api/routes/form_replacement.py](backend/app/api/routes/form_replacement.py#L61-L66)
```python
# Lưu file
file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{datetime.now().timestamp()}_{file.filename}")
with open(file_path, "wb") as f:
    content = await file.read()
    f.write(content)
```

---

### 1.3 Form Replacement Upload Route (Dot-Lines)
**File:** [backend/app/api/routes/form_replacement.py](backend/app/api/routes/form_replacement.py#L360)

**Endpoint:** `POST /api/form-replacement/upload-with-dotlines`

**Same Prefix Pattern:**
```python
file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{datetime.now().timestamp()}_{file.filename}")
```

**Code Location:** [backend/app/api/routes/form_replacement.py](backend/app/api/routes/form_replacement.py#L375-L380)

---

## 💾 Part 2: DATABASE STORAGE - FILENAME FIELDS

### 2.1 WordTemplate Model
**File:** [backend/app/db/models.py](backend/app/db/models.py#L94)

**Two filename columns:**
```python
class WordTemplate(Base):
    __tablename__ = "word_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    template_name = Column(String(255), nullable=False)      # Display name (cleaned filename)
    file_path = Column(String(500), nullable=False)          # Full path with prefix (e.g., "uploads/1_123456.789_form.docx")
    original_filename = Column(String(255), nullable=False)  # Original filename (e.g., "form.docx")
    fields_json = Column(Text)                                # JSON string of fields
```

**Storage mapping:**
| Column | Content | Example |
|--------|---------|---------|
| `template_name` | Cleaned from original filename | `form` |
| `file_path` | Full path with prefix | `uploads/1_1710916234.5678_form.docx` |
| `original_filename` | User's uploaded filename | `form.docx` |

---

## 🎨 Part 3: FILENAME DISPLAY LOGIC

### 3.1 Template List Display (GET /templates)
**File:** [backend/app/api/routes/word.py](backend/app/api/routes/word.py#L112)

**Endpoint:** `GET /api/word/templates?user_id={user_id}`

**Response Fields:**
```python
@router.get("/templates")
async def get_user_templates(user_id: int = Query(1), db: Session = Depends(get_db)):
    templates = db.query(WordTemplate).filter(WordTemplate.user_id == user_id).all()
    
    return {
        "templates": [
            {
                "id": t.id,
                "name": t.template_name,              # Display name ★ USED FOR DISPLAY
                "filename": t.original_filename,     # Original filename ★ USED FOR INFO
                "fields_count": len(json.loads(t.fields_json)) if t.fields_json else 0,
                "created_at": t.created_at.isoformat(),
                "submissions_count": len(t.submissions)
            }
            for t in templates
        ]
    }
```

**Display mapping:**
- **UI shows:** `t.template_name` (cleaned, user-friendly name)
- **Metadata shows:** `t.original_filename` (the actual file uploaded)

---

### 3.2 Template Detail Display (GET /template/{id})
**File:** [backend/app/api/routes/word.py](backend/app/api/routes/word.py#L148)

**Endpoint:** `GET /api/word/template/{template_id}?user_id={user_id}`

**Response includes:**
```python
return {
    "id": template.id,
    "name": template.template_name,           # ★ Display name
    "filename": template.original_filename,   # ★ Original filename
    "fields": enriched_fields,
    "form_id": form_id,
    "created_at": template.created_at.isoformat(),
    "submissions_count": submissions_count
}
```

---

### 3.3 Frontend Display in word-upload.html
**File:** [backend/app/static/word-upload.html](backend/app/static/word-upload.html#L1120)

**Template list rendering:**
```javascript
templatesList.innerHTML = templates.map(t => `
    <div class="template-item">
        <div class="template-info">
            <div class="template-name">${escapeHtml(t.name)}</div>     <!-- Displays: template_name -->
            <div class="template-meta">
                ${t.fields_count} trường • ${t.submissions_count} submissions • 
                ${new Date(t.created_at).toLocaleDateString('vi-VN')}
            </div>
        </div>
        <div class="template-actions">
            <button class="btn btn-danger btn-small" onclick="deleteTemplate(${t.id})">
                Xóa
            </button>
        </div>
    </div>
`).join('');
```

**Template detail display:**
```javascript
async function openForm(templateId) {
    const response = await fetch(`${API_BASE}/api/word/template/${templateId}`);
    const data = await response.json();
    
    currentTemplate = data;
    
    // Display template name as form title
    document.getElementById('formTitle').textContent = data.name;  // ★ Shows template_name
    document.getElementById('formDescription').textContent = `${data.fields.length} trường`;
}
```

---

## 🔄 Part 4: FILENAME TRANSFORMATION FLOW

### Upload → Database → Display Flow

```
┌─────────────────────────────────────────────────────────────┐
│ USER UPLOADS FILE: "My Form.docx"                           │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: SAVE WITH PREFIX                                    │
│ Filename: 1_1710916234.5678_My Form.docx                    │
│ Full Path: uploads/1_1710916234.5678_My Form.docx           │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: EXTRACT AND CLEAN FOR DISPLAY                       │
│ template_name = "My Form" (from original_filename without   │
│                 extension, using os.path.splitext)          │
│ file_path = "uploads/1_1710916234.5678_My Form.docx"       │
│ original_filename = "My Form.docx"                          │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: SAVE TO DATABASE (word_templates table)             │
│ INSERT INTO word_templates (template_name, file_path,       │
│         original_filename) VALUES (...)                     │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: DISPLAY TO USERS                                    │
│ List View: Shows template_name ("My Form")                  │
│ Detail View: Shows name="My Form", filename="My Form.docx"  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Part 5: CODE LOCATIONS SUMMARY

### Upload Route - File Saving
| Route | File | Method | Pattern |
|-------|------|--------|---------|
| `/api/word/upload` | [backend/app/api/routes/word.py](backend/app/api/routes/word.py#L63) | POST | `{user_id}_{timestamp}_{filename}` |
| `/api/form-replacement/upload-with-intelligent-detection` | [backend/app/api/routes/form_replacement.py](backend/app/api/routes/form_replacement.py#L61) | POST | `{user_id}_{timestamp}_{filename}` |
| `/api/form-replacement/upload-with-dotlines` | [backend/app/api/routes/form_replacement.py](backend/app/api/routes/form_replacement.py#L375) | POST | `{user_id}_{timestamp}_{filename}` |

### Retrieval & Display Routes
| Route | File | Returns | Display Field |
|-------|------|---------|----------------|
| `GET /api/word/templates` | [backend/app/api/routes/word.py](backend/app/api/routes/word.py#L112) | List of templates | `name` (template_name) |
| `GET /api/word/template/{id}` | [backend/app/api/routes/word.py](backend/app/api/routes/word.py#L148) | Template detail | `name` (template_name) |

### Frontend Display
| File | Component | Displays |
|------|-----------|----------|
| [backend/app/static/word-upload.html](backend/app/static/word-upload.html#L1120) | Template list | `t.name` from API response |
| [backend/app/static/word-upload.html](backend/app/static/word-upload.html#L1125) | Form title | `data.name` from template detail |

---

## 🎯 Part 6: KEY INSIGHTS

### Naming Strategy:
1. **File storage prefix** - Includes `user_id` and `timestamp` for:
   - ✅ Preventing filename collisions
   - ✅ Organizing files by user
   - ✅ Creating unique identifiers

2. **Database columns** - Three separate fields for:
   - `template_name` - User-friendly display name (cleaned)
   - `file_path` - Full path with prefix (for file access)
   - `original_filename` - Original filename (for reference)

3. **Display logic** - Always uses:
   - `template_name` in lists and headers (clean, short)
   - `original_filename` in metadata (reference)
   - `file_path` internally (for file operations)

### Security Implications:
- ✅ User ID in prefix allows multi-user file isolation
- ✅ Timestamp ensures no overwriting
- ✅ Original filename preserved for user reference
- ⚠️ File paths exposed in API responses (consider if needed)

---

## 📝 Template Name Extraction Code

**From [backend/app/api/routes/form_replacement.py](backend/app/api/routes/form_replacement.py#L104):**
```python
template = WordTemplate(
    user_id=user_id,
    template_name=os.path.splitext(file.filename)[0],    # Removes extension
    file_path=file_path,                                  # Full path with prefix
    original_filename=file.filename,                      # Original filename
    fields_json=json.dumps(fields)
)
```

**From [backend/app/api/routes/word.py](backend/app/api/routes/word.py#L81):**
```python
template = WordTemplate(
    user_id=user_id,
    template_name=metadata.get("title", file.filename),  # Uses document title or filename
    file_path=file_path,                                  # Full path with prefix
    original_filename=file.filename,                      # Original filename
    fields_json=json.dumps([f.to_dict() for f in fields])
)
```

---

## 🎓 Usage Examples

### Example 1: Upload Flow
```
1. User uploads: "Student_List.xlsx"
2. Server creates prefix: "2_1710920000.123_Student_List.xlsx"
3. Saves to: "uploads/2_1710920000.123_Student_List.xlsx"
4. Database stores:
   - template_name: "Student_List"
   - file_path: "uploads/2_1710920000.123_Student_List.xlsx"
   - original_filename: "Student_List.xlsx"
5. Frontend displays: "Student_List"
```

### Example 2: Multiple Users
```
User 1 uploads "form.docx":
→ uploads/1_1710920000.111_form.docx

User 2 uploads "form.docx":
→ uploads/2_1710920000.222_form.docx

User 3 uploads "form.docx":
→ uploads/3_1710920001.333_form.docx

✅ No conflicts, user_id + timestamp = unique!
```

---

## 🔍 Supported File Formats

From [backend/app/api/routes/word.py](backend/app/api/routes/word.py#L120):
- `.docx` - Word Document
- `.pdf` - PDF File
- `.xlsx` - Excel Spreadsheet (2007+)
- `.xls` - Excel Spreadsheet (97-2003)
- `.csv` - Comma-Separated Values
- `.txt` - Plain Text File

All follow the same prefix naming pattern!

