"""
Utility functions for file handling
"""

import re
from pathlib import Path


def extract_clean_filename(prefixed_filename: str) -> str:
    """
    Extract clean filename from prefixed format
    
    Pattern: {user_id}_{timestamp}_{original_filename}
    Example: 1_1772336043.37835_testapi.docx => testapi.docx
    
    Args:
        prefixed_filename: Filename with user_id and timestamp prefix
        
    Returns:
        Clean filename without prefix
    """
    # Pattern: user_id (digits) _ timestamp (digits.digits) _ rest
    # The filename starts after the second underscore following the timestamp
    
    # Try to match the prefix pattern: digit(s) + underscore + digit(s).digit(s) + underscore
    match = re.match(r'^\d+_\d+\.\d+_(.+)$', prefixed_filename)
    if match:
        return match.group(1)
    
    # If it doesn't match the pattern, return as-is (might already be clean)
    return prefixed_filename


def get_clean_filename_from_path(file_path: str) -> str:
    """
    Extract clean filename from a full file path and remove prefix
    
    Args:
        file_path: Full or relative file path
        
    Returns:
        Clean filename without path and prefix
    """
    # Extract just the filename from path
    filename = Path(file_path).name
    # Remove prefix if present
    return extract_clean_filename(filename)
