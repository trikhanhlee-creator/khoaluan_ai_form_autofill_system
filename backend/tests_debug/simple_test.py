#!/usr/bin/env python3
"""Simple test to verify suggestions cache is working"""
import sys
import time
sys.path.insert(0, '.')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "mysql+pymysql://root:ltK240304@localhost:3306/autofill_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def setup():
    """Setup test data"""
    db = SessionLocal()
    try:
        print("Setting up test data...")
        # Delete old data
        db.execute(text("DELETE FROM suggestions"))
        db.execute(text("DELETE FROM entries"))
        db.execute(text("DELETE FROM fields"))
        db.execute(text("DELETE FROM forms"))
        db.execute(text("DELETE FROM users"))
        db.commit()
        
        # Create user, form, fields
        db.execute(text("""INSERT INTO users (id, email, username) VALUES (1, 'test@test.com', 'Test')"""))
        db.execute(text("""INSERT INTO forms (id, user_id, form_name) VALUES (1, 1, 'Test Form')"""))
        db.execute(text("""INSERT INTO fields (id, form_id, field_name, field_type, display_order) VALUES (1, 1, 'Province', 'text', 1)"""))
        db.commit()
        print("✓ Setup complete")
        
    finally:
        db.close()

def test_save_and_cache():
    """Test that save_entry updates suggestions cache"""
    db = SessionLocal()
    try:
        from app.services.suggestion_service import SuggestionService
        
        print("\nTest: Save entry and verify suggestions cache...")
        
        # Save 3 entries with same value
        for i in range(3):
            result = SuggestionService.save_entry(
                db=db,
                user_id=1,
                field_id=1,
                form_id=1,
                value="Ha Noi"
            )
            print(f"✓ Saved entry {i+1}: {result}")
        
        # Check suggestions table
        suggestions = db.execute(text("""
            SELECT suggested_value, frequency, ranking FROM suggestions 
            WHERE user_id=1 AND field_id=1
        """)).fetchall()
        
        print(f"\nSuggestions in cache: {len(suggestions)}")
        for sug in suggestions:
            print(f"  - Value: {sug[0]}, Frequency: {sug[1]}, Ranking: {sug[2]}")
        
        # Check entries table
        entries = db.execute(text("""
            SELECT id, value FROM entries WHERE user_id=1 AND field_id=1
        """)).fetchall()
        
        print(f"\nEntries in table: {len(entries)}")
        for entry in entries:
            print(f"  - ID: {entry[0]}, Value: {entry[1]}")
        
        if len(suggestions) > 0:
            print("\n✅ Suggestions cache is being populated!")
            return True
        else:
            print("\n❌ Suggestions cache is NOT being populated!")
            return False
        
    finally:
        db.close()

if __name__ == "__main__":
    setup()
    success = test_save_and_cache()
    sys.exit(0 if success else 1)
