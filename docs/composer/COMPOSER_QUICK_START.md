# 🎯 QUICK START - AI Document Composer

## ⚡ Khởi Động Nhanh (5 Phút)

### 1️⃣ Cài Đặt Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2️⃣ Cấu Hình AI API
```bash
# Copy file .env
cp .env.example .env

# Cập nhật .env với một trong hai lựa chọn:
# ✅ OpenAI API (khuyến nghị)
AI_PROVIDER=openai
AI_API_KEY=sk-xxxxxxxxxxxxx

# HOẶC Google Gemini
AI_PROVIDER=gemini
AI_API_KEY=google-api-key-xxx
```

### 3️⃣ Chạy Server
```bash
python run.py
```

### 4️⃣ Mở Ứng Dụng
```
http://127.0.0.1:8000
```

---

## 🎨 Giao Diện

```
┌─────────────────────────────────────────────────────────────┐
│   📝 AI Document Composer - Soạn Thảo Tài Liệu              │
│   💾 Lưu  ⬇️ Xuất  ⚙️ Cài đặt                              │
├─────────┬───────────────────────────┬──────────────────────┤
│ 📄 Tài  │  Toolbar:                 │ 💡 Gợi Ý AI        │
│ Liệu    │  [B] [I] [U] [─] [1.]     │                    │
│ Gần     │  Font: [─] Size: [─]      │ Viết thêm để      │
│ Đây     │                           │ nhận gợi ý...     │
│         ├───────────────────────────┤                    │
│ ⊕ Mới   │                           │ ┌────────┐         │
│         │     Editor Area:          │ │Gợi ý 1 │ ✓ ✗    │
│ Doc 1   │     Viết nội dung         │ ├────────┤         │
│ Doc 2   │     tài liệu tại đây      │ │Gợi ý 2 │ ✓ ✗    │
│ Doc 3   │                           │ ├────────┤         │
│         │                           │ │Gợi ý 3 │ ✓ ✗    │
├─────────┼───────────────────────────┼──────────────────────┤
│ ✍️ Từ: 0  📄 Ký tự: 0   Đã lưu: 3:45 PM              │
└─────────┴───────────────────────────┴──────────────────────┘
```

---

## 🚀 Các Bước Sử Dụng

### 1. Tạo Tài Liệu Mới
- Click button **"⊕ Tài Liệu Mới"** bên trái
- Nhập tiêu đề & mô tả
- Click **"Tạo Mới"**

### 2. Soạn Thảo
- Gõ nội dung vào editor ở giữa
- Tự động nhận gợi ý sau 1 giây

### 3. Nhận Gợi Ý AI
- Panel phải sẽ hiển thị **3 gợi ý**
- Xem confidence score (%)
- Click **✓** để chấp nhận
- Click **✗** để từ chối

### 4. Định Dạng
- **[B]** Bold (Đậm)
- **[I]** Italic (Nghiêng)
- **[U]** Underline (Gạch chân)
- **Font** chọn kiểu chữ
- **Size** chọn kích thước

### 5. Lưu & Xuất
- **💾 Lưu** - Lưu ngay
- **⬇️ Xuất** - Download as HTML
- Tự động lưu trong 5 giây (mặc định)

---

## 📝 Ví Dụ Sử Dụng

### Tình Huống 1: Viết Báo Cáo
```
Nhập: "Báo cáo quản lý dự án."
AI gợi ý: "Dự án đã được triển khai thành công"

Nhập: "Dự án đã được triển khai thành công trên"
AI gợi ý: "toàn bộ các bộ phận"
```

### Tình Huống 2: Viết Email
```
Nhập: "Kính gửi,"
AI gợi ý: "Tôi rất vinh dự được gửi"

Nhập: "Tôi rất vinh dự được gửi"
AI gợi ý: "email này đến quý vị"
```

---

## 🔧 Cấu Hình

### Cài Đặt Ứng Dụng (⚙️)
- **☑ Tự động lưu** - Lưu tự động mỗi 5 giây
- **☑ Gợi ý AI** - Bật/tắt gợi ý
- **Số lượng gợi ý** - 3, 5, hoặc 7 gợi ý

### Thay Đổi AI Provider
```bash
# Trong .env, thay đổi:
AI_PROVIDER=openai     # ← Thay đổi đây
AI_API_KEY=sk-xxx      # ← Hoặc key mới

# Restart server
```

---

## 🆘 Khắc Phục Sự Cố

### ❌ Không nhận gợi ý
- [ ] Check API key trong `.env`
- [ ] Check `AI_PROVIDER` setting
- [ ] Gõ ít nhất 10 ký tự
- [ ] Restart server

### ❌ Lỗi kết nối database
- [ ] MySQL server đang chạy?
- [ ] Check `DATABASE_URL` trong `.env`
- [ ] Check username/password

### ❌ Module not found
```bash
pip install --upgrade openai google-generativeai
```

### ❌ Port 8000 đã được sử dụng
```bash
# Chạy ở port khác:
# Sửa backend/run.py line 36: port=8001
```

---

## 📊 API Reference (cho developers)

### Create Document
```bash
curl -X POST http://127.0.0.1:8000/api/composer/documents \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Document",
    "content": "<p>Content</p>"
  }'
```

### Get Suggestions
```bash
curl -X POST http://127.0.0.1:8000/api/composer/suggestions \
  -H "Content-Type: application/json" \
  -d '{
    "context": "Văn bản hiện tại...",
    "max_suggestions": 3
  }'
```

### List Documents
```bash
curl http://127.0.0.1:8000/api/composer/documents
```

---

## 💡 Mẹo & Thủ Thuật

1. **Copy-paste giữ định dạng** - Ctrl+V (plain text)
2. **Undo/Redo** - Ctrl+Z / Ctrl+Shift+Z
3. **Lưu nhanh** - Ctrl+S
4. **Chọn tất cả** - Ctrl+A
5. **In tài liệu** - Ctrl+P

---

## 📚 Tài Liệu Đầy Đủ

Xem file: `COMPOSER_SETUP_GUIDE.md` để có hướng dẫn chi tiết

---

## ✨ Tính Năng Sắp Tới

- 📄 Export as PDF/Word
- 🤝 Cộng tác thời gian thực
- 🎤 Voice typing
- 🌍 Hỗ trợ nhiều ngôn ngữ
- 📋 Templates
- ✍️ Grammar checking

---

**Version**: 1.0.0  
**Ngày**: 2026-03-01  
**Powered by**: FastAPI + OpenAI/Gemini

---

👨‍💻 Hãy bắt đầu viết ngay! Vui lòng báo cáo bug hoặc đề xuất tính năng.
