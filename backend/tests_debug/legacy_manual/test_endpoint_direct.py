#!/usr/bin/env python3
"""Test the template endpoint directly without HTTP"""
import sys
sys.path.insert(0, '.')
from app.db.session import SessionLocal
from app.db.models import WordTemplate, Field, Form, User
from app.core.file_utils import extract_clean_filename
import json

db = SessionLocal()

# Get the latest template
from sqlalchemy import desc
template = db.query(WordTemplate).order_by(desc(WordTemplate.id)).first()

if not template:
    print("No templates found")
    db.close()
    exit(1)

print(f"Testing template {template.id}...")
print(f"Template name: {template.template_name}")
print()

# Simulate the endpoint logic
template_id = template.id
form_id = 1
user_id = 1

# Ensure form exists
form = db.query(Form).filter(Form.id == form_id).first()
if not form:
    form = Form(id=form_id, user_id=user_id, name="Default Form")
    db.add(form)
    db.commit()

# Ensure user exists
user = db.query(User).filter(User.id == user_id).first()
if not user:
    user = User(id=user_id, email=f"user_{user_id}@test.local", username=f"user_{user_id}")
    db.add(user)
    db.commit()

try:
    fields_json = json.loads(template.fields_json) if template.fields_json else []
    print(f"Loaded {len(fields_json)} fields from JSON\n")
    
    enriched_fields = []
    for idx, field_data in enumerate(fields_json):
        print(f"Processing field {idx}: {field_data.get('name', 'UNKNOWN')}")
        
        field_name = field_data.get("name", "")
        field_label = field_data.get("label", field_name)
        field_type = field_data.get("field_type", "text")
        field_order = field_data.get("order", idx)
        
        print(f"  - name={field_name}, label={field_label}")
        
        # Try to find field
        db_field = db.query(Field).filter(
            Field.form_id == form_id,
            Field.field_name == field_name
        ).first()
        
        if not db_field:
            print(f"  - Field not in DB, creating...")
            try:
                db_field = Field(
                    form_id=form_id,
                    field_name=field_name,
                    field_type=field_type,
                    display_order=field_order
                )
                db.add(db_field)
                db.commit()
                db.refresh(db_field)
                print(f"  ✓ Created field with id={db_field.id}")
            except Exception as e:
                print(f"  ❌ Error: {e}")
                db.rollback()
                db_field = None
        else:
            print(f"  ✓ Found existing field with id={db_field.id}")
        
        field_id = db_field.id if db_field else -1
        
        enriched = {
            **field_data,
            "field_id": field_id,
            "field_index": idx,
            "field_label": field_label
        }
        enriched_fields.append(enriched)
        print(f"  Final: field_id={field_id}\n")
    
    print("=" * 60)
    print("Building response...")
    
    response = {
        "id": template.id,
        "name": template.template_name,
        "filename": extract_clean_filename(template.original_filename),
        "fields": enriched_fields,
        "form_id": form_id,
        "created_at": template.created_at.isoformat() if template.created_at else None,
        "submissions_count": len(template.submissions) if template.submissions else 0
    }
    
    print("✅ Response created successfully!")
    print(json.dumps(response, indent=2, ensure_ascii=False))
    
except Exception as e:
    import traceback
    print(f"\n❌ ERROR: {e}")
    print("\nTraceback:")
    traceback.print_exc()
finally:
    db.close()
