#!/usr/bin/env python3
"""
Setup database cho Word Upload feature
"""

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[2]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.db.session import engine, Base
from app.db.models import WordTemplate, WordSubmission

print("🔧 Creating Word tables...")
Base.metadata.create_all(bind=engine)
print("✅ Word tables created successfully!")

print("\n📊 Tables in database:")
print("✅ word_templates - Lưu template từ file Word")
print("✅ word_submissions - Lưu dữ liệu submit form")
print("✅ Tất cả tables được tạo thành công!")
