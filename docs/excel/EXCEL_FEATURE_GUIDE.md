# 📊 Excel Upload & Auto-Fill Feature Guide

## Tổng Quan Chức Năng Mới

Hệ thống AutoFill AI System đã được nâng cấp với chức năng mạnh mẽ:

1. **📋 Menu Chính** - Điều hướng trung tâm để chọn các chức năng
2. **📊 Excel Upload** - Tải file Excel lên hệ thống
3. **✏️ Dynamic Form** - Form được tạo tự động từ headers trong Excel
4. **🔄 Auto-Fill** - Dữ liệu từ Excel được tự động điền vào form
5. **⌨️ Navigation** - Dễ dàng chuyển đổi giữa các dòng dữ liệu
6. **💾 Suggestions** - Gợi ý thông minh từ dữ liệu lịch sử

---

## 🚀 Hướng Dẫn Sử Dụng

### 1. Truy Cập Menu Chính
```
http://localhost:8000/
```

Trang menu chính hiển thị 3 tùy chọn:
- 📊 **Excel Upload** - Chức năng mới
- 📝 **Word Upload** - Upload file Word
- ✏️ **Điền Form** - Form chuẩn

### 2. Tải File Excel Lên

Truy cập: `http://localhost:8000/excel`

**Yêu cầu File Excel:**
- Định dạng: `.xlsx` hoặc `.xls`
- Dòng 1: Tên các trường (headers)
- Dòng 2+: Dữ liệu cần điền

**Ví dụ:**
```
Ho Ten          | Email                 | So Dien Thoai | Dia Chi
Nguyen Van A    | nguyenvana@email.com | 0901234567    | 123 To Ky
Tran Thi B      | tranthib@email.com   | 0912345678    | 456 Ly Thai To
```

**Cách Tải File:**
- Kéo & thả file vào khu vực upload
- Hoặc bấm nút "Chọn File Excel"

### 3. Điền Form Tự Động

Sau khi tải file thành công, bạn sẽ được chuyển đến trang form điền dữ liệu.

**Giao Diện Form:**
```
┌─────────────────────────────────────┐
│ Dòng 1 / 5                  [Thanh Progress]
├─────────────────────────────────────┤
│ Ho Ten: [Nguyen Van A...]   ↓ Gợi ý │
│ Email:  [nguyenvana@...]             │
│ So Dien Thoai: [0901234567]          │
│ Dia Chi: [123 To Ky...]              │
│ Nganh Hang: [...]                    │
│ Ghi Chu: [...]                       │
├─────────────────────────────────────┤
│ [← Dòng Trước] [Dòng Tiếp Theo →]   │
│ [⏮️ Đầu Tiên]  [⏭️ Cuối Cùng]        │
└─────────────────────────────────────┘
```

### 4. Điều Hướng Giữa Các Dòng

**Cách 1: Sử dụng Nút Điều Khiển**
- **← Dòng Trước** - Quay lại dòng trước
- **Dòng Tiếp Theo →** - Tiến đến dòng kế tiếp
- **⏮️ Đầu Tiên** - Nhảy đến dòng đầu tiên
- **⏭️ Cuối Cùng** - Nhảy đến dòng cuối cùng

**Cách 2: Sử dụng Bàn Phím**
- **Tab** - Chuyển sang trường tiếp theo
- **Shift + Tab** - Quay lại trường trước
- **Enter** (trên trường cuối) - Chuyển dòng tiếp theo

### 5. Gợi Ý Thông Minh

Form sẽ hiển thị gợi ý dựa trên:
- Dữ liệu bạn đã nhập trước đó
- Dữ liệu lịch sử được lưu trữ
- Kiểu nhập từng phần (fuzzy matching)

**Ví dụ:**
```
Khi bạn gõ "ng" vào trường Email:
┌─────────────────────────┐
│ nguyenvana@email.com ← │
│ nguyenvanb@email.com  │
│ nguyenvanc@email.com  │
└─────────────────────────┘
```

---

## 🔧 API Documentation

### Endpoints Chính

#### 1. Upload File Excel
```http
POST /api/excel/upload
Content-Type: multipart/form-data

file: <binary>

Response:
{
  "status": "success",
  "session_id": "sample_data",
  "filename": "sample_data.xlsx",
  "headers": ["Ho Ten", "Email", "So Dien Thoai", ...],
  "total_rows": 5,
  "message": "Tải file thành công! Tìm thấy 5 dòng dữ liệu"
}
```

#### 2. Lấy Dữ Liệu Excel
```http
GET /api/excel/data/{session_id}

Response:
{
  "status": "success",
  "headers": ["Ho Ten", "Email", ...],
  "rows": [...],
  "total_rows": 5,
  "filename": "sample_data.xlsx"
}
```

#### 3. Lấy Dòng Cụ Thể
```http
GET /api/excel/row/{session_id}/{row_index}

Response:
{
  "status": "success",
  "headers": [...],
  "row_index": 0,
  "row_data": {"Ho Ten": "Nguyen Van A", "Email": "nguyenvana@email.com", ...},
  "total_rows": 5,
  "current_row": 1
}
```

#### 4. Danh Sách Sessions Hoạt Động
```http
GET /api/excel/sessions

Response:
{
  "status": "success",
  "sessions": [
    {
      "session_id": "sample_data",
      "filename": "sample_data.xlsx",
      "total_rows": 5
    }
  ],
  "total_sessions": 1
}
```

#### 5. Xóa Session
```http
DELETE /api/excel/session/{session_id}

Response:
{
  "status": "success",
  "message": "Session deleted successfully"
}
```

---

## 📁 Cấu Trúc Tệp

### Backend
```
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── excel.py          ← NEW: Xử lý Excel API
│   │       ├── suggestions.py
│   │       ├── word.py
│   │       └── form_replacement.py
│   ├── static/
│   │   ├── menu.html             ← NEW: Menu chính
│   │   ├── excel-upload.html     ← NEW: Upload Excel
│   │   ├── excel-form.html       ← NEW: Form động
│   │   ├── form.html
│   │   └── word-upload.html
│   └── main.py                   ← UPDATED: Thêm routes
└── run.py
```

### Thay Đổi Chi Tiết

**1. main.py**
- ✅ Import `excel` router
- ✅ Include `excel.router` 
- ✅ Thêm route `/excel` - upload page
- ✅ Thêm route `/excel-form/{session_id}` - form page
- ✅ Cập nhật route `/` - menu chính

**2. excel.py (NEW)**
- ✅ Upload file Excel
- ✅ Parse headers và rows
- ✅ Lưu session data
- ✅ API lấy data theo session
- ✅ API lấy row cụ thể
- ✅ API danh sách sessions
- ✅ API xóa session

**3. HTML Pages**
- ✅ menu.html - Navigation chính
- ✅ excel-upload.html - Upload & manage sessions
- ✅ excel-form.html - Dynamic form với gợi ý

---

## 💡 Tính Năng Nổi Bật

### 1. Form Tạo Động
```javascript
// Tự động tạo input fields từ headers
headers.forEach((header, index) => {
  const input = document.createElement('input');
  input.name = header;
  input.placeholder = `Nhập ${header}...`;
  form.appendChild(input);
});
```

### 2. Auto-Fill Dữ Liệu
```javascript
// Điền dữ liệu từ Excel
data.headers.forEach((header, idx) => {
  const input = document.getElementById(`field-${idx}`);
  input.value = data.row_data[header] || '';
});
```

### 3. Gợi Ý Thông Minh
```javascript
// Lưu & gợi ý từ lịch sử
suggestions[fieldName].unshift(value);
localStorage.setItem(`suggestions_${fieldName}`, 
  JSON.stringify(suggestions[fieldName]));
```

### 4. Thanh Progress
```javascript
// Hiển thị tiến độ
const percentage = (currentRow / totalRows) * 100;
progressBar.style.width = percentage + '%';
```

### 5. Keyboard Shortcuts
- **Tab** - Next field
- **Shift+Tab** - Previous field
- **Enter** - Next row (from last field)
- **Arrow Down** - Focus suggestions

---

## 🧪 Test Chức Năng

### Tệp Test Excel
File mẫu: `backend/uploads/sample_data.xlsx`

**Dữ Liệu:**
```
Ho Ten          Email                   So Dien Thoai  Dia Chi                    Nganh Hang    Ghi Chu
Nguyen Van A    nguyenvana@email.com   0901234567     123 To Ky, Q.12, TP.HCM   Cong nghe     Nhan vien moi
Tran Thi B      tranthib@email.com     0912345678     456 Ly Thai To, Q.10       Xuat khau     Chuyen gia
Le Hoang C      lehoangc@email.com     0923456789     789 Vung Tau, Ba Ria       Ban le        Nguoi quan ly
Pham Huy D      phamhuyd@email.com     0934567890     321 Nguyen Hue, Q.1        Tu van        Tu van truong
Hoang Kim E     hoangkime@email.com    0945678901     654 Dien Bien Phu          Thiet ke      Nha thiet ke
```

### Cách Test
1. Truy cập: `http://localhost:8000/excel`
2. Tải file: `backend/uploads/sample_data.xlsx`
3. Hệ thống sẽ chuyển đến form
4. Kiểm tra:
   - ✅ Dữ liệu của dòng 1 được điền
   - ✅ Có thể chuyển sang dòng 2 bằng nút hoặc Enter
   - ✅ Gợi ý hiển thị khi gõ
   - ✅ Thanh progress cập nhật

---

## 🛠️ Cài Đặt & Chạy

### Yêu Cầu
- Python 3.8+
- openpyxl (đã cài)
- FastAPI (đã cài)
- SQLAlchemy (đã cài)

### Khởi Động Server
```bash
cd backend
python run.py
```

Server sẽ chạy tại: `http://127.0.0.1:8000`

### Truy Cập
- **Menu:** http://localhost:8000/
- **Excel:** http://localhost:8000/excel
- **Health Check:** http://localhost:8000/health
- **API Docs (Swagger):** http://localhost:8000/docs

---

## 🚀 Tiếp Theo (Future Enhancements)

- [ ] Export form data thành CSV/Excel
- [ ] Batch import multiple Excel files
- [ ] Template templates untuk form
- [ ] Advanced validation rules
- [ ] Real-time collaboration
- [ ] Undo/Redo functionality
- [ ] Dark mode UI
- [ ] Mobile app support

---

## 📝 Ghi Chú

- Session data được lưu trong memory (production nên dùng database)
- Suggestions được lưu trong localStorage (client-side)
- Max 10,000 dòng dữ liệu trên một file
- Support file Excel .xlsx và .xls
- Form fields được tạo động dựa trên headers

---

## 🆘 Troubleshooting

### Lỗi: "File Excel không được nhận"
- ✅ Kiểm tra phần mở rộng (.xlsx hoặc .xls)
- ✅ Đảm bảo dòng 1 có headers

### Lỗi: "Không thể tải dữ liệu"
- ✅ Kiểm tra server có chạy không: http://localhost:8000/health
- ✅ Xóa browser cache (Ctrl+Shift+Delete)

### Form không hiển thị
- ✅ Kiểm tra console browser (F12)
- ✅ Đảm bảo session_id chính xác

---

## 📞 Support

Liên hệ hỗ trợ hoặc báo lỗi tại GitHub Issues.

Happy Excel filling! 🎉
