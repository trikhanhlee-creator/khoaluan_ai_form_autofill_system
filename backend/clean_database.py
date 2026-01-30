#!/usr/bin/env python3
"""
Script để xóa tất cả dữ liệu trong database AutoFill AI
Sử dụng SQLAlchemy để xóa dữ liệu một cách an toàn
"""

from app.db.session import SessionLocal, Base, engine
from app.db.models import Entry, Suggestion, Field, Form, User
from sqlalchemy import text


def clean_database():
    """Xóa tất cả dữ liệu từ tất cả các bảng"""
    db = SessionLocal()
    
    try:
        print("🔄 Bắt đầu xóa dữ liệu từ database...")
        
        # Vô hiệu hóa kiểm tra khóa ngoại
        db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        
        # Xóa dữ liệu từ các bảng (theo thứ tự để tránh lỗi khóa ngoại)
        tables_to_clean = [
            ('entries', Entry),
            ('suggestions', Suggestion),
            ('fields', Field),
            ('forms', Form),
            ('users', User),
        ]
        
        for table_name, model_class in tables_to_clean:
            count = db.query(model_class).delete()
            print(f"  ✅ Xóa {count} dòng từ bảng '{table_name}'")
        
        # Bật lại kiểm tra khóa ngoại
        db.execute(text("SET FOREIGN_KEY_CHECKS=1"))
        
        # Commit
        db.commit()
        
        print("\n✅ Database đã được làm sạch thành công!")
        print("   Tất cả dữ liệu đã bị xóa. Bảng vẫn tồn tại nhưng rỗng.")
        
        # Hiển thị thống kê
        print("\n📊 Thống kê sau khi xóa:")
        print(f"  • Users: {db.query(User).count()} dòng")
        print(f"  • Forms: {db.query(Form).count()} dòng")
        print(f"  • Fields: {db.query(Field).count()} dòng")
        print(f"  • Entries: {db.query(Entry).count()} dòng")
        print(f"  • Suggestions: {db.query(Suggestion).count()} dòng")
        
    except Exception as e:
        print(f"❌ Lỗi khi xóa dữ liệu: {str(e)}")
        db.rollback()
    finally:
        db.close()


def reset_database():
    """Reset database: xóa tất cả bảng và tạo lại"""
    print("\n⚠️  WARNING: Bạn sắp XÓA và TẠO LẠI tất cả bảng!")
    confirm = input("Bạn có chắc chắn không? (yes/no): ").lower().strip()
    
    if confirm != 'yes':
        print("❌ Hủy bỏ.")
        return
    
    db = SessionLocal()
    try:
        print("🗑️  Xóa tất cả bảng...")
        Base.metadata.drop_all(bind=engine)
        print("✅ Đã xóa tất cả bảng.")
        
        print("🛠️  Tạo lại tất cả bảng...")
        Base.metadata.create_all(bind=engine)
        print("✅ Đã tạo lại tất cả bảng.")
        
        print("\n✅ Database đã được reset thành công!")
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    print("\n" + "="*50)
    print("  AutoFill AI - Database Cleanup Tool")
    print("="*50 + "\n")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    else:
        clean_database()
