"""
Form Replacement Service
Xác định các trường bằng dot-lines và thay thế bằng input fields
Nâng cấp: Phát hiện tiêu đề, label thông minh, tổ chức theo section
"""

from .dot_line_detector import DotLineDetector, DotLinePlaceholder
from .field_replacer import HTMLFieldReplacer, DocxFieldReplacer
from .models import DotLineField, FormReplacementResult
from .intelligent_detector import IntelligentDetector, FormSection, FormField, ParsedForm
from .smart_form_renderer import SmartFormRenderer, DocumentStructurePreserver
from .form_layout_renderer import FormLayoutRenderer, FormPageRenderer

__all__ = [
    # Old API
    'DotLineDetector',
    'DotLinePlaceholder',
    'HTMLFieldReplacer',
    'DocxFieldReplacer',
    'DotLineField',
    'FormReplacementResult',
    # New API
    'IntelligentDetector',
    'FormSection',
    'FormField',
    'ParsedForm',
    'SmartFormRenderer',
    'DocumentStructurePreserver',
    # Layout API
    'FormLayoutRenderer',
    'FormPageRenderer'
]
