# Phân Tích Cơ Sở Dữ Liệu - Autofill AI System

## 📊 Tóm Tắt

**Bảng hiện có**: 9 bảng
**Bảng nên giữ**: 7 bảng (có sửa đổi)
**Bảng không cần thiết**: 2 bảng
**Bảng nên thêm**: 4 bảng
**TOTAL bảng sau cải tiến**: 11 bảng

---

## ✅ BẢNG CẦN GIỮ (7 bảng)

### 1. **users** ⭐ QUAN TRỌNG
**Trạng thái**: GIỮ + CẦN SỬA

**Lý do**: Cần để quản lý tài khoản, authen, phân quyền
- Đăng ký/đăng nhập
- Quản lý admin
- Sở hữu các form, document, template

**Cấu trúc hiện tại**:
```sql
id, email, username, password_hash, is_admin, is_active, 
last_login, created_at, updated_at
```

**Sửa đổi cần thiết**: ✅ Đã có đầy đủ trong schema (password_hash, is_admin, is_active)

**Ghi chú**: Hiện tại ORM models.py còn thiếu password_hash, is_active, last_login - cần update

---

### 2. **forms** 
**Trạng thái**: GIỮ

**Lý do**: 
- Lưu trữ các mẫu form tạo từ Word
- Lưu trữ các mẫu form tạo từ Excel
- Lưu trữ các form thông thường

**Cấu trúc**: id, user_id, form_name, description, created_at, updated_at

**Cải tiến đề xuất**: 
- Thêm `form_type` (enum: 'standard', 'word', 'excel') để phân loại
- Thêm `is_template` (boolean) để đánh dấu form mẫu

---

### 3. **fields**
**Trạng thái**: GIỮ

**Lý do**: Lưu trữ các trường trong form

**Cấu trúc**: id, form_id, field_name, field_type, display_order, created_at

**Cải tiến đề xuất**:
- Thêm `is_required` (boolean)
- Thêm `validation_rules` (JSON) - để validate input
- Thêm `placeholder` (string) - hướng dẫn nhập liệu

---

### 4. **entries** 
**Trạng thái**: GIỮ

**Lý do**: Lịch sử nhập dữ liệu - cơ sở để:
- Gợi ý auto-fill
- Excel auto-fill
- Phân tích dữ liệu

**Cấu trúc**: id, user_id, field_id, form_id, value, created_at

---

### 5. **suggestions**
**Trạng thái**: GIỮ

**Lý do**: Cache gợi ý từ entries - để Word form có gợi ý từ lịch sử

**Cấu trúc**: id, user_id, field_id, suggested_value, frequency, ranking, created_at, updated_at

---

### 6. **word_templates**
**Trạng thái**: GIỮ

**Lý do**: Lưu trữ Word templates được upload - phục vụ tính năng:
- Upload Word
- Tạo form từ Word
- Điền form từ Word

**Cấu trúc**: id, user_id, template_name, file_path, original_filename, fields_json, created_at, updated_at

---

### 7. **word_submissions**
**Trạng thái**: GIỮ

**Lý do**: Lịch sử submit form từ Word - để:
- Lưu trữ dữ liệu đã submit
- Tạo lịch sử (audit trail)
- Hiển thị submission history

**Cấu trúc**: id, template_id, user_id, submission_data, created_at

---

## ❌ BẢNG KHÔNG CẦN THIẾT (2 bảng)

### ❌ 1. **sessions** (schema.sql có, nhưng có thể thay thế)
**Lý do**: 
- Hệ thống hiện tại dùng JWT token (in-memory sessions)
- Nếu dùng JWT (stateless), không cần lưu sessions
- Nếu muốn support multi-device logout, có thể thêm sau

**Quyết định**: ⚠️ OPTIONAL
- Giữ nếu cần: Logout ngay lập tức, Multi-device management
- Bỏ nếu dùng JWT stateless

---

### ❌ 2. **login_logs** (schema.sql có)
**Lý do**:
- Quá chi tiết cho MVP
- Có thể thêm sau khi cần audit

**Quyết định**: ⚠️ OPTIONAL
- Bỏ ở MVP
- Thêm sau nếu cần audit security

---

## ✨ BẢNG CẦN THÊM (4 bảng mới)

### ➕ 1. **excel_templates** ⭐ QUAN TRỌNG
**Tính năng phục vụ**: Upload Excel → Tạo form → Tự động điền dữ liệu

**Cấu trúc**:
```sql
CREATE TABLE excel_templates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    template_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    sheet_name VARCHAR(255),              -- Tên sheet trong Excel
    headers_json TEXT,                    -- JSON danh sách cột headers
    data_row_start INT DEFAULT 2,         -- Hàng bắt đầu có dữ liệu
    mapping_json TEXT,                    -- JSON mapping: column -> field
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
);
```

**Ghi chú**: Tương tự word_templates nhưng thêm thông tin Excel-specific

---

### ➕ 2. **documents** ⭐ QUAN TRỌNG
**Tính năng phục vụ**: Soạn thảo có hỗ trợ AI

**Cấu trúc**:
```sql
CREATE TABLE documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content LONGTEXT NOT NULL,           -- HTML hoặc Markdown content
    description TEXT,
    document_type VARCHAR(50),            -- 'composition', 'template', 'draft'
    is_public BOOLEAN DEFAULT FALSE,      -- Chia sẻ công khai
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_updated_at (updated_at)
);
```

**Ghi chú**: 
- Hiện tại models.py có Document nhưng schema chưa có
- Cần thêm vào schema.sql

---

### ➕ 3. **composition_history** 
**Tính năng phục vụ**: Lịch sử AI suggestions & edits khi soạn thảo

**Cấu trúc**:
```sql
CREATE TABLE composition_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_id INT NOT NULL,
    user_id INT NOT NULL,
    action_type VARCHAR(50) NOT NULL,    -- 'suggestion', 'edit', 'acceptance', 'rejection'
    original_text VARCHAR(1000),         -- Text gốc
    suggested_text VARCHAR(1000),        -- Text được gợi ý
    modified_text VARCHAR(1000),         -- Text sau khi edit
    context TEXT,                         -- Ngữ cảnh để AI tạo gợi ý
    accepted INT DEFAULT 0,               -- 1: chấp nhận, 0: từ chối, NULL: chưa quyết định
    ai_model VARCHAR(50),                 -- Model AI được dùng (GPT-4, Claude, etc.)
    created_at TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_document_id (document_id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);
```

**Ghi chú**:
- Hiện tại models.py có nhưng schema chưa có
- Cần thêm vào schema.sql

---

### ➕ 4. **email_verifications** 
**Tính năng phục vụ**: Xác thực email khi đăng ký

**Cấu trúc**:
```sql
CREATE TABLE email_verifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    email VARCHAR(255) NOT NULL,
    token VARCHAR(500) UNIQUE NOT NULL,   -- Verification token
    expires_at TIMESTAMP NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_email (email),
    INDEX idx_token (token),
    INDEX idx_expires_at (expires_at)
);
```

**Lý do thêm**: 
- Đảm bảo email hợp lệ khi đăng ký
- Tăng tính bảo mật

---

### ➕ 5. **password_reset_tokens** (OPTIONAL)
**Tính năng phục vụ**: Reset password

**Cấu trúc**:
```sql
CREATE TABLE password_reset_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(500) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP NULL,               -- Nếu token đã được dùng
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_token (token),
    INDEX idx_expires_at (expires_at)
);
```

---

## 👨‍💼 BẢNG GỢI Ý BỔ SUNG CHO ADMIN (OPTIONAL)

### 🔧 **admin_audit_logs** (OPTIONAL - Nên thêm sau MVP)
**Tính năng phục vụ**: Quản lý admin - audit trail

```sql
CREATE TABLE admin_audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    action_type VARCHAR(100) NOT NULL,    -- 'user_delete', 'user_suspend', 'form_delete', etc.
    target_user_id INT,                   -- User bị tác động
    target_resource_type VARCHAR(50),     -- 'user', 'form', 'document', etc.
    target_resource_id INT,
    details JSON,                         -- Chi tiết thay đổi
    created_at TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_admin_id (admin_id),
    INDEX idx_created_at (created_at)
);
```

---

## 📋 BẢNG QUẢN LÝ PHÂN QUYỀN (OPTIONAL - Nên thêm sau MVP)

### 🔐 **roles** & **user_roles** (OPTIONAL)
Nếu muốn hierarchy roles (Admin, Editor, Viewer, etc.)

```sql
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,     -- 'admin', 'editor', 'viewer'
    description TEXT,
    created_at TIMESTAMP
);

CREATE TABLE user_roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    created_at TIMESTAMP,
    UNIQUE KEY unique_user_role (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);
```

---

## 📊 TỔNG QUAN KIẾN TRÚC CUỐI CÙNG

### **MVP - Phiên bản tối thiểu (11 bảng)**
```
✅ Bắt buộc (9 bảng):
├── users
├── forms
├── fields
├── entries
├── suggestions
├── word_templates
├── word_submissions
├── documents
└── composition_history

✅ Khuyến nghị (2 bảng):
├── excel_templates
└── email_verifications
```

### **Để phát triển thêm (Optional)**
```
📝 Quản lý admin:
├── admin_audit_logs

🔐 Phân quyền:
├── roles
├── user_roles

🔒 Bảo mật:
├── password_reset_tokens
├── sessions (nếu dùng non-stateless)
├── login_logs

💾 Khác:
├── notifications
├── api_keys
├── user_preferences
```

---

## 📝 CHECKLIST CẬP NHẬT DATABASE

- [ ] **Update schema.sql**: Thêm documents, composition_history, excel_templates
- [ ] **Update models.py**: Thêm excel_templates model, email_verifications
- [ ] **Update models.py**: Thêm password_hash, is_active, last_login vào User model
- [ ] **Update forms model**: Thêm form_type, is_template
- [ ] **Update fields model**: Thêm is_required, validation_rules, placeholder
- [ ] **Tạo migration**: Chuyển đổi cơ sở dữ liệu từ cô đơn sang đầy đủ
- [ ] **Update auth.py**: Dùng database thay vì in-memory users_db
- [ ] **Thêm email service**: Xác thực email khi đăng ký
- [ ] **Thêm password reset flow**: Sử dụng password_reset_tokens

---

## 🔍 CHI TIẾT TỪng CHỨC NĂNG

### 1️⃣ Upload Word → Tạo Form → Điền Form Có Gợi ý
**Bảng sử dụng**:
- `word_templates` (lưu Word)
- `forms` + `fields` (form được tạo)
- `entries` (dữ liệu đã điền)
- `suggestions` (gợi ý từ lịch sử)

### 2️⃣ Upload Excel → Tạo Form → Auto-fill
**Bảng sử dụng**:
- `excel_templates` ⭐ (mới)
- `forms` + `fields` (form được tạo)
- `entries` (dữ liệu từ Excel được tự động)

### 3️⃣ Soạn Thảo Có AI Support
**Bảng sử dụng**:
- `documents` ⭐ (mới)
- `composition_history` ⭐ (mới)

### 4️⃣ Đăng ký/Đăng Nhập
**Bảng sử dụng**:
- `users` (cập nhật: password_hash, is_active)
- `email_verifications` ⭐ (mới - cho xác thực email)
- `password_reset_tokens` (optional - cho reset)

### 5️⃣ Quản Lý Admin
**Bảng sử dụng**:
- `users` (với is_admin flag)
- `admin_audit_logs` (optional - cho audit)

---

## 🚀 ĐỀ XUẤT THỰC HIỆN

### **Giai đoạn 1 (MVP hiện tại)**
- Sửa schema.sql: Thêm 2 bảng mới (documents, composition_history, excel_templates)
- Update models.py ORM
- Tất cả chức năng đủ để hoạt động

### **Giai đoạn 2 (Enhance - tháng sau)**
- Thêm email_verifications
- Thêm password reset flow
- Migrate từ in-memory auth sang database auth

### **Giai đoạn 3 (Scale - quý sau)**
- Thêm admin_audit_logs
- Thêm roles/permissions system
- Thêm notifications system

---

**Cập nhật lần cuối**: 24/03/2026
