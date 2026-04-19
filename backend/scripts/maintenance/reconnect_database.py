"""
Script để kết nối lại MySQL và thiết kế lại database
"""

import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

BACKEND_DIR = Path(__file__).resolve().parents[2]
DATABASE_DIR = BACKEND_DIR.parent / "database"

# Thông số kết nối MySQL
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = input("Nhập MySQL username (mặc định: root): ").strip() or "root"
MYSQL_PASSWORD = input("Nhập MySQL password: ").strip()
MYSQL_DATABASE = "autofill_db"

# URL kết nối
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

def create_database():
    """Tạo database nếu chưa tồn tại"""
    # Kết nối tới MySQL server mà không chỉ định database
    engine = create_engine(
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}",
        echo=True
    )
    
    with engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT")
        # Tạo database
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}"))
        print(f"✓ Database '{MYSQL_DATABASE}' đã được tạo hoặc đã tồn tại")
        connection.close()

def setup_schema():
    """Thiết kế lại schema từ SQL file"""
    engine = create_engine(DATABASE_URL, echo=True)
    
    # Đọc schema SQL
    schema_file = DATABASE_DIR / 'schema.sql'
    with open(schema_file, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    with engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT")
        
        # Xóa tất cả các table cũ
        print("\n🧹 Xóa các bảng cũ...")
        tables = ['entries', 'suggestions', 'fields', 'forms', 'users']
        for table in tables:
            try:
                connection.execute(text(f"DROP TABLE IF EXISTS {table}"))
                print(f"  ✓ Xóa bảng '{table}'")
            except Exception as e:
                print(f"  ⚠ Không thể xóa bảng '{table}': {e}")
        
        # Tạo các bảng mới từ schema
        print("\n📐 Tạo các bảng mới...")
        for statement in schema_sql.split(';'):
            statement = statement.strip()
            if statement:
                try:
                    connection.execute(text(statement))
                except Exception as e:
                    print(f"  ⚠ Lỗi khi thực thi: {e}")
        
        print("✓ Schema đã được thiết kế lại thành công")
        connection.close()

def seed_data():
    """Nhập dữ liệu seed nếu file tồn tại"""
    import os
    
    seed_file = DATABASE_DIR / 'seed.sql'
    if not os.path.exists(seed_file):
        print(f"\n⚠ File {seed_file} không tồn tại, bỏ qua seed dữ liệu")
        return
    
    engine = create_engine(DATABASE_URL, echo=True)
    
    with open(seed_file, 'r', encoding='utf-8') as f:
        seed_sql = f.read()
    
    with engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT")
        
        print("\n🌱 Nhập dữ liệu seed...")
        for statement in seed_sql.split(';'):
            statement = statement.strip()
            if statement:
                try:
                    connection.execute(text(statement))
                except Exception as e:
                    print(f"  ⚠ Lỗi: {e}")
        
        print("✓ Dữ liệu seed đã được nhập")
        connection.close()

def verify_connection():
    """Kiểm tra kết nối database"""
    try:
        engine = create_engine(DATABASE_URL, echo=False)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("\n✓ Kết nối MySQL thành công!")
            return True
    except Exception as e:
        print(f"\n✗ Lỗi kết nối: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("RECONNECT & REBUILD DATABASE")
    print("=" * 60)
    
    try:
        # 1. Tạo database
        print("\n[1/4] Tạo database...")
        create_database()
        
        # 2. Thiết kế schema
        print("\n[2/4] Thiết kế schema...")
        setup_schema()
        
        # 3. Nhập dữ liệu seed
        print("\n[3/4] Nhập dữ liệu seed...")
        seed_data()
        
        # 4. Kiểm tra kết nối
        print("\n[4/4] Kiểm tra kết nối...")
        if verify_connection():
            print("\n" + "=" * 60)
            print("✓ DATABASE SETUP HOÀN THÀNH!")
            print("=" * 60)
            print(f"\nThông tin kết nối:")
            print(f"  Host: {MYSQL_HOST}")
            print(f"  Port: {MYSQL_PORT}")
            print(f"  Database: {MYSQL_DATABASE}")
            print(f"  User: {MYSQL_USER}")
            print(f"\nBạn có thể truy cập phpMyAdmin tại:")
            print(f"  http://localhost/phpmyadmin/")
        else:
            sys.exit(1)
            
    except Exception as e:
        print(f"\n✗ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
