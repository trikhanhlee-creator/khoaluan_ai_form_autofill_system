#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '.')
os.environ['PYTHONIOENCODING'] = 'utf-8'
import json
from app.db.session import SessionLocal
from app.db.models import WordTemplate, Field
from sqlalchemy import desc

db = SessionLocal()

# Get the latest template
template = db.query(WordTemplate).order_by(desc(WordTemplate.id)).first()
if not template:
    print("No templates found")
    db.close()
    exit(1)

print(f"=== Template ID {template.id} ===\n")

# Get the fields_json
fields_json = json.loads(template.fields_json) if template.fields_json else []
print(f"Fields from fields_json ({len(fields_json)} fields):")
for idx, field_data in enumerate(fields_json):
    try:
        print(f"  {idx}: {json.dumps(field_data, ensure_ascii=False)}")
    except:
        print(f"  {idx}: (encoding error, skipping detail)")

print("\n=== Simulating GET /api/word/template/{template_id} ===\n")

# Simulate the endpoint logic
enriched_fields = []
form_id = 1
user_id = 1

for idx, field_data in enumerate(fields_json):
    field_name = field_data.get("name", "")
    field_label = field_data.get("label", field_name)
    field_type = field_data.get("field_type", "text")
    field_order = field_data.get("order", idx)
    
    # Tìm field trong database theo form_id + field_name
    db_field = db.query(Field).filter(
        Field.form_id == form_id,
        Field.field_name == field_name
    ).first()
    
    # Nếu không tồn tại, tự động tạo
    if not db_field:
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
            print(f"Auto-created field: {field_name} (id={db_field.id})")
        except Exception as e:
            print(f"Error creating field {field_name}: {str(e)}")
            db_field = None
    
    # Always use field_id from database
    field_id = db_field.id if db_field else -1
    
    enriched = {
        **field_data,
        "field_id": field_id,
        "field_index": idx,
    }
    enriched_fields.append(enriched)

print(f"\n=== Enriched Fields ===\n")
for field in enriched_fields:
    print(f"Field: {field}")
    print(f"  label={repr(field.get('label'))}")
    print(f"  field_id={field.get('field_id')}")
    print()

# Return as JSON (like the API would)
response = {
    "status": "success",
    "template_id": template.id,
    "template_name": template.template_name,
    "fields": enriched_fields,
    "user_id": user_id
}

print("\n=== API Response (JSON) ===\n")
print(json.dumps(response, indent=2, ensure_ascii=False))

db.close()
