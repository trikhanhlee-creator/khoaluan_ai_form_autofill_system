"""
Word Document Parser - Trích xuất fields từ file Word
Deprecated: Hãy dùng file_parser.py thay thế cho hỗ trợ nhiều định dạng

Lớp này được giữ lại cho backward compatibility.
Nó sử dụng FileParserFactory nội bộ để hỗ trợ tất cả định dạng file.
"""

from app.services.file_parser import FileParserFactory, FileField


# Backward compatibility - WordField class
class WordField(FileField):
    """Model cho một field từ file Word (backward compatibility)"""
    pass


class WordParser:
    """Parser để trích xuất fields từ file Word (.docx)
    
    Note: Lớp này hiện sử dụng FileParserFactory để hỗ trợ tất cả định dạng.
    Được giữ lại cho backward compatibility.
    """
    
    FIELD_TYPE_KEYWORDS = {
        'năm': 'number',
        'ngày': 'date',
        'điện thoại': 'phone',
        'email': 'email',
        'địa chỉ': 'text',
        'tên': 'text',
        'họ': 'text',
        'số': 'number',
        'năm sinh': 'number',
    }
    
    def __init__(self, file_path: str):
        # Dùng FileParserFactory để tạo parser phù hợp
        self.file_path = file_path
        self.parser = FileParserFactory.create_parser(file_path)
        self.fields = []
    
    def parse(self):
        """Parse file và trích xuất fields"""
        fields = self.parser.parse()
        # Convert FileField to WordField for backward compatibility
        self.fields = [WordField(
            name=f.name,
            field_type=f.field_type,
            label=f.label,
            order=f.order
        ) for f in fields]
        return self.fields
    
    def to_dict_list(self):
        """Chuyển fields thành list dict"""
        return [field.to_dict() for field in self.fields]
    
    def get_metadata(self):
        """Lấy metadata của file"""
        return self.parser.get_metadata()
if __name__ == "__main__":
    parser = WordParser('C:\\Users\\KHANH\\Downloads\\testform.docx')
    fields = parser.parse()
    
    print("=== PARSED FIELDS ===")
    for field in fields:
        print(f"- {field.label} ({field.name}): {field.field_type}")
    
    print("\n=== METADATA ===")
    print(parser.get_metadata())
