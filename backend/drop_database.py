#!/usr/bin/env python3
"""
Script để xóa toàn bộ database và tạo lại
"""

from sqlalchemy import create_engine, text

MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "ltK240304"
MYSQL_DATABASE = "autofill_db"

def drop_and_recreate_db():
    """Xóa toàn bộ database và tạo lại"""
    
    # Kết nối tới MySQL server mà không chỉ định database
    engine = create_engine(
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}",
        echo=False
    )
    
    print("🗑️  Xóa database...\n")
    
    with engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT")
        
        try:
            connection.execute(text(f"DROP DATABASE {MYSQL_DATABASE}"))
            print(f"✓ Xóa database '{MYSQL_DATABASE}'")
        except Exception as e:
            print(f"⚠️  Không thể xóa: {e}")
        
        try:
            connection.execute(text(f"CREATE DATABASE {MYSQL_DATABASE}"))
            print(f"✓ Tạo lại database '{MYSQL_DATABASE}'")
        except Exception as e:
            print(f"❌ Lỗi tạo database: {e}")
            return
        
        connection.close()
    
    print("\n✅ Database đã được xóa và tạo lại!")

if __name__ == "__main__":
    try:
        drop_and_recreate_db()
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()
