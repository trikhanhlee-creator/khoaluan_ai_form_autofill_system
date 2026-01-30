from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    forms = relationship("Form", back_populates="user", cascade="all, delete-orphan")
    entries = relationship("Entry", back_populates="user", cascade="all, delete-orphan")
    suggestions = relationship("Suggestion", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Form(Base):
    __tablename__ = "forms"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    form_name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="forms")
    fields = relationship("Field", back_populates="form", cascade="all, delete-orphan")
    entries = relationship("Entry", back_populates="form", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Form(id={self.id}, form_name={self.form_name})>"


class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    form_id = Column(Integer, ForeignKey("forms.id", ondelete="CASCADE"), nullable=False)
    field_name = Column(String(255), nullable=False)
    field_type = Column(String(50))
    display_order = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    form = relationship("Form", back_populates="fields")
    entries = relationship("Entry", back_populates="field", cascade="all, delete-orphan")
    suggestions = relationship("Suggestion", back_populates="field", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Field(id={self.id}, field_name={self.field_name})>"


class Entry(Base):
    """Lịch sử nhập dữ liệu"""
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    field_id = Column(Integer, ForeignKey("fields.id", ondelete="CASCADE"), nullable=False)
    form_id = Column(Integer, ForeignKey("forms.id", ondelete="CASCADE"), nullable=False)
    value = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="entries")
    field = relationship("Field", back_populates="entries")
    form = relationship("Form", back_populates="entries")

    def __repr__(self):
        return f"<Entry(id={self.id}, field_id={self.field_id}, value={self.value})>"


class Suggestion(Base):
    """Bảng cache cho gợi ý"""
    __tablename__ = "suggestions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    field_id = Column(Integer, ForeignKey("fields.id", ondelete="CASCADE"), nullable=False)
    suggested_value = Column(String(1000), nullable=False)
    frequency = Column(Integer, default=1)
    ranking = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="suggestions")
    field = relationship("Field", back_populates="suggestions")

    def __repr__(self):
        return f"<Suggestion(id={self.id}, value={self.suggested_value}, frequency={self.frequency})>"


class WordTemplate(Base):
    """Template từ file Word được upload"""
    __tablename__ = "word_templates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    template_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    original_filename = Column(String(255), nullable=False)
    fields_json = Column(Text)  # JSON string of fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User")
    submissions = relationship("WordSubmission", back_populates="template", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<WordTemplate(id={self.id}, template_name={self.template_name})>"


class WordSubmission(Base):
    """Lịch sử submit form từ template Word"""
    __tablename__ = "word_submissions"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("word_templates.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    submission_data = Column(Text)  # JSON string of submitted data
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    template = relationship("WordTemplate", back_populates="submissions")
    user = relationship("User")

    def __repr__(self):
        return f"<WordSubmission(id={self.id}, template_id={self.template_id})>"
