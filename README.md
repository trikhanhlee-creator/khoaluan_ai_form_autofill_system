# 🎯 AutoFill AI System - Word Upload & Form Builder

Hệ thống tự động điền dữ liệu với hỗ trợ upload file Word và form thông minh.

## 📋 Mô Tả

Hệ thống backend được xây dựng bằng **Python + FastAPI** và **MySQL**, cung cấp:
- Upload file Word (.docx) và tự động parse thành form
- Gợi ý tự động từ lịch sử nhập liệu
- Lưu và quản lý form templates
- Tracking submission history

## 📁 Cấu Trúc Thư Mục

```
autofill-ai-system/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/routes/         # API endpoints
│   │   │   ├── suggestions.py  # AutoFill suggestions API
│   │   │   └── word.py         # Word upload & form API
│   │   ├── services/
│   │   │   └── word_parser.py  # Word document parser
│   │   ├── db/
│   │   │   ├── models.py       # Database models
│   │   │   └── session.py      # DB connection
│   │   ├── static/             # Static files (form.html)
│   │   └── main.py             # FastAPI app
│   ├── run.py                  # Server launcher
│   └── setup_word_db.py        # Database setup
├── ui/                         # Frontend HTML files
│   ├── word-upload.html        # Word upload & form builder UI
│   └── form.html               # AutoFill suggestions form
├── database/                   # Database files
└── README.md                   # This file
```
│
├── backend/                 # Backend FastAPI
│   ├── app/
│   │   ├── main.py          # Entry point FastAPI
│   │   ├── core/
│   │   │   ├── config.py    # Cấu hình ứng dụng
│   │   │   └── logger.py    # Logger
│   │   │
│   │   ├── db/
│   │   │   ├── session.py   # Database session
│   │   │   ├── models.py    # SQLAlchemy models
│   │   │   └── repositories/
│   │   │       └── entry_repo.py  # Repository pattern
│   │   │
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── suggestions.py # API routes
│   │   │
│   │   ├── services/
│   │   │   └── suggestion_service.py # Business logic
│   │   │
│   │   ├── ai/
│   │   │   └── rule_engine.py # AI logic
│   │   │
│   │   └── schemas/
│   │       └── suggestion.py # Pydantic schemas
│   │
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
│
├── database/
│   └── schema.sql           # SQL schema
│
└── README.md
```

## 🚀 Cách Chạy

### 1. Chuẩn Bị Database

Tạo database MySQL:
```sql
CREATE DATABASE autofill_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Chạy schema:
```sql
mysql -u root -p autofill_db < database/schema.sql
```

### 2. Cài Đặt Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Cấu Hình Environment

Sửa file `.env`:
```
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/autofill_db
```

### 4. Chạy Server

```bash
# Cách 1: Chạy từ backend folder
cd backend
python -m uvicorn app.main:app --reload

# Cách 2: Chạy từ root
cd backend/app
python main.py
```

Server sẽ chạy tại `http://localhost:8000`

### 5. Kiểm Tra API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 Database Schema

### Bảng Users
```sql
- id (PK)
- email (UNIQUE)
- username
- created_at, updated_at
```

### Bảng Forms
```sql
- id (PK)
- user_id (FK)
- form_name
- description
- created_at, updated_at
```

### Bảng Fields
```sql
- id (PK)
- form_id (FK)
- field_name
- field_type
- display_order
- created_at
```

### Bảng Entries (Lịch sử nhập)
```sql
- id (PK)
- user_id (FK)
- field_id (FK)
- form_id (FK)
- value
- created_at (INDEX)
```

### Bảng Suggestions
```sql
- id (PK)
- user_id (FK)
- field_id (FK)
- suggested_value
- frequency
- ranking
- created_at, updated_at
```

## 🔌 API Endpoints

### 1. GET /api/suggestions
Lấy top gợi ý cho một field

**Parameters:**
- `user_id` (int, required): ID của user
- `field_id` (int, required): ID của field
- `top_k` (int, optional): Số gợi ý top (mặc định 3, max 10)

**Response:**
```json
{
  "user_id": 1,
  "field_id": 1,
  "suggestions": [
    {
      "value": "Hà Nội",
      "frequency": 5,
      "ranking": 1
    },
    {
      "value": "TP Hồ Chí Minh",
      "frequency": 3,
      "ranking": 2
    },
    {
      "value": "Đà Nẵng",
      "frequency": 2,
      "ranking": 3
    }
  ],
  "total_count": 3
}
```

### 2. GET /api/suggestions/history
Lấy gợi ý dựa vào lịch sử trong khoảng thời gian

**Parameters:**
- `user_id` (int, required)
- `field_id` (int, required)
- `days` (int, optional): Số ngày quay lại (mặc định 30)
- `top_k` (int, optional): Số gợi ý top (mặc định 3)

### 3. GET /api/suggestions/stats
Lấy thống kê về entries của một field

**Parameters:**
- `user_id` (int, required)
- `field_id` (int, required)

**Response:**
```json
{
  "total_entries": 10,
  "recent_entries_count": 5,
  "unique_values": 3,
  "frequency_distribution": {
    "Hà Nội": 5,
    "TP Hồ Chí Minh": 3,
    "Đà Nẵng": 2
  }
}
```

## 📝 Dữ Liệu Mẫu (Test)

Tạo file `database/seed.sql` để thêm dữ liệu test:

```sql
-- Insert users
INSERT INTO users (email, username) VALUES
('user1@example.com', 'User 1'),
('user2@example.com', 'User 2');

-- Insert forms
INSERT INTO forms (user_id, form_name, description) VALUES
(1, 'Form Thông Tin Cá Nhân', 'Form điền thông tin cá nhân'),
(1, 'Form Địa Chỉ', 'Form điền địa chỉ');

-- Insert fields
INSERT INTO fields (form_id, field_name, field_type, display_order) VALUES
(1, 'Tỉnh/Thành phố', 'text', 1),
(1, 'Quận/Huyện', 'text', 2),
(2, 'Địa chỉ', 'text', 1);

-- Insert entries (lịch sử nhập)
INSERT INTO entries (user_id, field_id, form_id, value) VALUES
(1, 1, 1, 'Hà Nội'),
(1, 1, 1, 'Hà Nội'),
(1, 1, 1, 'Hà Nội'),
(1, 1, 1, 'Hà Nội'),
(1, 1, 1, 'Hà Nội'),
(1, 1, 1, 'TP Hồ Chí Minh'),
(1, 1, 1, 'TP Hồ Chí Minh'),
(1, 1, 1, 'TP Hồ Chí Minh'),
(1, 1, 1, 'Đà Nẵng'),
(1, 1, 1, 'Đà Nẵng');
```

Chạy seed data:
```bash
mysql -u root -p autofill_db < database/seed.sql
```

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.104.1
- **Web Server**: Uvicorn 0.24.0
- **Database**: MySQL + SQLAlchemy 2.0.23
- **Driver**: PyMySQL 1.1.0
- **Validation**: Pydantic 2.5.0
- **Authentication**: Cryptography 41.0.7

## 📌 Các Module Chính

### 1. **Rule Engine** (`app/ai/rule_engine.py`)
- `calculate_frequency()`: Tính tần suất
- `rank_suggestions()`: Xếp hạng gợi ý
- `generate_suggestions()`: Sinh gợi ý từ entries
- `validate_entries()`: Kiểm tra dữ liệu

### 2. **Repository** (`app/db/repositories/entry_repo.py`)
- `get_recent_entries()`: Lấy N entry gần nhất
- `get_entries_by_field()`: Lấy entries trong khoảng thời gian
- `count_field_entries()`: Đếm entries
- `create_entry()`: Tạo entry mới

### 3. **Service** (`app/services/suggestion_service.py`)
- `get_suggestions()`: Lấy gợi ý
- `get_suggestions_with_history()`: Lấy gợi ý từ lịch sử
- `get_field_statistics()`: Lấy thống kê

### 4. **Routes** (`app/api/routes/suggestions.py`)
- `GET /api/suggestions`: API chính
- `GET /api/suggestions/history`: API lịch sử
- `GET /api/suggestions/stats`: API thống kê

## 🧪 Testing

Có thể test API bằng cURL:

```bash
# Test get_suggestions
curl "http://localhost:8000/api/suggestions?user_id=1&field_id=1&top_k=3"

# Test get_suggestions_with_history
curl "http://localhost:8000/api/suggestions/history?user_id=1&field_id=1&days=30&top_k=3"

# Test get_field_stats
curl "http://localhost:8000/api/suggestions/stats?user_id=1&field_id=1"
```

## 📚 Thiết Kế Architecture

### Tầng Presentation (API Routes)
```
GET /api/suggestions
  ↓
Route Handler (suggestions.py)
  ↓ Dependency Injection (get_db)
```

### Tầng Business Logic (Service)
```
SuggestionService.get_suggestions()
  ├─ Validate inputs
  ├─ Call Repository
  ├─ Process with Rule Engine
  └─ Return structured response
```

### Tầng Data Access (Repository)
```
EntryRepository.get_recent_entries()
  ├─ Query database with SQLAlchemy
  ├─ Filter & Sort
  └─ Return entities
```

### Tầng AI (Rule Engine)
```
RuleEngine.generate_suggestions()
  ├─ Calculate frequency
  ├─ Rank by frequency
  └─ Return top-k suggestions
```

## 🔐 Error Handling

Tất cả endpoints có xử lý lỗi:
- **400 Bad Request**: Invalid parameters
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error
- **Logging**: Tất cả lỗi được log vào `logs/app.log`

## 📖 Logging

Log được lưu tại `backend/logs/app.log` với:
- Timestamp
- Log level (DEBUG, INFO, WARNING, ERROR)
- Module name
- Message

## 🎓 Hướng Phát Triển

Có thể mở rộng:
1. Thêm ML models (Recommendation, Clustering)
2. Cache suggestions với Redis
3. Authentication & Authorization
4. Rate limiting
5. GraphQL API
6. Advanced analytics

## 📄 License

MIT

## 👥 Tác Giả

AutoFill AI System - 2026

---

**Lưu ý:**
- Đảm bảo MySQL đang chạy trước khi start server
- Sửa `DATABASE_URL` trong `.env` theo cấu hình của bạn
- Logs được lưu trong folder `backend/logs/`
