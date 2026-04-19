#!/usr/bin/env python3
import re

# Test the clean_field_label logic
test_cases = [
    'Địa chỉ""',
    'Địa chỉ."',
    'Lớp"',
    "Trường'''",
    "Địa chỉ.",
]

pattern = r'[\s.:\,;!)\]\}»"\'─\-_*~`(]+$'

print("Testing clean_field_label regex:")
for text in test_cases:
    cleaned = re.sub(pattern, '', text)
    print(f'Input: {repr(text):30} -> Output: {repr(cleaned)}')

# Now test the full clean_field_label function from word_parser
import sys
sys.path.insert(0, '.')
from app.services.word_parser import WordParser

parser = WordParser.__new__(WordParser)  # Create instance without __init__
print("\nUsing actual clean_field_label method:")
for text in test_cases:
    cleaned = parser.clean_field_label(text)
    print(f'Input: {repr(text):30} -> Output: {repr(cleaned)}')
