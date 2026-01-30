#!/usr/bin/env python3
"""Clean database script - remove all entries and suggestions"""

from app.db.session import SessionLocal
from app.db.models import Entry, Suggestion, WordTemplate, WordSubmission, User, Form, Field

def clean_database():
    db = SessionLocal()
    
    # Delete in correct order (cascade will handle some relationships)
    # But explicitly delete in order to be safe:
    # 1. Delete entries and suggestions first (they reference fields)
    entries_deleted = db.query(Entry).delete()
    suggestions_deleted = db.query(Suggestion).delete()
    submissions_deleted = db.query(WordSubmission).delete()
    templates_deleted = db.query(WordTemplate).delete()
    
    # 2. Then delete forms and fields (optional - can recreate)
    # For now, keep structure but clear data
    
    db.commit()
    
    print(f"Deleted:")
    print(f"  - {entries_deleted} entries")
    print(f"  - {suggestions_deleted} suggestions")
    print(f"  - {submissions_deleted} submissions")
    print(f"  - {templates_deleted} templates")
    
    # Ensure user exists
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        user = User(id=1, username='test', email='test@example.com')
        db.add(user)
    
    # Ensure form exists
    form = db.query(Form).filter(Form.id == 1).first()
    if not form:
        form = Form(id=1, user_id=1, form_name='Test Form')
        db.add(form)
    
    db.flush()
    
    # Ensure fields exist
    field_names = ['name', 'email', 'phone', 'city', 'company']
    for idx, name in enumerate(field_names, 1):
        field = db.query(Field).filter(Field.id == idx).first()
        if not field:
            field = Field(id=idx, form_id=1, field_name=name)
            db.add(field)
    
    db.commit()
    
    print("\nDatabase Status:")
    print("  - User 1: OK")
    print("  - Form 1: OK")
    print("  - Fields: OK (5 fields)")
    print("  - Entries: CLEAN")
    print("  - Suggestions: CLEAN")
    print("\nReady for testing!")
    
    db.close()

if __name__ == '__main__':
    clean_database()
