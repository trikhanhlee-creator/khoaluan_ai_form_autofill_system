"""
Form Layout Renderer - Render form giống hệt cấu trúc document
Phân biệt giữa tiêu đề (non-editable) và trường nhập liệu (editable)
"""

import re
from typing import List, Dict, Optional, Tuple
from .intelligent_detector import ParsedForm, FormField, FormSection


class FormLayoutRenderer:
    """Render form giữ nguyên layout document, phân biệt title vs fields"""

    @staticmethod
    def render_form_as_layout(parsed_form: ParsedForm) -> str:
        """
        Render form giống hệt document structure:
        - Tiêu đề: Text không editable
        - Trường: Input boxes trong vị trí tương ứng
        - Layout: Chính xác như document gốc
        """
        html_parts = []

        # Container với styling giống document
        html_parts.append('''
        <div class="form-layout-container" style="
            font-family: 'Times New Roman', serif;
            max-width: 900px;
            margin: 20px auto;
            padding: 40px;
            background-color: white;
            line-height: 1.8;
            color: #333;
        ">
        ''')

        # Build map of fields by line (để replace placeholder)
        field_by_context = {}
        for field in parsed_form.fields:
            field_by_context[field.context] = field

        # Render từng section
        for section_idx, section in enumerate(parsed_form.sections):
            if section.is_title:
                # Render title section
                html_parts.append(FormLayoutRenderer._render_title_section(section))
            else:
                # Render content section
                html_parts.append(FormLayoutRenderer._render_content_section(
                    section, parsed_form.fields, field_by_context
                ))

        html_parts.append('</div>')

        return '\n'.join(html_parts)

    @staticmethod
    def _render_title_section(section: FormSection) -> str:
        """Render title/header section (non-editable)"""
        html = ''

        if section.title:
            # Main title style
            if section.level == 1:
                html = f'''
                <div class="form-title-main" style="
                    text-align: center;
                    margin: 20px 0;
                    font-weight: bold;
                    font-size: 18px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                ">
                    {section.title}
                </div>
                '''
            else:
                html = f'''
                <div class="form-title-sub" style="
                    text-align: center;
                    margin: 15px 0;
                    font-weight: bold;
                    font-size: 14px;
                ">
                    {section.title}
                </div>
                '''

        # Render subtitle items (if any)
        for item in section.items:
            if item['type'] == 'text':
                html += f'''
                <div class="form-subtitle" style="
                    text-align: center;
                    margin: 10px 0;
                    font-size: 12px;
                ">
                    {item['text']}
                </div>
                '''

        return html

    @staticmethod
    def _render_content_section(section: FormSection, all_fields: List[FormField], 
                                field_by_context: Dict) -> str:
        """Render content section với fields"""
        html_parts = []

        for item in section.items:
            if item['type'] == 'text':
                # Regular text (non-editable)
                text = item['text']
                html_parts.append(f'''
                <div class="form-text" style="
                    margin: 10px 0;
                    line-height: 1.6;
                ">
                    {text}
                </div>
                ''')

            elif item['type'] == 'field':
                # Input field
                field_idx = item['field_index']
                if field_idx < len(all_fields):
                    field = all_fields[field_idx]
                    html_parts.append(
                        FormLayoutRenderer._render_field_row(field)
                    )

        return '\n'.join(html_parts)

    @staticmethod
    def _render_field_row(field: FormField) -> str:
        """Render một field row - label + input box"""
        
        # Label styling
        label_style = "display: inline-block; min-width: 150px; font-weight: 500; vertical-align: top;"
        
        # Input styling - giống boxes trong hình
        input_type = FormLayoutRenderer._map_field_type(field.field_type)
        
        if field.field_type == 'textarea':
            input_html = f'''
            <textarea 
                id="{field.field_name}" 
                name="{field.field_name}"
                style="
                    border: 1px solid #000;
                    width: 100%;
                    min-height: 60px;
                    padding: 8px;
                    font-family: 'Times New Roman', serif;
                    font-size: 13px;
                    box-sizing: border-box;
                    vertical-align: top;
                "
                placeholder="Nhập {field.label.lower()}..."
                data-field-label="{field.label}"
                data-field-type="{field.field_type}"
            ></textarea>
            '''
        else:
            # Single-line input
            input_html = f'''
            <input 
                type="{input_type}" 
                id="{field.field_name}" 
                name="{field.field_name}"
                style="
                    border: 1px solid #000;
                    padding: 6px 8px;
                    font-family: 'Times New Roman', serif;
                    font-size: 13px;
                    min-width: 250px;
                "
                placeholder="Nhập {field.label.lower()}..."
                data-field-label="{field.label}"
                data-field-type="{field.field_type}"
            />
            '''

        # Field row layout
        html = f'''
        <div class="form-field-row" style="
            margin: 15px 0;
            display: flex;
            gap: 15px;
            align-items: flex-start;
        ">
            <label for="{field.field_name}" style="{label_style}">
                {field.label}:
            </label>
            <div style="flex: 1;">
                {input_html}
            </div>
        </div>
        '''

        return html

    @staticmethod
    def _map_field_type(field_type: str) -> str:
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
    def render_form_document_style(parsed_form: ParsedForm) -> str:
        """
        Render form giống Word document style - boxes tương tự hình ảnh
        Phân biệt rõ ràng title vs fields
        """
        html_parts = []

        # Main container
        html_parts.append('''
        <div class="form-document-style" style="
            font-family: 'Arial', sans-serif;
            max-width: 1000px;
            margin: 20px auto;
            padding: 50px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        ">
        ''')

        # Group fields by section
        fields_by_section = {}
        for field in parsed_form.fields:
            section_idx = field.section_index
            if section_idx not in fields_by_section:
                fields_by_section[section_idx] = []
            fields_by_section[section_idx].append(field)

        # Process each section
        for section_idx, section in enumerate(parsed_form.sections):
            section_fields = fields_by_section.get(section_idx, [])

            if section.is_title and not section_fields:
                # Pure title section - no fields
                title_html = FormLayoutRenderer._render_document_title(section)
                html_parts.append(title_html)
            elif section.is_title and section_fields:
                # Section with both title and fields
                title_html = FormLayoutRenderer._render_document_title(section)
                html_parts.append(title_html)
                content_html = FormLayoutRenderer._render_document_content(
                    section, section_fields
                )
                html_parts.append(content_html)
            else:
                # Content section - with fields
                content_html = FormLayoutRenderer._render_document_content(
                    section, section_fields
                )
                html_parts.append(content_html)

        html_parts.append('</div>')

        return '\n'.join(html_parts)

    @staticmethod
    def _render_document_title(section: FormSection) -> str:
        """Render title section in document style"""
        html_parts = []

        if section.title:
            title_size = "22px" if section.level == 1 else "16px"
            html_parts.append(f'''
            <div style="
                text-align: center;
                margin-bottom: 30px;
                font-weight: bold;
                font-size: {title_size};
                text-transform: uppercase;
                letter-spacing: 0.5px;
                line-height: 1.4;
            ">
                {section.title}
            </div>
            ''')

        # Add subtitle items
        for item in section.items:
            if item['type'] == 'text':
                html_parts.append(f'''
                <div style="
                    text-align: center;
                    margin-bottom: 15px;
                    font-size: 12px;
                    font-style: italic;
                ">
                    {item['text']}
                </div>
                ''')

        return '\n'.join(html_parts)

    @staticmethod
    def _render_document_content(section: FormSection, fields: List[FormField]) -> str:
        """Render content section with form fields in document style"""
        html_parts = []

        # Create a map of field objects by their context for matching
        field_map = {field.context: field for field in fields}

        for item in section.items:
            if item['type'] == 'text':
                # Text content - regular paragraph
                html_parts.append(f'''
                <p style="
                    margin: 12px 0;
                    line-height: 1.6;
                    text-align: justify;
                    font-size: 13px;
                ">
                    {item['text']}
                </p>
                ''')

            elif item['type'] == 'field':
                # Find the field that matches this item
                field = None
                for f in fields:
                    if f.context == item['text']:
                        field = f
                        break
                
                if field:
                    field_html = FormLayoutRenderer._render_document_field(field)
                    html_parts.append(field_html)

        return '\n'.join(html_parts)

    @staticmethod
    def _render_document_field(field: FormField) -> str:
        """Render single field in document style (label: [box])"""
        
        input_type = FormLayoutRenderer._map_field_type(field.field_type)
        
        # Box styling - giống hình ảnh
        box_style = """
            border: 1.5px solid #000;
            display: inline-block;
            min-width: 200px;
            padding: 8px 10px;
            font-family: 'Arial', sans-serif;
            font-size: 12px;
            vertical-align: middle;
            background-color: #fff;
        """

        if field.field_type == 'textarea':
            input_html = f'''
            <textarea 
                id="{field.field_name}" 
                name="{field.field_name}"
                style="{box_style} width: calc(100% - 20px); min-height: 80px; vertical-align: top;"
                placeholder=""
                data-field-label="{field.label}"
                data-field-type="{field.field_type}"
            ></textarea>
            '''
        else:
            input_html = f'''
            <input 
                type="{input_type}" 
                id="{field.field_name}" 
                name="{field.field_name}"
                style="{box_style}"
                placeholder=""
                data-field-label="{field.label}"
                data-field-type="{field.field_type}"
            />
            '''

        # Full row with label and input
        html = f'''
        <div style="margin: 12px 0; line-height: 1.8;">
            <span style="font-weight: 500; margin-right: 8px;">{field.label}:</span>
            {input_html}
        </div>
        '''

        return html


class FormPageRenderer:
    """Render form as an interactive page"""

    @staticmethod
    def render_complete_form_page(parsed_form: ParsedForm) -> str:
        """Render complete form page with HTML, CSS, JS"""
        
        html = f'''
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Form</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Times New Roman', serif;
                    background-color: #f5f5f5;
                    padding: 20px;
                }}
                
                .form-page-wrapper {{
                    max-width: 900px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 40px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                
                .form-title {{
                    text-align: center;
                    font-weight: bold;
                    font-size: 18px;
                    margin: 20px 0;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                
                .form-subtitle {{
                    text-align: center;
                    font-size: 12px;
                    margin: 10px 0;
                }}
                
                .form-section {{
                    margin: 20px 0;
                }}
                
                .form-field-row {{
                    margin: 15px 0;
                    display: flex;
                    align-items: center;
                    gap: 15px;
                }}
                
                .form-field-label {{
                    font-weight: 500;
                    min-width: 160px;
                    font-size: 13px;
                }}
                
                .form-input {{
                    border: 1.5px solid #000;
                    padding: 8px 10px;
                    font-family: 'Times New Roman', serif;
                    font-size: 12px;
                    background-color: white;
                }}
                
                .form-input[type="text"],
                .form-input[type="tel"],
                .form-input[type="email"],
                .form-input[type="date"],
                .form-input[type="number"] {{
                    min-width: 250px;
                }}
                
                .form-input[type="textarea"],
                textarea {{
                    width: 100%;
                    min-height: 80px;
                    resize: vertical;
                }}
                
                .form-text {{
                    margin: 12px 0;
                    line-height: 1.6;
                    text-align: justify;
                    font-size: 13px;
                }}
                
                .form-button-group {{
                    margin: 30px 0;
                    text-align: center;
                }}
                
                button {{
                    padding: 10px 30px;
                    background-color: #0066cc;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                    margin: 0 5px;
                }}
                
                button:hover {{
                    background-color: #0052a3;
                }}
            </style>
        </head>
        <body>
            <div class="form-page-wrapper">
                {FormLayoutRenderer.render_form_document_style(parsed_form)}
                
                <div class="form-button-group">
                    <button type="submit" onclick="submitForm()">Gửi</button>
                    <button type="reset" onclick="resetForm()">Xóa</button>
                </div>
            </div>
            
            <script>
                function submitForm() {{
                    const formData = new FormData();
                    const inputs = document.querySelectorAll('[data-field-label]');
                    
                    inputs.forEach(input => {{
                        formData.append(input.name, input.value);
                    }});
                    
                    // Send to server
                    fetch('/api/form-replacement/submit-dotline-form', {{
                        method: 'POST',
                        body: formData
                    }})
                    .then(r => r.json())
                    .then(d => alert('Form submitted: ' + d.message))
                    .catch(e => alert('Error: ' + e));
                }}
                
                function resetForm() {{
                    document.querySelectorAll('[data-field-label]').forEach(input => {{
                        input.value = '';
                    }});
                }}
            </script>
        </body>
        </html>
        '''
        
        return html
