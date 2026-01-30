-- Script xóa tất cả dữ liệu trong database AutoFill AI
-- Chạy script này để reset database về trạng thái rỗng

-- Vô hiệu hóa kiểm tra khóa ngoại tạm thời
SET FOREIGN_KEY_CHECKS=0;

-- Xóa tất cả dữ liệu từ các bảng (giữ lại cấu trúc)
TRUNCATE TABLE autofill_ai.entries;
TRUNCATE TABLE autofill_ai.suggestions;
TRUNCATE TABLE autofill_ai.fields;
TRUNCATE TABLE autofill_ai.forms;
TRUNCATE TABLE autofill_ai.users;

-- Bật lại kiểm tra khóa ngoại
SET FOREIGN_KEY_CHECKS=1;

-- Xác nhận
SELECT 'Database cleaned successfully!' AS Status;

-- Kiểm tra số dòng còn lại trong mỗi bảng
SELECT 'users' AS table_name, COUNT(*) AS row_count FROM autofill_ai.users
UNION ALL
SELECT 'forms', COUNT(*) FROM autofill_ai.forms
UNION ALL
SELECT 'fields', COUNT(*) FROM autofill_ai.fields
UNION ALL
SELECT 'entries', COUNT(*) FROM autofill_ai.entries
UNION ALL
SELECT 'suggestions', COUNT(*) FROM autofill_ai.suggestions;
