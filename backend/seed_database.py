#!/usr/bin/env python3
"""
Script để nhập lại dữ liệu seed vào database
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Thông số kết nối
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "ltK240304"
MYSQL_DATABASE = "autofill_db"

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

def seed_data():
    """Nhập dữ liệu seed"""
    engine = create_engine(DATABASE_URL, echo=False)
    
    with engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT")
        
        # Vô hiệu hoá check khóa ngoại
        connection.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        
        print("🌱 Nhập dữ liệu seed...\n")
        
        # Insert users
        connection.execute(text("""
            INSERT INTO users (email, username) VALUES
            ('user1@example.com', 'Nguyễn Văn A'),
            ('user2@example.com', 'Trần Thị B')
        """))
        print("✅ Nhập 2 users")
        
        # Insert forms
        connection.execute(text("""
            INSERT INTO forms (user_id, form_name, description) VALUES
            (1, 'Form Thông Tin Cá Nhân', 'Form điền thông tin cá nhân'),
            (1, 'Form Địa Chỉ', 'Form điền địa chỉ'),
            (2, 'Form Tuyển Dụng', 'Form ứng tuyển')
        """))
        print("✅ Nhập 3 forms")
        
        # Insert fields
        connection.execute(text("""
            INSERT INTO fields (form_id, field_name, field_type, display_order) VALUES
            (1, 'Tỉnh/Thành phố', 'text', 1),
            (1, 'Quận/Huyện', 'text', 2),
            (1, 'Phường/Xã', 'text', 3),
            (2, 'Địa chỉ đầy đủ', 'text', 1),
            (2, 'Mã bưu điện', 'text', 2),
            (3, 'Vị trí ứng tuyển', 'text', 1),
            (3, 'Ngành học', 'text', 2)
        """))
        print("✅ Nhập 7 fields")
        
        # Insert entries cho field 1 (Tỉnh/Thành phố)
        connection.execute(text("""
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
            (1, 1, 1, 'Đà Nẵng')
        """))
        print("✅ Nhập 10 entries cho field 1")
        
        # Insert entries cho field 2 (Quận/Huyện)
        connection.execute(text("""
            INSERT INTO entries (user_id, field_id, form_id, value) VALUES
            (1, 2, 1, 'Quận 1'),
            (1, 2, 1, 'Quận 1'),
            (1, 2, 1, 'Quận 1'),
            (1, 2, 1, 'Quận 3'),
            (1, 2, 1, 'Quận 3')
        """))
        print("✅ Nhập 5 entries cho field 2")
        
        # Insert entries cho field 3 (Phường/Xã)
        connection.execute(text("""
            INSERT INTO entries (user_id, field_id, form_id, value) VALUES
            (1, 3, 1, 'Phường Bến Nghé'),
            (1, 3, 1, 'Phường Bến Nghé'),
            (1, 3, 1, 'Phường Võ Thị Sáu'),
            (1, 3, 1, 'Phường Võ Thị Sáu')
        """))
        print("✅ Nhập 4 entries cho field 3")
        
        # Insert entries cho field 4 (Địa chỉ đầy đủ)
        connection.execute(text("""
            INSERT INTO entries (user_id, field_id, form_id, value) VALUES
            (1, 4, 2, '123 Đường Nguyễn Huệ, Quận 1, TP Hồ Chí Minh'),
            (1, 4, 2, '123 Đường Nguyễn Huệ, Quận 1, TP Hồ Chí Minh'),
            (1, 4, 2, '456 Đường Trần Hưng Đạo, Quận 5, TP Hồ Chí Minh'),
            (1, 4, 2, '789 Đường Cách Mạng Tháng Tám, Quận 1, TP Hồ Chí Minh')
        """))
        print("✅ Nhập 4 entries cho field 4")
        
        # Insert entries cho field 5 (Mã bưu điện)
        connection.execute(text("""
            INSERT INTO entries (user_id, field_id, form_id, value) VALUES
            (1, 5, 2, '700000'),
            (1, 5, 2, '700000'),
            (1, 5, 2, '700000'),
            (1, 5, 2, '750000')
        """))
        print("✅ Nhập 4 entries cho field 5")
        
        # Insert entries cho field 6 (Vị trí ứng tuyển)
        connection.execute(text("""
            INSERT INTO entries (user_id, field_id, form_id, value) VALUES
            (2, 6, 3, 'Kỹ sư Phần mềm'),
            (2, 6, 3, 'Kỹ sư Phần mềm'),
            (2, 6, 3, 'Kỹ sư Phần mềm'),
            (2, 6, 3, 'Kỹ sư DevOps'),
            (2, 6, 3, 'Kỹ sư DevOps')
        """))
        print("✅ Nhập 5 entries cho field 6")
        
        # Insert entries cho field 7 (Ngành học)
        connection.execute(text("""
            INSERT INTO entries (user_id, field_id, form_id, value) VALUES
            (2, 7, 3, 'Công nghệ thông tin'),
            (2, 7, 3, 'Công nghệ thông tin'),
            (2, 7, 3, 'Công nghệ thông tin'),
            (2, 7, 3, 'Khoa học máy tính'),
            (2, 7, 3, 'Hệ thống thông tin')
        """))
        print("✅ Nhập 5 entries cho field 7")
        
        # Bật lại check khóa ngoại
        connection.execute(text("SET FOREIGN_KEY_CHECKS=1"))
        
        connection.close()
    
    print("\n✅ Dữ liệu seed đã được nhập thành công!")

if __name__ == "__main__":
    try:
        seed_data()
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()
