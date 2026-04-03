#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from app.db.session import SessionLocal
from app.db.models import Field, WordTemplate
import json

db = SessionLocal()

# Get the latest template
template = db.query(WordTemplate).order_by(WordTemplate.id.desc()).first()
if template:
    print(f'Template ID: {template.id}')
    print(f'Fields JSON:')
    fields_json = json.loads(template.fields_json)
    for f in fields_json:
        print(f'  - NAME: {repr(f.get("name", ""))}')
        print(f'    LABEL: {repr(f.get("label", ""))}')
        print()

# Check fields in database
print('\nFields in database:')
fields = db.query(Field).all()
for f in fields:
    print(f'  Field ID={f.id}: name={repr(f.field_name)}')

db.close()
