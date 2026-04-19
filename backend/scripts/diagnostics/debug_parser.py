#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from app.services.word_parser import WordParser
from docx import Document
import os

# Test with the actual uploaded file
file_path = 'uploads/5_1771924856.915534_test_user_form.docx'

print(f"=== PARSING {file_path} ===\n")

# Check raw paragraph text
doc = Document(file_path)
print("Raw paragraph texts:")
for idx, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    if text:
        print(f"  Para {idx}: {repr(text)}")

print("\n=== Using WordParser ===\n")

# Parse using WordParser
parser = WordParser(file_path)
fields = parser.parse()

print(f"Parsed {len(fields)} fields:")
for field in fields:
    print(f"  - name={repr(field.name)}")
    print(f'    label={repr(field.label)}')
    print(f"    to_dict()={field.to_dict()}")
    print()
