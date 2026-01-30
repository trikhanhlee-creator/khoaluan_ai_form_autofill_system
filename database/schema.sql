-- Bảng người dùng
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng form
CREATE TABLE IF NOT EXISTS forms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    form_name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Bảng field (các trường trong form)
CREATE TABLE IF NOT EXISTS fields (
    id INT AUTO_INCREMENT PRIMARY KEY,
    form_id INT NOT NULL,
    field_name VARCHAR(255) NOT NULL,
    field_type VARCHAR(50),
    display_order INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (form_id) REFERENCES forms(id) ON DELETE CASCADE
);

-- Bảng lịch sử nhập (entry history)
CREATE TABLE IF NOT EXISTS entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    field_id INT NOT NULL,
    value VARCHAR(1000) NOT NULL,
    form_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (field_id) REFERENCES fields(id) ON DELETE CASCADE,
    FOREIGN KEY (form_id) REFERENCES forms(id) ON DELETE CASCADE,
    KEY idx_user_field (user_id, field_id, created_at)
);

-- Bảng gợi ý (suggestions cache)
CREATE TABLE IF NOT EXISTS suggestions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    field_id INT NOT NULL,
    suggested_value VARCHAR(1000) NOT NULL,
    frequency INT DEFAULT 1,
    ranking INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (field_id) REFERENCES fields(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_field_value (user_id, field_id, suggested_value)
);
