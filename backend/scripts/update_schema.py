"""
Script to update database schema and add missing columns
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.db.session import SessionLocal

def update_schema():
    """Add missing columns to users table"""
    db = SessionLocal()
    
    try:
        print("🔄 Updating database schema...\n")
        
        # Add password_hash column
        try:
            db.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255) NOT NULL DEFAULT ''"))
            db.commit()
            print("✓ Added password_hash column")
        except Exception as e:
            if "Duplicate column" in str(e):
                print("✓ password_hash column already exists")
            else:
                print(f"  password_hash: {str(e)[:50]}")
        
        # Add is_active column
        try:
            db.execute(text("ALTER TABLE users ADD COLUMN is_active TINYINT(1) DEFAULT 1"))
            db.commit()
            print("✓ Added is_active column")
        except Exception as e:
            if "Duplicate column" in str(e):
                print("✓ is_active column already exists")
            else:
                print(f"  is_active: {str(e)[:50]}")
        
        # Add last_login column
        try:
            db.execute(text("ALTER TABLE users ADD COLUMN last_login TIMESTAMP NULL"))
            db.commit()
            print("✓ Added last_login column")
        except Exception as e:
            if "Duplicate column" in str(e):
                print("✓ last_login column already exists")
            else:
                print(f"  last_login: {str(e)[:50]}")
        
        print("\n✓ Database schema updated successfully!")
        
    except Exception as e:
        print(f"✗ Error updating schema: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_schema()
