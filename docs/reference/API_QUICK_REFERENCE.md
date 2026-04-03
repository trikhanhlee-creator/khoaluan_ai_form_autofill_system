# 🎯 API Quick Reference - Form Document Layout Rendering

## 📌 NEW Endpoints

### 1️⃣ Upload Form with Intelligent Detection
```
POST /api/form-replacement/upload-with-intelligent-detection
```

**CURL:**
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
  "template_name": "form",
  "fields_count": 5,
  "sections_count": 2,
  "fields": [...]
}
```

---

### 2️⃣ Render as Document Layout ⭐ NEW
```
GET /api/form-replacement/template/{template_id}/render-form-document
```

**CURL:**
```bash
curl "http://localhost:8000/api/form-replacement/template/123/render-form-document"
```

**JavaScript:**
```javascript
fetch('/api/form-replacement/template/123/render-form-document')
  .then(r => r.json())
  .then(d => {
    document.getElementById('form').innerHTML = d.html_form;
  });
```

**Response:**
```json
{
  "status": "success",
  "template_id": 123,
  "render_type": "document",
  "html_form": "<div class='form-document-style'>...</div>"
}
```

**What You Get:**
- ✅ Centered, bold titles (non-editable)
- ✅ Labeled input boxes with borders
- ✅ Section grouping preserved
- ✅ Professional document appearance
- ✅ 5-10KB HTML size
- ✅ Ready for web display

---

### 3️⃣ Render as Complete Page ⭐ NEW
```
GET /api/form-replacement/template/{template_id}/render-form-page
```

**CURL:**
```bash
curl "http://localhost:8000/api/form-replacement/template/123/render-form-page"
```

**JavaScript:**
```javascript
fetch('/api/form-replacement/template/123/render-form-page')
  .then(r => r.json())
  .then(d => {
    // Option 1: Open in new window
    window.open('data:text/html,' + encodeURIComponent(d.html_page));
    
    // Option 2: Display in iframe
    document.querySelector('iframe').srcdoc = d.html_page;
  });
```

**Response:**
```json
{
  "status": "success",
  "template_id": 123,
  "render_type": "page",
  "html_page": "<!DOCTYPE html><html>...</html>"
}
```

**What You Get:**
- ✅ Complete HTML page (<!DOCTYPE...>)
- ✅ Professional CSS styling included
- ✅ JavaScript form handling included
- ✅ Submit and Reset buttons
- ✅ Ready to open in browser
- ✅ 10-15KB HTML size
- ✅ Print-friendly

---

## 🎨 HTML Output Examples

### Document Layout Output
```html
<div class="form-document-style">
  <div style="text-align: center; font-weight: bold; font-size: 22px; text-transform: uppercase; margin-bottom: 20px;">
    CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
  </div>
  
  <div style="text-align: center; font-style: italic; margin-bottom: 20px;">
    Độc lập - Tự do - Hạnh phúc
  </div>
  
  <div style="text-align: center; font-weight: bold; font-size: 20px; margin-bottom: 30px;">
    ĐƠN XIN VIỆC
  </div>
  
  <div style="margin-bottom: 15px;">
    <span style="font-weight: 500;">Tôi tên là:</span>
    <input type="text" 
           style="border: 1.5px solid #000; padding: 8px 10px; margin-left: 8px; width: 200px;"
           data-field-label="Tôi tên là"
           name="toi_ten_la" />
  </div>
  
  <div style="margin-bottom: 15px;">
    <span style="font-weight: 500;">Sinh ngày:</span>
    <input type="date" 
           style="border: 1.5px solid #000; padding: 8px 10px; margin-left: 8px;"
           data-field-label="Sinh ngày"
           name="sinh_ngay" />
  </div>
  
  <!-- More fields... -->
</div>
```

### Complete Page Output
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Form Document</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    .form-container { max-width: 800px; margin: 0 auto; }
    .form-document-style { ... }
    button { padding: 10px 20px; margin: 10px 5px; cursor: pointer; }
  </style>
</head>
<body>
  <div class="form-container">
    <div class="form-document-style">
      <!-- Form content here -->
    </div>
    <div style="text-align: center; margin-top: 30px;">
      <button type="submit" onclick="submitForm()">Gửi</button>
      <button type="reset" onclick="resetForm()">Xóa</button>
    </div>
  </div>
  
  <script>
    function submitForm() { /* ... */ }
    function resetForm() { /* ... */ }
  </script>
</body>
</html>
```

---

## 📊 Response Body Breakdown

### Common Response Fields
```json
{
  "status": "success|error",        // Operation status
  "template_id": 123,               // Form template ID
  "template_name": "form_name",     // Document name
  "render_type": "document|page",   // Rendering mode
  "fields_count": 5,                // Number of fields detected
  "sections_count": 2,              // Number of sections detected
  "fields": [                        // Field metadata
    {
      "order": 0,
      "name": "toi_ten_la",
      "label": "Tôi tên là",
      "field_type": "text",
      "section_index": 1,
      "required": true
    }
  ],
  "html_form": "...",              // Document layout HTML (render-form-document)
  "html_page": "<!DOCTYPE...",     // Complete page HTML (render-form-page)
  "message": "Form render thành công"
}
```

---

## 🔍 Field Types Auto-Detection

The system automatically detects field types from field labels:

| Label Contains | Field Type | HTML Input |
|---|---|---|
| ngày, sinh, năm sinh | date | `<input type="date">` |
| điện thoại, số điện thoại, liên hệ | phone | `<input type="tel">` |
| email, thư điện tử | email | `<input type="email">` |
| số, năm, tuổi | number | `<input type="number">` |
| ghi chú, mô tả, kinh nghiệm | textarea | `<textarea>` |
| (default) | text | `<input type="text">` |

---

## 💻 Frontend Integration Code

### 1. Display Form
```javascript
async function loadForm(templateId) {
  const response = await fetch(
    `/api/form-replacement/template/${templateId}/render-form-document`
  );
  const data = await response.json();
  
  if (data.status === 'success') {
    document.getElementById('form-container').innerHTML = data.html_form;
  }
}

// Usage
loadForm(123);
```

### 2. Collect Form Data
```javascript
function getFormData() {
  const data = {};
  const inputs = document.querySelectorAll('[data-field-label]');
  
  inputs.forEach(input => {
    const fieldName = input.getAttribute('name') || input.name;
    data[fieldName] = input.value;
  });
  
  return data;
}
```

### 3. Submit Form
```javascript
async function submitForm(templateId) {
  const formData = getFormData();
  
  try {
    const response = await fetch('/api/form-replacement/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        template_id: templateId,
        data: formData
      })
    });
    
    const result = await response.json();
    console.log('✅ Form submitted:', result);
  } catch (error) {
    console.error('❌ Error:', error);
  }
}
```

### 4. Validate Form
```javascript
function validateRequired() {
  const inputs = document.querySelectorAll('[data-field-label]');
  let valid = true;
  
  inputs.forEach(input => {
    if (!input.value.trim()) {
      input.style.border = '2px solid red';
      valid = false;
    } else {
      input.style.border = '';
    }
  });
  
  return valid;
}

// Before submit
if (validateRequired()) {
  submitForm(123);
}
```

---

## 🚀 Complete Workflow Example

```javascript
// Step 1: Upload form
async function uploadAndRender() {
  const fileInput = document.querySelector('input[type="file"]');
  const file = fileInput.files[0];
  
  const formData = new FormData();
  formData.append('file', file);
  formData.append('user_id', 1);
  
  // Step 2: Upload
  const uploadResponse = await fetch(
    '/api/form-replacement/upload-with-intelligent-detection',
    { method: 'POST', body: formData }
  );
  
  const uploadData = await uploadResponse.json();
  const templateId = uploadData.template_id;
  
  // Step 3: Render
  const renderResponse = await fetch(
    `/api/form-replacement/template/${templateId}/render-form-document`
  );
  
  const renderData = await renderResponse.json();
  
  // Step 4: Display
  document.getElementById('form-container').innerHTML = renderData.html_form;
  
  // Step 5: Handle submit
  document.getElementById('submit-btn').onclick = () => {
    if (validateRequired()) {
      submitForm(templateId);
    }
  };
}
```

---

## ✅ Status Codes & Error Handling

```javascript
// Check response status
fetch('/api/form-replacement/template/123/render-form-document')
  .then(r => {
    if (!r.ok) {
      throw new Error(`HTTP ${r.status}`);
    }
    return r.json();
  })
  .then(d => {
    if (d.status === 'success') {
      console.log('✅ Success:', d);
    } else {
      console.error('❌ Error:', d.message);
    }
  })
  .catch(e => {
    console.error('❌ Network error:', e);
  });
```

---

## 📋 Cheat Sheet

| Task | Endpoint | Method |
|------|----------|--------|
| Upload form | `/upload-with-intelligent-detection` | POST |
| Get document layout | `/template/{id}/render-form-document` | GET |
| Get complete page | `/template/{id}/render-form-page` | GET |
| Get form list | `/templates` | GET |
| Get form details | `/template/{id}` | GET |
| Delete form | `/template/{id}` | DELETE |

---

## 🎯 Common Use Cases

### Use Case 1: Website Contact Form
```javascript
// 1. Upload form document
// 2. Get document layout render
// 3. Display on website
// 4. Collect submissions
```

### Use Case 2: Mobile App Form
```javascript
// 1. Upload and store template_id
// 2. On app load, fetch render-form-document
// 3. Display in WebView
// 4. Collect data locally
```

### Use Case 3: PDF Export
```javascript
// 1. Get complete page HTML
// 2. Use library (html2pdf) to convert
// 3. Download as PDF
```

### Use Case 4: Form Management System
```javascript
// 1. Upload multiple forms
// 2. Store template_ids
// 3. Render on demand
// 4. Track submissions
```

---

## 🔗 Related Endpoints

```
Existing Endpoints (also available):
  GET  /api/form-replacement/templates                      - List all forms
  GET  /api/form-replacement/template/{id}                  - Get form details
  GET  /api/form-replacement/template/{id}/render-form-structured
  GET  /api/form-replacement/template/{id}/render-form-inline
  POST /api/form-replacement/submit                         - Submit form data
  DELETE /api/form-replacement/template/{id}                - Delete form
```

---

## 🎓 Quick Start

```bash
# 1. Start the server
cd backend
python run.py

# 2. Upload a form
curl -X POST "http://localhost:8000/api/form-replacement/upload-with-intelligent-detection" \
  -F "file=@job_application.docx" \
  -F "user_id=1"

# 3. Get template_id from response (e.g., 123)

# 4. Render form
curl "http://localhost:8000/api/form-replacement/template/123/render-form-document"

# 5. Copy the html_form value and insert into your website
```

---

**Version:** 1.0 | **Status:** ✅ Production Ready | **Last Updated:** 2024
