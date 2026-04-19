#!/usr/bin/env python3
"""Test the updated clean_field_label with Unicode quotes"""
import sys
sys.path.insert(0, '.')
from app.services.word_parser import WordParser

parser = WordParser.__new__(WordParser)

# Test with both ASCII and Unicode quotes
test_cases = [
    ('Địa chỉ""', 'ASCII quotes'),  # Regular quotes (char 34)
    ('Địa chỉ""', 'Unicode smart quotes (8221)'),  # Unicode right double quotes
    ('Địa chỉ""', 'Mixed quotes'),  # Left and right smart quotes
    ('Địa chỉ\'\'', 'Unicode single quotes'),  # Unicode single quotes
]

print("Testing updated clean_field_label():\n")

# Also test with actual char codes 8221
actual_smart_quote_text = 'Địa chỉ' + chr(8221) + chr(8221)  # Actual Unicode char 8221
test_cases.append((actual_smart_quote_text, f'Actual Unicode 8221: {repr(actual_smart_quote_text)}'))

for text, description in test_cases:
    cleaned = parser.clean_field_label(text)
    has_quotes = '"' in cleaned or '"' in cleaned or "'" in cleaned or "'" in cleaned
    has_any_quotes = any(c in cleaned for c in ['"', '"', "'", "'"])
    
    status = "FAIL" if has_any_quotes else "OK"
    print(f"[{status}] {description}")
    print(f"    Input:  {repr(text)}")
    print(f"    Output: {repr(cleaned)}")
    print()

# Save to file
with open('unicode_quote_test.txt', 'w', encoding='utf-8') as f:
    for text, description in test_cases:
        cleaned = parser.clean_field_label(text)
        f.write(f"{description}\n")
        f.write(f"  Input:  {repr(text)}\n")
        f.write(f"  Output: {repr(cleaned)}\n\n")

print("Results written to unicode_quote_test.txt")
