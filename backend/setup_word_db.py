#!/usr/bin/env python3
"""
Setup database cho Word Upload feature
"""

import sys
sys.path.insert(0, '.')

from app.db.session import engine, Base
from app.db.models import WordTemplate, WordSubmission

print("🔧 Creating Word tables...")
Base.metadata.create_all(bind=engine)
print("✅ Word tables created successfully!")

print("\n📊 Tables in database:")
print("✅ word_templates - Lưu template từ file Word")
print("✅ word_submissions - Lưu dữ liệu submit form")
print("✅ Tất cả tables được tạo thành công!")
