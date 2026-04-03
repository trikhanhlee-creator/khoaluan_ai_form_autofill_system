#!/usr/bin/env python3
"""Debug parser - simple version"""
import sys
sys.path.insert(0, '.')
from app.services.word_parser import WordParser

# Use the user's actual file
file_path = 'uploads/1_1771926182.710894_thu.docx'

print("Testing WordParser on user's file...")
print()

parser = WordParser(file_path)
fields = parser.parse()

print(f"Parsed {len(fields)} fields:\n")
for idx, field in enumerate(fields):
    has_quotes = '"' in field.label
    status = "ERROR" if has_quotes else "OK"
    print(f"{idx+1}. [{status}] Label: {field.label}")
    print(f"   Name: {field.name}")
    print()
