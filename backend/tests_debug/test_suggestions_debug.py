#!/usr/bin/env python
"""
Debug script để test suggestions flow
"""
import sys
import os

# Setup path
sys.path.insert(0, os.path.dirname(__file__))

from app.db.session import SessionLocal
from app.db.models import User, Form, Field, Entry, Suggestion, WordTemplate
from app.services.suggestion_service import SuggestionService
from app.ai.rule_engine import RuleEngine
from app.core.logger import logger
from datetime import datetime

def main():
    db = SessionLocal()
    
    print("=" * 80)
    print("SUGGESTIONS FLOW DEBUG TEST")
    print("=" * 80)
    
    # Setup test data
    print("\n[1] Setting up test data...")
    
    # Create/get user
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        user = User(id=1, username='test', email='test@example.com')
        db.add(user)
        db.commit()
    print(f"✓ User {user.id}: {user.email}")
    
    # Create/get form
    form = db.query(Form).filter(Form.id == 1).first()
    if not form:
        form = Form(id=1, user_id=1, form_name='Test Form')
        db.add(form)
        db.commit()
    print(f"✓ Form {form.id}: {form.form_name}")
    
    # Create/get field
    field = db.query(Field).filter(Field.id == 1).first()
    if not field:
        field = Field(id=1, form_id=1, field_name='name', field_type='text')
        db.add(field)
        db.commit()
    print(f"✓ Field {field.id}: {field.field_name}")
    
    # Clear existing entries
    print("\n[2] Clearing existing entries...")
    db.query(Suggestion).delete()
    db.query(Entry).delete()
    db.commit()
    print("✓ Cleared entries and suggestions")
    
    # Create test entries
    print("\n[3] Creating test entries...")
    values = ["Nguyễn Văn A", "Nguyễn Văn A", "Nguyễn Văn B"]
    for i, value in enumerate(values, 1):
        entry = Entry(
            user_id=1,
            field_id=1,
            form_id=1,
            value=value,
            created_at=datetime.utcnow()
        )
        db.add(entry)
        db.commit()
        print(f"  Entry {i}: '{value}'")
    
    # Verify entries in DB
    print("\n[4] Verifying entries in database...")
    entries = db.query(Entry).filter(Entry.user_id == 1, Entry.field_id == 1).all()
    print(f"✓ Total entries: {len(entries)}")
    for e in entries:
        print(f"  - Entry {e.id}: '{e.value}' (created: {e.created_at})")
    
    # Test getting entries via repository
    print("\n[5] Testing EntryRepository.get_recent_entries()...")
    from app.db.repositories.entry_repo import EntryRepository
    repo_entries = EntryRepository.get_recent_entries(db, user_id=1, field_id=1, limit=1000)
    print(f"✓ Repository returned {len(repo_entries)} entries")
    for e in repo_entries:
        print(f"  - Entry {e.id}: '{e.value}'")
    
    # Test RuleEngine
    print("\n[6] Testing RuleEngine.generate_suggestions()...")
    suggestions = RuleEngine.generate_suggestions(entries, top_k=5)
    print(f"✓ Generated {len(suggestions)} suggestions")
    for s in suggestions:
        print(f"  - '{s['suggested_value']}' (frequency: {s['frequency']}, ranking: {s['ranking']})")
    
    # Test SuggestionService.get_suggestions
    print("\n[7] Testing SuggestionService.get_suggestions()...")
    service_suggestions = SuggestionService.get_suggestions(
        db=db,
        user_id=1,
        field_id=1,
        top_k=5
    )
    print(f"✓ Service returned {len(service_suggestions)} suggestions")
    for s in service_suggestions:
        print(f"  - '{s['suggested_value']}' (frequency: {s['frequency']}, ranking: {s['ranking']})")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)
    
    db.close()

if __name__ == '__main__':
    main()
