"""
Smart Form Renderer - Render form với thế hiện bố cục của document
"""

import re
from typing import Dict, List, Optional
from .intelligent_detector import IntelligentDetector, ParsedForm, FormField


class SmartFormRenderer:
    """Render form từ parsed structure, giữ nguyên bố cục document"""

    @staticmethod
    def render_form_html(parsed_form: ParsedForm) -> str:
        """Render form HTML từ parsed document, giữ cấu trúc gốc"""
        html_parts = []

        html_parts.append('''
        <div class="form-container" style="font-family: Arial, sans-serif; max-width: 900px; margin: 20px auto; padding: 20px; background-color: #f9f9f9; border: 1px solid #ddd;">
        ''')

        # Group fields by section
        fields_by_section = {}
        for field in parsed_form.fields:
            section_idx = field.section_index
            if section_idx not in fields_by_section:
                fields_by_section[section_idx] = []
            fields_by_section[section_idx].append(field)

        # Render sections
        for section_idx, section in enumerate(parsed_form.sections):
            html_parts.append(SmartFormRenderer._render_section(
                section, fields_by_section.get(section_idx, [])
            ))

        html_parts.append('</div>')

        return '\n'.join(html_parts)

    @staticmethod
    def _render_section(section, fields: List[FormField]) -> str:
        """Render một section"""
        html_parts = []

        # Render section title nếu có
        if section.is_title and section.title:
            title_class = 'form-title-main' if section.level == 1 else 'form-title-sub'
            html_parts.append(f'''
            <div class="{title_class}" style="text-align: center; margin: 20px 0; font-weight: bold; font-size: {'24px' if section.level == 1 else '16px'}; text-transform: uppercase; letter-spacing: 1px;">
                {section.title}
            </div>
            ''')

        # Render items
        for item in section.items:
            if item['type'] == 'field':
                field_idx = item['field_index']
                if field_idx < len(fields):
                    field = fields[field_idx]
                    html_parts.append(SmartFormRenderer._render_field(field))
            else:  # text
                html_parts.append(SmartFormRenderer._render_text_item(item['text']))

        return '\n'.join(html_parts)

    @staticmethod
    def _render_field(field: FormField) -> str:
        """Render một field với input"""
        input_html = SmartFormRenderer._generate_input_html(
            field.field_name,
            field.label,
            field.field_type
        )

        # Format: "Label: [input]"
        html = f'''
        <div class="form-field" style="margin: 15px 0; display: flex; align-items: center;">
            <label for="{field.field_name}" style="min-width: 200px; font-weight: 500; margin-right: 15px;">
                {field.label}:
            </label>
            {input_html}
        </div>
        '''

        return html

    @staticmethod
    def _render_text_item(text: str) -> str:
        """Render text content line"""
        return f'''
        <div class="form-text" style="margin: 10px 0; line-height: 1.6; color: #333;">
            {text}
        </div>
        '''

    @staticmethod
    def _generate_input_html(field_name: str, label: str, field_type: str) -> str:
        """Generate HTML input element"""
        input_type = SmartFormRenderer._map_field_type_to_html(field_type)
        
        base_style = "padding: 8px 12px; border: 1px solid #999; border-radius: 4px; font-size: 14px; min-width: 300px;"

        if field_type == 'textarea':
            return f'''
            <textarea 
                id="{field_name}" 
                name="{field_name}" 
                placeholder="Nhập {label.lower()}..."
                style="{base_style} height: 100px; resize: vertical;"
                data-field-type="{field_type}"
                data-field-label="{label}"
            ></textarea>
            '''
        else:
            return f'''
            <input 
                type="{input_type}" 
                id="{field_name}" 
                name="{field_name}" 
                placeholder="Nhập {label.lower()}..."
                style="{base_style}"
                data-field-type="{field_type}"
                data-field-label="{label}"
            />
            '''

    @staticmethod
    def _map_field_type_to_html(field_type: str) -> str:
        """Map field type to HTML input type"""
        type_map = {
            'date': 'date',
            'phone': 'tel',
            'email': 'email',
            'number': 'number',
            'text': 'text',
            'textarea': 'textarea',
        }
        return type_map.get(field_type, 'text')

    @staticmethod
    def render_form_with_inline_replacement(raw_content: List[str], fields: List[FormField]) -> str:
        """Render form với replacement inline (giữ text gốc nhưng thay placeholder bằng input)"""
        html_parts = []

        html_parts.append('''
        <div class="form-document" style="font-family: 'Times New Roman', serif; max-width: 900px; margin: 20px auto; padding: 40px; background-color: white; line-height: 1.8;">
        ''')

        field_lines = {}  # Map line text to field
        for field in fields:
            field_lines[field.context] = field

        for line_idx, line in enumerate(raw_content):
            if line in field_lines:
                field = field_lines[line]
                modified_line = SmartFormRenderer._replace_placeholder_with_input(
                    line, field
                )
                html_parts.append(f'<p style="margin: 10px 0;">{modified_line}</p>')
            else:
                html_parts.append(f'<p style="margin: 10px 0;">{line}</p>')

        html_parts.append('</div>')

        return '\n'.join(html_parts)

    @staticmethod
    def _replace_placeholder_with_input(text: str, field: FormField) -> str:
        """Replace placeholder trong text bằng input element"""
        start, end = field.position_in_line

        # Lấy phần trước và sau placeholder
        before = text[:start]
        after = text[end:]

        input_html = SmartFormRenderer._generate_input_html(
            field.field_name,
            field.label,
            field.field_type
        ).strip()

        # Remove newlines từ input html
        input_html = re.sub(r'\s+', ' ', input_html)

        return f"{before}{input_html}{after}"


class DocumentStructurePreserver:
    """Preserve document structure khi render"""

    @staticmethod
    def render_structured_form(parsed_form: ParsedForm) -> str:
        """Render form structure giống document gốc"""
        renderer = SmartFormRenderer()
        return renderer.render_form_html(parsed_form)

    @staticmethod
    def render_with_original_layout(parsed_form: ParsedForm) -> str:
        """Render form với bố cục gốc (inline placeholder replacement)"""
        renderer = SmartFormRenderer()
        return renderer.render_form_with_inline_replacement(
            parsed_form.raw_content,
            parsed_form.fields
        )
