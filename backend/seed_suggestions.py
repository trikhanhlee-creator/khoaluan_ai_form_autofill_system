#!/usr/bin/env python3
"""Seed test data into database"""
import sys
import io

# Fix encoding for Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app.db.session import SessionLocal
from app.db.models import Entry, Suggestion
from datetime import datetime, timedelta
import random

db = SessionLocal()

# Test data for fields
test_data = {
    1: {  # name field
        'name': 'name',
        'values': [
            'Nguyen Van A',
            'Tran Thi B', 
            'Le Minh C',
            'Pham Duy D',
            'Hoang Thu E'
        ]
    },
    2: {  # email field
        'name': 'email',
        'values': [
            'nguyenvana@gmail.com',
            'tranb@yahoo.com',
            'leminc@hotmail.com',
            'phamduyd@gmail.com',
            'hoangthue@outlook.com'
        ]
    },
    3: {  # phone field
        'name': 'phone',
        'values': [
            '0912345678',
            '0987654321',
            '0945612378',
            '0934567890',
            '0923456789'
        ]
    },
    4: {  # city field
        'name': 'city',
        'values': [
            'Ha Noi',
            'Ho Chi Minh City',
            'Da Nang',
            'Hai Phong',
            'Can Tho'
        ]
    },
    5: {  # company field
        'name': 'company',
        'values': [
            'Google Vietnam',
            'Microsoft Vietnam',
            'Apple Vietnam',
            'Facebook Vietnam',
            'Amazon Vietnam'
        ]
    }
}

print("Seeding test data...")

# Create entries and suggestions
for field_id, field_data in test_data.items():
    print(f"\nField {field_id} ({field_data['name']}):")
    
    for idx, value in enumerate(field_data['values']):
        # Create entry
        entry = Entry(
            user_id=1,
            field_id=field_id,
            form_id=1,
            value=value,
            created_at=datetime.utcnow() - timedelta(days=5-idx)
        )
        db.add(entry)
        
        # Create suggestion
        suggestion = Suggestion(
            user_id=1,
            field_id=field_id,
            suggested_value=value,
            frequency=5 - idx,  # Most recent has higher frequency
            ranking=idx + 1,
            created_at=datetime.utcnow() - timedelta(days=5-idx),
            updated_at=datetime.utcnow()
        )
        db.add(suggestion)
        print(f"  + {value}")

db.commit()

# Verify
entries = db.query(Entry).all()
suggs = db.query(Suggestion).all()
print(f"\nDone!")
print(f"   Entries: {len(entries)}")
print(f"   Suggestions: {len(suggs)}")

db.close()
