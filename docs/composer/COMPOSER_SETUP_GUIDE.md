# 🎯 AI Document Composer - Hướng Dẫn Cài Đặt & Sử Dụng

## 📋 Tổng Quan

Hệ thống **AI Document Composer** đã được cấu hình để thay thế hoàn toàn chức năng tự động điền form cũ. Đây là một trình soạn thảo tài liệu hiện đại với gợi ý AI thông minh, giống Word nhưng mạnh mẽ hơn.

## 🚀 Cài Đặt Nhanh

### 1. Cài Đặt Dependencies

```bash
# Cải nhật dependencies
pip install -r requirements.txt

# Các package AI được cấu hình tự động:
# - openai>=1.0.0 (cho OpenAI API)
# - google-generativeai>=0.3.0 (cho Gemini API)
```

### 2. Cấu Hình AI API

Copy file `.env.example` thành `.env` và cập nhật:

```bash
# Chọn một trong hai AI provider
AI_PROVIDER=openai  # hoặc "gemini"

# OpenAI - Lấy key từ: https://platform.openai.com/api-keys
AI_API_KEY=sk-xxxxxxxxxxxxxxxx

# HOẶC Gemini - Lấy key từ: https://makersuite.google.com/app/apikey
AI_API_KEY=google-api-key-xxxxxxxx
```

### 3. Cấu Hình Database

```bash
# Trong .env, cấu hình database (nếu chưa có)
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/autofill_db
```

### 4. Chạy Server

```bash
cd backend
python run.py
```

Server sẽ chạy ở: **http://127.0.0.1:8000**

## 📖 Hướng Dẫn Sử Dụng

### Truy Cập Ứng Dụng

1. Mở trình duyệt: http://127.0.0.1:8000
2. Bạn sẽ thấy menu chính với **"AI Document Composer"** là tính năng chính
3. Nhấp vào để mở trình soạn thảo

### Các Tính Năng

#### 💻 Soạn Thảo Tài Liệu
- **Rich Text Editor**: Định dạng văn bản (Bold, Italic, Underline)
- **Danh sách**: Bullet list, numbered list
- **Lưu tài liệu**: Tự động hoặc thủ công
- **Quản lý tài liệu**: Xem lịch sử tài liệu gần đây

#### 🤖 Gợi Ý AI
- **Auto-complete**: Dự đoán từ/cụm từ tiếp theo
- **Smart Suggestions**: 3 gợi ý tốt nhất được xếp hạng
- **Flexible**: Chấp nhận hoặc từ chối gợi ý
- **History**: Theo dõi điều gợi ý đã được chấp nhận

#### 📊 Quản Lý Tài Liệu
- **Tạo** tài liệu mới
- **Lưu** tài liệu
- **Xuất** tài liệu as HTML
- **Xóa** tài liệu cũ

#### ⚙️ Cài Đặt
- Bật/tắt **Tự động lưu**
- Bật/tắt **Gợi ý AI**
- Điều chỉnh **Số lượng gợi ý**

## 🔌 API Endpoints

### Document Management

```bash
# Tạo tài liệu mới
POST /api/composer/documents
{
    "title": "Tài liệu mới",
    "content": "<p>Nội dung...</p>",
    "description": "Mô tả tài liệu"
}

# Danh sách tài liệu
GET /api/composer/documents?limit=20&offset=0

# Lấy tài liệu theo ID
GET /api/composer/documents/{document_id}

# Cập nhật tài liệu
PUT /api/composer/documents/{document_id}
{
    "title": "Tiêu đề mới",
    "content": "<p>Nội dung mới</p>"
}

# Xóa tài liệu
DELETE /api/composer/documents/{document_id}
```

### AI Suggestions

```bash
# Lấy gợi ý từ AI
POST /api/composer/suggestions
{
    "context": "Văn bản hiện tại...",
    "max_suggestions": 3,
    "suggestion_length": 10
}

# Response:
{
    "success": true,
    "data": [
        {
            "text": "gợi ý 1",
            "confidence": 0.9
        },
        {
            "text": "gợi ý 2",
            "confidence": 0.8
        }
    ]
}
```

### Composition History

```bash
# Lưu hành động soạn thảo
POST /api/composer/save-action
{
    "document_id": 1,
    "action_type": "suggestion",  # hoặc "edit", "acceptance"
    "suggested_text": "Text được gợi ý",
    "context": "Ngữ cảnh cho gợi ý",
    "accepted": 1
}
```

## 📧 Các Biến Môi Trường (Environment Variables)

```env
# Database
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/autofill_db

# AI Configuration
AI_PROVIDER=openai              # hoặc "gemini"
AI_API_KEY=sk-xxxxx            # OpenAI key
COMPOSER_MAX_SUGGESTIONS=3      # Số lượng gợi ý
COMPOSER_SUGGESTION_LENGTH=10   # Độ dài trung bình gợi ý (từ)

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

## 🔑 Lấy AI API Keys

### OpenAI
1. Đi tới https://platform.openai.com/api-keys
2. Đăng nhập với tài khoản OpenAI
3. Nhấp "Create new secret key"
4. Copy key và dán vào `.env` file

### Google Gemini
1. Đi tới https://makersuite.google.com/app/apikey
2. Nhấp "Create API Key"
3. Copy key và dán vào `.env` file

## 🐛 Troubleshooting

### Lỗi: "AI client not initialized"
- Kiểm tra `AI_API_KEY` trong `.env` file
- Kiểm tra `AI_PROVIDER` được set đúng ("openai" hoặc "gemini")
- Restart server

### Lỗi: "Database connection failed"
- Kiểm tra MySQL server đang chạy
- Kiểm tra `DATABASE_URL` trong `.env` file
- Kiểm tra credentials database

### Không nhận được gợi ý từ AI
- Kiểm tra AI API key có hợp lệ không
- Kiểm tra quota/limit của API
- Viết ít nhất 10 ký tự để trigger suggestions
- Bật/tắt "Gợi ý AI" trong cài đặt

### Lỗi: "Module not found"
```bash
# Cài đặt lại dependencies
pip install --upgrade -r requirements.txt

# Hoặc cài riêng AI packages
pip install openai google-generativeai
```

## 📊 Cấu Trúc Cơ Sở Dữ Liệu

### Document
- `id`: Primary key
- `user_id`: Foreign key USER
- `title`: Tiêu đề tài liệu
- `content`: Nội dung (HTML/plain text)
- `description`: Mô tả
- `created_at`, `updated_at`: Timestamps

### CompositionHistory
- `id`: Primary key
- `document_id`: Foreign key Document
- `user_id`: Foreign key User
- `action_type`: 'suggestion', 'edit', 'acceptance'
- `suggested_text`: Text được gợi ý
- `original_text`: Text gốc
- `modified_text`: Text sau khi edit
- `accepted`: 1 (accept) hoặc 0 (reject)
- `created_at`: Timestamp

## 🎨 Customization

### Thay Đổi Giao Diện

File UI: `/backend/app/static/composer.html`

```html
<!-- Thay đổi màu chính -->
<style>
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        /* Thay đổi màu ở đây */
    }
</style>
```

### Thay Đổi Prompt API

File: `/backend/app/services/ai_composer_service.py`

```python
def _get_openai_suggestions(self, context, max_suggestions, suggestion_length):
    prompt = f"""Bạn là một trợ lý viết văn xuất sắc. 
    # Thay đổi prompt ở đây để điều chỉnh gợi ý AI
    """
```

## 📝 Tính Năng Sắp Tới

- [ ] Export as PDF/Word (.docx)
- [ ] Collaboration real-time
- [ ] Voice typing
- [ ] Multiple language support
- [ ] Document templates
- [ ] Advanced grammar checking
- [ ] Citation management

## 🤝 Support

Nếu bạn gặp vấn đề hoặc có câu hỏi, vui lòng kiểm tra:
1. Console browser (F12) cho client-side errors
2. Terminal logs cho server-side errors
3. `.env` file cấu hình

---

**Version**: 1.0.0  
**Last Updated**: 2026-03-01  
**Powered by**: FastAPI + OpenAI/Gemini
