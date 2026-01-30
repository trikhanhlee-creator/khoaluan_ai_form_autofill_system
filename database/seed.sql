-- Insert users
INSERT INTO users (email, username) VALUES
('user1@example.com', 'Nguyễn Văn A'),
('user2@example.com', 'Trần Thị B');

-- Insert forms
INSERT INTO forms (user_id, form_name, description) VALUES
(1, 'Form Thông Tin Cá Nhân', 'Form điền thông tin cá nhân'),
(1, 'Form Địa Chỉ', 'Form điền địa chỉ'),
(2, 'Form Tuyển Dụng', 'Form ứng tuyển');

-- Insert fields
INSERT INTO fields (form_id, field_name, field_type, display_order) VALUES
(1, 'Tỉnh/Thành phố', 'text', 1),
(1, 'Quận/Huyện', 'text', 2),
(1, 'Phường/Xã', 'text', 3),
(2, 'Địa chỉ đầy đủ', 'text', 1),
(2, 'Mã bưu điện', 'text', 2),
(3, 'Vị trí ứng tuyển', 'text', 1),
(3, 'Ngành học', 'text', 2);

-- Insert entries (lịch sử nhập) cho field 1 (Tỉnh/Thành phố) của user 1
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

-- Insert entries cho field 2 (Quận/Huyện) của user 1
INSERT INTO entries (user_id, field_id, form_id, value) VALUES
(1, 2, 1, 'Quận 1'),
(1, 2, 1, 'Quận 1'),
(1, 2, 1, 'Quận 1'),
(1, 2, 1, 'Quận 3'),
(1, 2, 1, 'Quận 3');

-- Insert entries cho field 3 (Phường/Xã) của user 1
INSERT INTO entries (user_id, field_id, form_id, value) VALUES
(1, 3, 1, 'Phường Bến Nghé'),
(1, 3, 1, 'Phường Bến Nghé'),
(1, 3, 1, 'Phường Võ Thị Sáu'),
(1, 3, 1, 'Phường Võ Thị Sáu');

-- Insert entries cho field 4 (Địa chỉ đầy đủ) của user 1
INSERT INTO entries (user_id, field_id, form_id, value) VALUES
(1, 4, 2, '123 Đường Nguyễn Huệ, Quận 1, TP Hồ Chí Minh'),
(1, 4, 2, '123 Đường Nguyễn Huệ, Quận 1, TP Hồ Chí Minh'),
(1, 4, 2, '456 Đường Trần Hưng Đạo, Quận 5, TP Hồ Chí Minh'),
(1, 4, 2, '789 Đường Cách Mạng Tháng Tám, Quận 1, TP Hồ Chí Minh');

-- Insert entries cho field 5 (Mã bưu điện) của user 1
INSERT INTO entries (user_id, field_id, form_id, value) VALUES
(1, 5, 2, '700000'),
(1, 5, 2, '700000'),
(1, 5, 2, '700000'),
(1, 5, 2, '750000');

-- Insert entries cho field 6 (Vị trí ứng tuyển) của user 2
INSERT INTO entries (user_id, field_id, form_id, value) VALUES
(2, 6, 3, 'Kỹ sư Phần mềm'),
(2, 6, 3, 'Kỹ sư Phần mềm'),
(2, 6, 3, 'Kỹ sư Phần mềm'),
(2, 6, 3, 'Kỹ sư DevOps'),
(2, 6, 3, 'Kỹ sư DevOps');

-- Insert entries cho field 7 (Ngành học) của user 2
INSERT INTO entries (user_id, field_id, form_id, value) VALUES
(2, 7, 3, 'Công nghệ thông tin'),
(2, 7, 3, 'Công nghệ thông tin'),
(2, 7, 3, 'Công nghệ thông tin'),
(2, 7, 3, 'Khoa học máy tính'),
(2, 7, 3, 'Hệ thống thông tin');
