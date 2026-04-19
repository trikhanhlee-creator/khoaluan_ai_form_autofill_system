#!/usr/bin/env python3
"""Test clean_field_label on the exact problematic text"""
import sys
import re
sys.path.insert(0, '.')
from app.services.word_parser import WordParser

# Create parser instance (without file requirement)
parser = WordParser.__new__(WordParser)

# Test cases
test_cases = [
    'Địa chỉ"""',  # 3 quotes
    'Địa chỉ""',   # 2 quotes  
    'Địa chỉ"',    # 1 quote
    'Lớp ',         # trailing space
    'Trường(...)',  # parentheses
]

print("Testing clean_field_label():\n")
for text in test_cases:
    cleaned = parser.clean_field_label(text)
    status = "FAIL" if '"' in cleaned else "OK"
    print(f"[{status}] Input:  {repr(text)}")
    print(f"     Output: {repr(cleaned)}")
    print()

# Write the result to a file
with open('clean_label_test.txt', 'w', encoding='utf-8') as f:
    for text in test_cases:
        cleaned = parser.clean_field_label(text)
        has_quotes = '"' in cleaned
        f.write(f"Input: {text}\n")
        f.write(f"Output: {cleaned}\n")
        f.write(f"Has quotes: {has_quotes}\n\n")

print("Results written to clean_label_test.txt")
