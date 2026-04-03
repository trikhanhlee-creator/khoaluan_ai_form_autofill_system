"""
Script to seed initial users into the database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.db.models import User
from app.core.security import get_password_hash
from datetime import datetime

def seed_users():
    """Create initial user accounts"""
    db = SessionLocal()
    
    try:
        print("🚀 Seeding database with test accounts...\n")
        
        # Check if users already exist
        existing_user = db.query(User).filter(User.email == "user@example.com").first()
        existing_admin = db.query(User).filter(User.email == "admin@example.com").first()
        
        users_created = False
        
        if not existing_user:
            try:
                pwd_hash_user = get_password_hash("user123")
                user_account = User(
                    email="user@example.com",
                    username="user",
                    password_hash=pwd_hash_user,
                    is_admin=False,
                    is_active=True,
                    created_at=datetime.utcnow()
                )
                db.add(user_account)
                print("✓ Created user account: user@example.com (password: user123)")
                users_created = True
            except Exception as e:
                print(f"✗ Error creating user: {e}")
        else:
            print("✓ User account already exists")
        
        if not existing_admin:
            try:
                pwd_hash_admin = get_password_hash("admin123")
                admin_account = User(
                    email="admin@example.com",
                    username="admin",
                    password_hash=pwd_hash_admin,
                    is_admin=True,
                    is_active=True,
                    created_at=datetime.utcnow()
                )
                db.add(admin_account)
                print("✓ Created admin account: admin@example.com (password: admin123)")
                users_created = True
            except Exception as e:
                print(f"✗ Error creating admin: {e}")
        else:
            print("✓ Admin account already exists")
        
        # Commit if we created new users
        if users_created:
            db.commit()
            print("\n✓ Database seeding completed successfully!")
        else:
            print("\n✓ All accounts already exist")
        
        # Display all users
        all_users = db.query(User).all()
        print("\n📊 Current users in database:")
        print("─" * 60)
        for u in all_users:
            role = "👤 USER " if not u.is_admin else "👨‍💼 ADMIN"
            status = "✓ Active" if u.is_active else "⊘ Inactive"
            print(f"{role}  {u.username:15} ({u.email:25}) {status}")
        print("─" * 60)
            
    except Exception as e:
        print(f"✗ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_users()
