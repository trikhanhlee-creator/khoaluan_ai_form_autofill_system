"""
API Routes cho xử lý upload và submit form từ file Word
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from fastapi.requests import Request
from sqlalchemy.orm import Session
from typing import List, Dict
import os
import json
from datetime import datetime
import shutil

from app.db.session import get_db
from app.db.models import WordTemplate, WordSubmission, Entry, Field, Suggestion
from app.services.word_parser import WordParser
from sqlalchemy import func

router = APIRouter(prefix="/api/word", tags=["word"])

# Thư mục lưu file upload
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@router.post("/upload")
async def upload_word_template(
    file: UploadFile = File(...),
    user_id: int = Query(1),
    db: Session = Depends(get_db)
):
    """Upload file Word và parse thành template"""
    
    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file .docx")
    
    try:
        # Lưu file
        file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{datetime.now().timestamp()}_{file.filename}")
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Parse file
        parser = WordParser(file_path)
        fields = parser.parse()
        metadata = parser.get_metadata()
        
        if not fields:
            raise HTTPException(status_code=400, detail="Không tìm thấy trường trong file Word")
        
        # Lưu template vào database
        template = WordTemplate(
            user_id=user_id,
            template_name=metadata.get("title", file.filename),
            file_path=file_path,
            original_filename=file.filename,
            fields_json=json.dumps([f.to_dict() for f in fields])
        )
        db.add(template)
        db.commit()
        db.refresh(template)
        
        return {
            "status": "success",
            "template_id": template.id,
            "template_name": template.template_name,
            "fields_count": len(fields),
            "fields": [f.to_dict() for f in fields],
            "message": "Upload và parse thành công"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@router.get("/templates")
async def get_user_templates(
    user_id: int = Query(1),
    db: Session = Depends(get_db)
):
    """Lấy danh sách template của user"""
    
    templates = db.query(WordTemplate).filter(WordTemplate.user_id == user_id).all()
    
    return {
        "templates": [
            {
                "id": t.id,
                "name": t.template_name,
                "filename": t.original_filename,
                "fields_count": len(json.loads(t.fields_json)) if t.fields_json else 0,
                "created_at": t.created_at.isoformat(),
                "submissions_count": len(t.submissions)
            }
            for t in templates
        ]
    }


@router.get("/template/{template_id}")
async def get_template_detail(
    template_id: int,
    db: Session = Depends(get_db)
):
    """Lấy chi tiết template"""
    
    template = db.query(WordTemplate).filter(WordTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template không tồn tại")
    
    fields_json = json.loads(template.fields_json) if template.fields_json else []
    
    # Lấy form_id từ entries (nếu có submission)
    form_id = 1  # Default
    entries = db.query(Entry).filter(Entry.user_id == template.user_id).first()
    if entries:
        form_id = entries.form_id
    
    # Enrich fields với database field IDs
    enriched_fields = []
    for idx, field_data in enumerate(fields_json):
        field_name = field_data.get("name", "")
        # Try to find existing field in database
        db_field = db.query(Field).filter(
            Field.form_id == form_id,
            Field.field_name == field_name
        ).first()
        
        enriched_fields.append({
            **field_data,
            "field_id": db_field.id if db_field else None,
            "field_index": idx
        })
    
    return {
        "id": template.id,
        "name": template.template_name,
        "filename": template.original_filename,
        "fields": enriched_fields,
        "form_id": form_id,
        "created_at": template.created_at.isoformat(),
        "submissions_count": len(template.submissions)
    }


@router.post("/submit")
async def submit_form(
    template_id: int = Query(...),
    user_id: int = Query(1),
    form_id: int = Query(1),
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Submit form data cho template"""
    from app.core.logger import logger
    
    logger.info(f"submit_form called: template_id={template_id}, user_id={user_id}, form_id={form_id}")
    
    template = db.query(WordTemplate).filter(WordTemplate.id == template_id).first()
    if not template:
        logger.error(f"Template {template_id} not found")
        raise HTTPException(status_code=404, detail="Template không tồn tại")
    
    # Get JSON data from request body
    try:
        data = await request.json() if request else {}
    except:
        data = {}
    
    logger.info(f"Received form data: {data}")
    
    # Lưu submission
    submission = WordSubmission(
        template_id=template_id,
        user_id=user_id,
        submission_data=json.dumps(data or {})
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    
    logger.info(f"Submission saved: {submission.id}")
    
    # Lưu entries và tạo suggestions cho suggestions system
    try:
        fields_json = json.loads(template.fields_json) if template.fields_json else []
        logger.info(f"Template has {len(fields_json)} fields")
        
        for field_data in fields_json:
            field_name = field_data.get("name", "")
            logger.info(f"Processing field: {field_name}")
            
            # Lấy giá trị từ form submit
            value = data.get(field_name, "").strip()
            if not value:
                logger.info(f"  Field {field_name} has no value, skipping")
                continue
            
            logger.info(f"  Field {field_name} value: '{value}'")
            
            # Tìm hoặc tạo Field
            field = db.query(Field).filter(
                Field.form_id == form_id,
                Field.field_name == field_name
            ).first()
            
            if not field:
                # Auto-create field nếu không tồn tại
                logger.info(f"  Creating new field: {field_name}")
                field = Field(
                    form_id=form_id,
                    field_name=field_name,
                    field_type=field_data.get("field_type", "text"),
                    display_order=field_data.get("order", 0)
                )
                db.add(field)
                db.commit()
                db.refresh(field)
                logger.info(f"  Field created with id: {field.id}")
            else:
                logger.info(f"  Field found with id: {field.id}")
            
            # Lưu entry
            entry = Entry(
                user_id=user_id,
                field_id=field.id,
                form_id=form_id,
                value=value
            )
            db.add(entry)
            db.commit()
            logger.info(f"  Entry saved: id={entry.id}, value='{value}'")
            
            # Tạo suggestion nếu có 2+ entries với cùng giá trị
            entry_count = db.query(func.count(Entry.id)).filter(
                Entry.user_id == user_id,
                Entry.field_id == field.id,
                Entry.value == value
            ).scalar()
            
            logger.info(f"  Entry count for value '{value}': {entry_count}")
            
            if entry_count >= 2:
                # Kiểm tra suggestion đã tồn tại chưa
                suggestion = db.query(Suggestion).filter(
                    Suggestion.user_id == user_id,
                    Suggestion.field_id == field.id,
                    Suggestion.suggested_value == value
                ).first()
                
                if suggestion:
                    # Update frequency
                    suggestion.frequency = entry_count
                    suggestion.ranking = entry_count
                    logger.info(f"  Updated suggestion: frequency={entry_count}")
                else:
                    # Tạo suggestion mới
                    suggestion = Suggestion(
                        user_id=user_id,
                        field_id=field.id,
                        suggested_value=value,
                        frequency=entry_count,
                        ranking=entry_count
                    )
                    db.add(suggestion)
                    logger.info(f"  Created new suggestion: frequency={entry_count}")
                
                db.commit()
    
    except Exception as e:
        logger.error(f"Error saving entries/suggestions: {str(e)}", exc_info=True)
        # Không throw error, vẫn trả về success vì submission đã lưu
    
    logger.info(f"Submit completed for submission {submission.id}")
    return {
        "status": "success",
        "submission_id": submission.id,
        "message": "Submit thành công"
    }


@router.get("/submissions")
async def get_submissions(
    template_id: int = Query(None),
    user_id: int = Query(1),
    db: Session = Depends(get_db)
):
    """Lấy danh sách submission"""
    
    query = db.query(WordSubmission).filter(WordSubmission.user_id == user_id)
    
    if template_id:
        query = query.filter(WordSubmission.template_id == template_id)
    
    submissions = query.all()
    
    return {
        "submissions": [
            {
                "id": s.id,
                "template_id": s.template_id,
                "template_name": s.template.template_name,
                "data": json.loads(s.submission_data) if s.submission_data else {},
                "created_at": s.created_at.isoformat()
            }
            for s in submissions
        ]
    }


@router.get("/submission/{submission_id}")
async def get_submission_detail(
    submission_id: int,
    db: Session = Depends(get_db)
):
    """Lấy chi tiết một submission"""
    
    submission = db.query(WordSubmission).filter(WordSubmission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission không tồn tại")
    
    return {
        "id": submission.id,
        "template_id": submission.template_id,
        "template_name": submission.template.template_name,
        "data": json.loads(submission.submission_data) if submission.submission_data else {},
        "created_at": submission.created_at.isoformat()
    }


@router.delete("/template/{template_id}")
async def delete_template(
    template_id: int,
    user_id: int = Query(1),
    db: Session = Depends(get_db)
):
    """Xóa template"""
    
    template = db.query(WordTemplate).filter(
        WordTemplate.id == template_id,
        WordTemplate.user_id == user_id
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template không tồn tại")
    
    # Xóa file
    if os.path.exists(template.file_path):
        os.remove(template.file_path)
    
    # Xóa record
    db.delete(template)
    db.commit()
    
    return {"status": "success", "message": "Xóa template thành công"}
