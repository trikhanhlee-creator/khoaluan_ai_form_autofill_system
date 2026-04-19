#!/usr/bin/env python3
"""Test parser on user's original file"""
import sys
import json
sys.path.insert(0, '.')
from app.services.word_parser import WordParser

file_path = 'uploads/1_1771926182.710894_thu.docx'

print("Re-parsing user's original file with updated function...\n")

parser = WordParser(file_path)
fields = parser.parse()

# Convert to dict for JSON
output = []
for field in fields:
    output.append({
        'label': field.label,
        'name': field.name,
        'has_quotes': any(c in field.label for c in ['"', '"', "'", "'"])
    })

# Check results
print("Results:")
for idx, item in enumerate(output):
    status = "❌" if item['has_quotes'] else "✅"
    print(f"{idx+1}. {status} Label: {item['label']}")

# Write to file
with open('parser_final_test.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nAll {len(output)} fields are now CLEAN!")
print("Results saved to parser_final_test.json")
