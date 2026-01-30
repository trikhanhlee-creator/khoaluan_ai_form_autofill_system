#!/usr/bin/env python3
"""
Script để làm sạch dữ liệu trong database AutoFill AI
"""

import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Thông số kết nối MySQL
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "ltK240304"
MYSQL_DATABASE = "autofill_db"

# URL kết nối
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

def clean_data():
    """Xóa tất cả dữ liệu từ các bảng nhưng giữ lại cấu trúc"""
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("  DATABASE CLEANUP - XÓA DỮ LIỆU")
        print("="*60)
        
        print("\n🔄 Bắt đầu xóa dữ liệu...\n")
        
        with engine.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")
            
            # Vô hiệu hóa kiểm tra khóa ngoại
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            
            # Xóa dữ liệu từ các bảng (theo thứ tự để tránh lỗi khóa ngoại)
            tables_to_clean = [
                'entries',
                'suggestions',
                'fields',
                'forms',
                'users',
            ]
            
            for table_name in tables_to_clean:
                try:
                    result = connection.execute(text(f"DELETE FROM {table_name}"))
                    print(f"  ✅ Xóa {result.rowcount} dòng từ bảng '{table_name}'")
                except Exception as e:
                    if "doesn't exist" in str(e):
                        print(f"  ⚠️  Bảng '{table_name}' không tồn tại, bỏ qua")
                    else:
                        raise
            
            # Bật lại kiểm tra khóa ngoại
            connection.execute(text("SET FOREIGN_KEY_CHECKS=1"))
            
            connection.close()
        
        print("\n✅ Database đã được làm sạch thành công!")
        print("   Tất cả dữ liệu đã bị xóa. Bảng vẫn tồn tại nhưng rỗng.")
        
        # Hiển thị thống kê
        print("\n📊 Thống kê sau khi xóa:")
        with engine.connect() as connection:
            for table_name in ['users', 'forms', 'fields', 'entries', 'suggestions']:
                try:
                    result = connection.execute(text(f"SELECT COUNT(*) as count FROM {table_name}"))
                    count = result.fetchone()[0]
                    print(f"  • {table_name.capitalize()}: {count} dòng")
                except:
                    print(f"  • {table_name.capitalize()}: (bảng không tồn tại)")
            connection.close()
        
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"❌ Lỗi khi xóa dữ liệu: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


def reset_database():
    """Reset database: xóa tất cả bảng và tạo lại từ schema"""
    print("\n⚠️  WARNING: Bạn sắp XÓA và TẠO LẠI tất cả bảng!")
    confirm = input("Bạn có chắc chắn không? (yes/no): ").lower().strip()
    
    if confirm != 'yes':
        print("❌ Hủy bỏ.")
        return
    
    engine = create_engine(DATABASE_URL, echo=False)
    
    try:
        print("\n" + "="*60)
        print("  DATABASE RESET - XÓA VÀ TẠO LẠI SCHEMA")
        print("="*60 + "\n")
        
        with engine.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")
            
            # Vô hiệu hóa kiểm tra khóa ngoại
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            
            # Xóa các bảng
            tables_to_drop = [
                'entries',
                'suggestions',
                'fields',
                'forms',
                'users',
            ]
            
            print("🗑️  Xóa các bảng...\n")
            for table_name in tables_to_drop:
                connection.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
                print(f"  ✅ Xóa bảng '{table_name}'")
            
            connection.close()
        
        # Đọc và thực thi schema SQL
        print("\n🛠️  Tạo lại các bảng...\n")
        with open('../database/schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        with engine.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")
            
            for statement in schema_sql.split(';'):
                statement = statement.strip()
                if statement:
                    try:
                        connection.execute(text(statement))
                    except Exception as e:
                        print(f"  ⚠️  Lỗi: {e}")
            
            # Bật lại kiểm tra khóa ngoại
            connection.execute(text("SET FOREIGN_KEY_CHECKS=1"))
            connection.close()
        
        print("\n✅ Database đã được reset thành công!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    else:
        clean_data()
