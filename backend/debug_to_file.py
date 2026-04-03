#!/usr/bin/env python3
"""Write parser output to file"""
import sys
import json
sys.path.insert(0, '.')
from app.services.word_parser import WordParser

file_path = 'uploads/1_1771926182.710894_thu.docx'

parser = WordParser(file_path)
fields = parser.parse()

# Convert to dict for JSON
output = []
for field in fields:
    output.append({
        'label': field.label,
        'name': field.name,
        'has_quotes': '"' in field.label
    })

# Write to file
with open('parser_debug_output.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Wrote {len(output)} fields to parser_debug_output.json")
