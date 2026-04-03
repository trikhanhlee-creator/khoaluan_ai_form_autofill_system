-- ========================================
-- SCRIPT XÓA VÀ TẠO LẠI CƠ SỞ DỮ LIỆU
-- Sử dụng khi cơ sở dữ liệu bị lỗi hoặc cần reset toàn bộ dữ liệu
-- ========================================

-- Tắt tạm thời kiểm tra khóa ngoại để có thể xóa các bảng
SET FOREIGN_KEY_CHECKS=0;

-- ========== BƯỚC 1: XÓA TẤT CẢ CÁC BẢNG CŨ ==========
-- Xóa bảng lịch sử soạn thảo (AI suggestions)
DROP TABLE IF EXISTS composition_history;
-- Xóa bảng tài liệu soạn thảo
DROP TABLE IF EXISTS documents;
-- Xóa bảng xác thực email
DROP TABLE IF EXISTS email_verifications;
-- Xóa bảng template Excel
DROP TABLE IF EXISTS excel_templates;
-- Xóa bảng lịch sử submit form Word
DROP TABLE IF EXISTS word_submissions;
-- Xóa bảng mẫu template Word
DROP TABLE IF EXISTS word_templates;
-- Xóa bảng gợi ý
DROP TABLE IF EXISTS suggestions;
-- Xóa bảng lịch sử nhập liệu
DROP TABLE IF EXISTS entries;
-- Xóa bảng trường dữ liệu
DROP TABLE IF EXISTS fields;
-- Xóa bảng mẫu form
DROP TABLE IF EXISTS forms;
-- Xóa bảng người dùng
DROP TABLE IF EXISTS users;

-- ========== BƯỚC 2: TẠO LẠI TẤT CẢ CÁC BẢNG MỚI ==========

-- Bảng người dùng: lưu trữ thông tin tài khoản người dùng
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,  -- Email duy nhất của người dùng
    username VARCHAR(100) NOT NULL,      -- Tên người dùng
    password_hash VARCHAR(255) NOT NULL, -- Hash của mật khẩu (bcrypt/argon2)
    is_admin BOOLEAN DEFAULT FALSE,      -- Cờ admin để phân biệt quản trị viên
    is_active BOOLEAN DEFAULT TRUE,      -- Trạng thái kích hoạt tài khoản
    last_login TIMESTAMP NULL,           -- Thời gian đăng nhập cuối cùng
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Thời gian tạo tài khoản
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Thời gian cập nhật
    INDEX idx_email (email),  -- Index để tìm kiếm theo email nhanh hơn
    INDEX idx_username (username)  -- Index để tìm kiếm theo username nhanh hơn
);

-- Bảng mẫu form: lưu trữ các mẫu form của người dùng
CREATE TABLE forms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,                -- ID người dùng sở hữu form này
    form_name VARCHAR(255) NOT NULL,     -- Tên mẫu form
    description TEXT,                    -- Mô tả chi tiết về form
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Thời gian tạo form
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Thời gian cập nhật
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,  -- Xóa cascading: xóa user thì xóa form
    INDEX idx_user_id (user_id)  -- Index tìm kiếm form theo user nhanh hơn
);

-- Bảng trường dữ liệu: lưu trữ các trường trong mỗi form
CREATE TABLE fields (
    id INT AUTO_INCREMENT PRIMARY KEY,
    form_id INT NOT NULL,                -- ID form chứa trường này
    field_name VARCHAR(255) NOT NULL,    -- Tên trường (ví dụ: Họ tên, Email, Số điện thoại)
    field_type VARCHAR(50),              -- Loại trường (text, email, number, date, etc.)
    display_order INT,                   -- Vị trí hiển thị trường trong form
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Thời gian tạo trường
    FOREIGN KEY (form_id) REFERENCES forms(id) ON DELETE CASCADE,  -- Xóa cascading
    INDEX idx_form_id (form_id)  -- Index tìm kiếm trường theo form nhanh hơn
);

-- Bảng lịch sử nhập liệu: lưu trữ tất cả các lần nhập dữ liệu của người dùng
CREATE TABLE entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,                -- ID người dùng nhập dữ liệu
    field_id INT NOT NULL,               -- ID trường được nhập
    form_id INT NOT NULL,                -- ID form chứa trường này
    value VARCHAR(1000) NOT NULL,        -- Giá trị được nhập vào
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Thời gian nhập
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,  -- Xóa cascading
    FOREIGN KEY (field_id) REFERENCES fields(id) ON DELETE CASCADE,  -- Xóa cascading
    FOREIGN KEY (form_id) REFERENCES forms(id) ON DELETE CASCADE,  -- Xóa cascading
    KEY idx_user_field (user_id, field_id, created_at)  -- Index ghép để tìm kiếm nhanh
);

-- Bảng gợi ý: cache gợi ý được generate từ lịch sử nhập liệu
CREATE TABLE suggestions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,                -- ID người dùng
    field_id INT NOT NULL,               -- ID trường cần gợi ý
    suggested_value VARCHAR(1000) NOT NULL,  -- Giá trị được gợi ý
    frequency INT DEFAULT 1,             -- Số lần giá trị này xuất hiện (mức độ phổ biến)
    ranking INT,                         -- Vị trí xếp hạng gợi ý (1, 2, 3...)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Thời gian tạo gợi ý
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Thời gian cập nhật
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,  -- Xóa cascading
    FOREIGN KEY (field_id) REFERENCES fields(id) ON DELETE CASCADE,  -- Xóa cascading
    INDEX idx_user_field (user_id, field_id),  -- Index tìm kiếm gợi ý theo user và field
    INDEX idx_frequency (frequency DESC)  -- Index sắp xếp theo tần suất giảm dần
);

-- Bảng mẫu template Word: lưu trữ các mẫu tài liệu Word được upload
CREATE TABLE word_templates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,                -- ID người dùng upload template
    template_name VARCHAR(255) NOT NULL, -- Tên của template
    file_path VARCHAR(500) NOT NULL,     -- Đường dẫn lưu file trên máy chủ
    original_filename VARCHAR(255) NOT NULL,  -- Tên file gốc do người dùng upload
    fields_json TEXT,                    -- Dữ liệu các trường trong template (dạng JSON)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Thời gian upload template
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Thời gian cập nhật
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,  -- Xóa cascading
    INDEX idx_user_id (user_id)  -- Index tìm kiếm template theo user nhanh hơn
);

-- Bảng lịch sử submit form từ Word: lưu trữ các lần submit dữ liệu từ template Word
CREATE TABLE word_submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    template_id INT NOT NULL,            -- ID template Word được sử dụng
    user_id INT NOT NULL,                -- ID người dùng submit form
    submission_data TEXT,                -- Dữ liệu form đã submit (dạng JSON)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Thời gian submit
    FOREIGN KEY (template_id) REFERENCES word_templates(id) ON DELETE CASCADE,  -- Xóa cascading
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,  -- Xóa cascading
    INDEX idx_template_id (template_id),  -- Index tìm kiếm submission theo template
    INDEX idx_user_id (user_id)  -- Index tìm kiếm submission theo user
);

-- Bảng mẫu template Excel: lưu trữ các mẫu tài liệu Excel được upload
CREATE TABLE excel_templates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,                -- ID người dùng upload template
    template_name VARCHAR(255) NOT NULL, -- Tên của template
    file_path VARCHAR(500) NOT NULL,     -- Đường dẫn lưu file trên máy chủ
    original_filename VARCHAR(255) NOT NULL,  -- Tên file gốc do người dùng upload
    sheet_name VARCHAR(255),             -- Tên sheet trong Excel
    headers_json TEXT,                   -- JSON danh sách cột headers
    data_row_start INT DEFAULT 2,        -- Hàng bắt đầu có dữ liệu
    mapping_json TEXT,                   -- JSON mapping: column -> field
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Thời gian upload template
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Thời gian cập nhật
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,  -- Xóa cascading
    INDEX idx_user_id (user_id)  -- Index tìm kiếm template theo user
);

-- Bảng tài liệu soạn thảo: lưu trữ các tài liệu được soạn thảo
CREATE TABLE documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,                -- ID người dùng sở hữu tài liệu
    title VARCHAR(255) NOT NULL,         -- Tiêu đề tài liệu
    content LONGTEXT NOT NULL,           -- Nội dung tài liệu (HTML hoặc Markdown)
    description TEXT,                    -- Mô tả tài liệu
    document_type VARCHAR(50),           -- Loại tài liệu ('composition', 'template', 'draft')
    is_public BOOLEAN DEFAULT FALSE,     -- Chia sẻ công khai
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Thời gian tạo
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Thời gian cập nhật
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,  -- Xóa cascading
    INDEX idx_user_id (user_id),  -- Index tìm kiếm tài liệu theo user
    INDEX idx_updated_at (updated_at)  -- Index sắp xếp theo thời gian cập nhật
);

-- Bảng lịch sử soạn thảo: lưu trữ các gợi ý AI và chỉnh sửa trong quá trình soạn thảo
CREATE TABLE composition_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_id INT NOT NULL,            -- ID tài liệu được soạn thảo
    user_id INT NOT NULL,                -- ID người dùng
    action_type VARCHAR(50) NOT NULL,    -- Loại hành động ('suggestion', 'edit', 'acceptance', 'rejection')
    original_text VARCHAR(1000),         -- Text gốc trước khi chỉnh sửa
    suggested_text VARCHAR(1000),        -- Text được gợi ý bởi AI
    modified_text VARCHAR(1000),         -- Text sau khi chỉnh sửa
    context TEXT,                        -- Ngữ cảnh để AI tạo gợi ý
    accepted INT DEFAULT 0,              -- Trạng thái chấp nhận (1: chấp nhận, 0: từ chối, NULL: chưa quyết định)
    ai_model VARCHAR(50),                -- Model AI được sử dụng (GPT-4, Claude, etc.)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Thời gian hành động
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,  -- Xóa cascading
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,  -- Xóa cascading
    INDEX idx_document_id (document_id),  -- Index tìm kiếm theo tài liệu
    INDEX idx_user_id (user_id),  -- Index tìm kiếm theo user
    INDEX idx_created_at (created_at)  -- Index sắp xếp theo thời gian
);

-- Bảng xác thực email: quản lý xác thực email khi người dùng đăng ký
CREATE TABLE email_verifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,                -- ID người dùng
    email VARCHAR(255) NOT NULL,         -- Email cần xác thực
    token VARCHAR(500) UNIQUE NOT NULL,  -- Token xác thực (UUID hoặc random string)
    expires_at TIMESTAMP NOT NULL,       -- Thời gian hết hạn token
    is_verified BOOLEAN DEFAULT FALSE,   -- Trạng thái xác thực
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Thời gian tạo token
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,  -- Xóa cascading
    INDEX idx_email (email),  -- Index tìm kiếm theo email
    INDEX idx_token (token),  -- Index tìm kiếm theo token
    INDEX idx_expires_at (expires_at)  -- Index tìm kiếm token hết hạn
);

-- Bật lại kiểm tra khóa ngoại
SET FOREIGN_KEY_CHECKS=1;

-- ========== BƯỚC 3: HOÀN THÀNH ==========
-- ✅ Tất cả các bảng đã được tạo lại thành công!
-- 📋 Các bảng tạo được: users, forms, fields, entries, suggestions, word_templates, word_submissions, excel_templates, documents, composition_history, email_verifications
-- 🔐 Quản lý người dùng: users (password_hash, is_admin, is_active, last_login)
-- 💾 Để nhập dữ liệu mẫu, chạy script: backend/seed_database.py
