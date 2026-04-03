"""
Data Models cho Form Replacement Service
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class DotLineField:
    """Model cho một field được extract từ dot-line"""
    name: str  # Field name (snake_case)
    label: str  # Field label/prompt
    field_type: str  # text, number, email, phone, date
    order: int  # Order trong form
    has_prefix: bool = False  # Có text trước dot-line
    has_suffix: bool = False  # Có text sau dot-line
    dot_start_pos: int = 0  # Vị trí bắt đầu dot-line
    dot_end_pos: int = 0  # Vị trí kết thúc dot-line

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class FormReplacementResult:
    """Kết quả sau khi thay thế dot-lines"""
    status: str  # 'success' or 'error'
    fields_count: int  # Số fields tìm được
    fields: List[Dict]  # List fields
    html_form: Optional[str] = None  # HTML form render
    error: Optional[str] = None  # Error message nếu có

    def to_dict(self) -> Dict:
        return {
            'status': self.status,
            'fields_count': self.fields_count,
            'fields': self.fields,
            'html_form': self.html_form,
            'error': self.error
        }
