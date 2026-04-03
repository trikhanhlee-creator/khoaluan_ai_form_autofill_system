"""
API Routes cho xử lý upload và submit form từ file Word/Document
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from fastapi.requests import Request
from sqlalchemy.orm import Session
from sqlalchemy import text, inspect
from typing import List, Dict
import os
import json
from datetime import datetime

from app.db.session import get_db
from app.db.models import WordTemplate, WordSubmission, Entry, Field, User, Form
from app.services.file_parser import FileParserFactory, FileField
from app.core.logger import logger
from app.core.file_utils import extract_clean_filename
from app.core.auth import get_current_user
import re

router = APIRouter(prefix="/api/word", tags=["word"])

# Thư mục lưu file upload
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


def _sanitize_field_label(text: str) -> str:
    """Normalize legacy label text into a clean display label."""
    value = (text or "").strip()
    value = re.sub(r'\s*([\.:,;\-_()\[\]{}])+\s*$', '', value)
    return value.strip()


def _to_field_name(label: str) -> str:
    """Create a snake_case field name from any label string."""
    value = (label or "").lower().strip()
    value = re.sub(r'[^\w\s]', ' ', value)
    value = re.sub(r'\s+', '_', value).strip('_')
    return value or "field"


def parse_template_fields(fields_json_raw: str | None) -> list[dict]:
    """Parse template fields_json and normalize legacy formats.

    Supported legacy formats:
    - list[dict] (current format)
    - list[str] (older placeholder-only format)
    - dict (single field)
    """
    if not fields_json_raw:
        return []

    try:
        payload = json.loads(fields_json_raw)
    except Exception:
        return []

    if isinstance(payload, dict):
        payload = [payload]
    if not isinstance(payload, list):
        return []

    normalized: list[dict] = []
    for idx, item in enumerate(payload):
        if isinstance(item, dict):
            raw_label = item.get("label") or item.get("name") or f"Field {idx + 1}"
            label = _sanitize_field_label(str(raw_label)) or f"Field {idx + 1}"
            name = item.get("name") or _to_field_name(label)
            field_type = item.get("field_type") or "text"
            order = item.get("order", idx)
        elif isinstance(item, str):
            label = _sanitize_field_label(item) or f"Field {idx + 1}"
            name = _to_field_name(label)
            field_type = "text"
            order = idx
        else:
            continue

        normalized.append({
            "name": str(name),
            "label": str(label),
            "field_type": str(field_type),
            "order": int(order) if isinstance(order, (int, float)) else idx
        })

    return normalized


def get_or_create_word_form_id(db: Session, user_id: int) -> int:
    """Get user-specific word form_id (create once if missing).

    Uses raw SQL with dynamic columns for compatibility with legacy schemas
    where ORM model columns may not exist yet.
    """
    try:
        ensure_forms_schema_compatibility(db)
    except Exception as schema_error:
        # Continue with dynamic SQL fallback even if ALTER TABLE is not permitted.
        logger.warning(f"Schema compatibility patch failed, using fallback form resolver: {schema_error}")

    bind = db.get_bind()
    inspector = inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("forms")}

    select_sql = "SELECT id FROM forms WHERE user_id = :user_id"
    if "form_type" in columns:
        select_sql += " AND form_type = 'word'"
    select_sql += " ORDER BY id ASC LIMIT 1"

    row = db.execute(text(select_sql), {"user_id": user_id}).first()
    if row:
        return int(row[0])

    insert_columns: list[str] = ["user_id", "form_name"]
    insert_values_sql: list[str] = [":user_id", ":form_name"]
    params: dict[str, object] = {
        "user_id": user_id,
        "form_name": "Word Smart Form",
    }

    if "description" in columns:
        insert_columns.append("description")
        insert_values_sql.append(":description")
        params["description"] = "System form for Word template field mapping"
    if "form_type" in columns:
        insert_columns.append("form_type")
        insert_values_sql.append(":form_type")
        params["form_type"] = "word"
    if "is_template" in columns:
        insert_columns.append("is_template")
        insert_values_sql.append(":is_template")
        params["is_template"] = 1
    if "created_at" in columns:
        insert_columns.append("created_at")
        insert_values_sql.append("CURRENT_TIMESTAMP")
    if "updated_at" in columns:
        insert_columns.append("updated_at")
        insert_values_sql.append("CURRENT_TIMESTAMP")

    insert_sql = (
        f"INSERT INTO forms ({', '.join(insert_columns)}) "
        f"VALUES ({', '.join(insert_values_sql)})"
    )

    result = db.execute(text(insert_sql), params)
    db.commit()

    if result.lastrowid:
        return int(result.lastrowid)

    row = db.execute(text(select_sql), {"user_id": user_id}).first()
    if not row:
        raise HTTPException(status_code=500, detail="Không thể tạo form Word cho người dùng")
    return int(row[0])


def ensure_forms_schema_compatibility(db: Session) -> None:
    """Best-effort runtime compatibility for legacy forms table schema."""
    bind = db.get_bind()
    inspector = inspect(bind)

    if not inspector.has_table("forms"):
        # In case schema bootstrap was incomplete in some environments.
        Form.__table__.create(bind=bind, checkfirst=True)
        return

    try:
        existing_columns = {col["name"] for col in inspector.get_columns("forms")}
    except Exception as schema_error:
        logger.error(f"Unable to inspect forms table schema: {schema_error}")
        raise

    required_columns: dict[str, str] = {
        "description": "TEXT NULL",
        "form_type": "VARCHAR(50) NOT NULL DEFAULT 'standard'",
        "is_template": "BOOLEAN NOT NULL DEFAULT 0",
        "updated_at": "DATETIME NULL",
    }

    missing_columns = [name for name in required_columns if name not in existing_columns]
    if not missing_columns:
        return

    try:
        for col_name in missing_columns:
            ddl = required_columns[col_name]
            db.execute(text(f"ALTER TABLE forms ADD COLUMN {col_name} {ddl}"))

        # Backfill timestamps for legacy rows when column is newly added.
        if "updated_at" in missing_columns and "created_at" in existing_columns:
            db.execute(text("UPDATE forms SET updated_at = created_at WHERE updated_at IS NULL"))

        # Backfill defaults for old rows where these columns were absent.
        if "form_type" in missing_columns:
            db.execute(text("UPDATE forms SET form_type = 'standard' WHERE form_type IS NULL OR form_type = ''"))
        if "is_template" in missing_columns:
            db.execute(text("UPDATE forms SET is_template = 0 WHERE is_template IS NULL"))

        db.commit()
        logger.info(f"Patched legacy forms schema, added columns: {', '.join(missing_columns)}")
    except Exception as alter_error:
        db.rollback()
        alter_message = str(alter_error).lower()
        # Another worker/request may have added columns concurrently.
        if "duplicate column" in alter_message or "already exists" in alter_message:
            inspector = inspect(bind)
            refreshed_columns = {col["name"] for col in inspector.get_columns("forms")}
            still_missing = [name for name in required_columns if name not in refreshed_columns]
            if not still_missing:
                return
        logger.error(f"Failed to patch forms schema: {alter_error}")
        raise


def ensure_template_fields_exist(db: Session, form_id: int, fields_json: list[dict]) -> dict[str, int]:
    """Ensure template fields exist and return mapping by field_name -> field_id.

    Uses dynamic SQL to stay compatible with legacy `fields` table schemas.
    """
    bind = db.get_bind()
    inspector = inspect(bind)

    if not inspector.has_table("fields"):
        Field.__table__.create(bind=bind, checkfirst=True)

    columns = {col["name"] for col in inspector.get_columns("fields")}

    select_sql = "SELECT id, field_name FROM fields WHERE form_id = :form_id"
    existing_rows = db.execute(text(select_sql), {"form_id": form_id}).all()
    field_by_name: dict[str, int] = {str(row[1]): int(row[0]) for row in existing_rows if row[1]}

    created_any = False
    for idx, field_data in enumerate(fields_json):
        field_name = (field_data.get("name") or "").strip()
        if not field_name or field_name in field_by_name:
            continue

        insert_columns: list[str] = ["form_id", "field_name"]
        insert_values_sql: list[str] = [":form_id", ":field_name"]
        params: dict[str, object] = {
            "form_id": form_id,
            "field_name": field_name,
        }

        if "field_type" in columns:
            insert_columns.append("field_type")
            insert_values_sql.append(":field_type")
            params["field_type"] = field_data.get("field_type", "text")
        if "display_order" in columns:
            insert_columns.append("display_order")
            insert_values_sql.append(":display_order")
            params["display_order"] = field_data.get("order", idx)
        if "is_required" in columns:
            insert_columns.append("is_required")
            insert_values_sql.append(":is_required")
            params["is_required"] = 0
        if "validation_rules" in columns:
            insert_columns.append("validation_rules")
            insert_values_sql.append(":validation_rules")
            params["validation_rules"] = None
        if "placeholder" in columns:
            insert_columns.append("placeholder")
            insert_values_sql.append(":placeholder")
            params["placeholder"] = field_data.get("label", field_name)
        if "created_at" in columns:
            insert_columns.append("created_at")
            insert_values_sql.append("CURRENT_TIMESTAMP")

        insert_sql = (
            f"INSERT INTO fields ({', '.join(insert_columns)}) "
            f"VALUES ({', '.join(insert_values_sql)})"
        )
        result = db.execute(text(insert_sql), params)
        created_any = True

        if result.lastrowid:
            field_by_name[field_name] = int(result.lastrowid)

    if created_any:
        db.commit()

    # Fill any unresolved IDs (e.g. driver did not return lastrowid)
    if any(name not in field_by_name for name in [f.get("name", "") for f in fields_json if f.get("name")]):
        refreshed_rows = db.execute(text(select_sql), {"form_id": form_id}).all()
        refreshed_map = {str(row[1]): int(row[0]) for row in refreshed_rows if row[1]}
        field_by_name.update(refreshed_map)

    return field_by_name


def resolve_effective_user_id(current_user: User, requested_user_id: int | None) -> int:
    """Resolve target user scope. Non-admin users can only access their own data."""
    if requested_user_id is None:
        return current_user.id

    if requested_user_id <= 0:
        raise HTTPException(status_code=400, detail="user_id phải là số dương")

    if not current_user.is_admin and requested_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền truy cập dữ liệu của người dùng khác")

    return requested_user_id


@router.post("/upload")
async def upload_word_template(
    file: UploadFile = File(...),
    user_id: int | None = Query(None, description="ID của user (optional, admin only)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload file (Word, PDF, Excel, CSV, Text) và parse thành template
    
    Hỗ trợ các định dạng:
    - .docx (Word Document)
    - .pdf (PDF File)
    - .xlsx, .xls (Excel File)
    - .csv (CSV File)
    - .txt (Text File)
    """
    
    # Kiểm tra file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if not FileParserFactory.is_supported(file.filename):
        supported = ', '.join(FileParserFactory.get_supported_extensions())
        raise HTTPException(
            status_code=400, 
            detail=f"Không hỗ trợ định dạng file: {file_ext}. Các định dạng được hỗ trợ: {supported}"
        )
    
    try:
        effective_user_id = resolve_effective_user_id(current_user, user_id)

        # Lưu file
        file_path = os.path.join(UPLOAD_DIR, f"{effective_user_id}_{datetime.now().timestamp()}_{file.filename}")
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Parse file bằng parser phù hợp
        parser = FileParserFactory.create_parser(file_path)
        fields = parser.parse()
        metadata = parser.get_metadata()
        
        # Nếu vẫn không tìm được field nào, tạo một default field từ tên file
        if not fields:
            # Tạo field tạm thời dựa trên tên file
            default_field_name = os.path.splitext(file.filename)[0]
            fields = [FileField(
                name=default_field_name.lower().replace(' ', '_'),
                field_type="text",
                label=f"Nội dung từ {file.filename}",
                order=0
            )]
        
        # Lưu template vào database
        template = WordTemplate(
            user_id=effective_user_id,
            template_name=metadata.get("title", file.filename),
            file_path=file_path,
            original_filename=file.filename,
            fields_json=json.dumps([f.to_dict() for f in fields])
        )
        db.add(template)
        db.commit()
        db.refresh(template)

        fields_json = parse_template_fields(template.fields_json)
        word_form_id = get_or_create_word_form_id(db, effective_user_id)
        ensure_template_fields_exist(db, word_form_id, fields_json)
        
        auto_generated = len(fields) == 1 and "nội dung" in [f.to_dict() for f in fields][0].get("label", "").lower()
        
        return {
            "status": "success",
            "template_id": template.id,
            "template_name": template.template_name,
            "file_type": file_ext,
            "fields_count": len(fields),
            "fields": [f.to_dict() for f in fields],
            "auto_generated_fields": auto_generated,
            "message": "Upload và parse thành công" if not auto_generated else "Upload thành công. Không tìm thấy trường cấu trúc, đã tạo trường mặc định."
        }
    
    except Exception as e:
        logger.error(f"Lỗi upload file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@router.get("/supported-formats")
async def get_supported_formats():
    """Lấy danh sách các định dạng file được hỗ trợ"""
    return {
        "supported_extensions": FileParserFactory.get_supported_extensions(),
        "description": {
            ".docx": "Word Document",
            ".pdf": "PDF File", 
            ".xlsx": "Excel Spreadsheet (2007+)",
            ".xls": "Excel Spreadsheet (97-2003)",
            ".csv": "Comma-Separated Values",
            ".txt": "Plain Text File"
        }
    }


@router.get("/templates")
async def get_user_templates(
    user_id: int | None = Query(None, description="ID của user (optional, admin only)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lấy danh sách template của user"""
    effective_user_id = resolve_effective_user_id(current_user, user_id)

    templates = db.query(WordTemplate).filter(WordTemplate.user_id == effective_user_id).all()
    
    return {
        "templates": [
            {
                "id": t.id,
                "name": t.template_name,
                "filename": extract_clean_filename(t.original_filename),
                "fields_count": len(parse_template_fields(t.fields_json)),
                "created_at": t.created_at.isoformat(),
                "submissions_count": len(t.submissions)
            }
            for t in templates
        ]
    }


@router.get("/template/{template_id}")
async def get_template_detail(
    template_id: int,
    user_id: int | None = Query(None, description="ID của user (optional, admin only)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lấy chi tiết template"""
    effective_user_id = resolve_effective_user_id(current_user, user_id)

    template = db.query(WordTemplate).filter(
        WordTemplate.id == template_id,
        WordTemplate.user_id == effective_user_id
    ).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template không tồn tại")

    if not os.path.exists(template.file_path):
        raise HTTPException(status_code=404, detail="File template không tồn tại trên server")

    form_id = get_or_create_word_form_id(db, effective_user_id)
    
    fields_json = parse_template_fields(template.fields_json)
    field_by_name = ensure_template_fields_exist(db, form_id, fields_json)

    # Enrich fields với database field IDs
    enriched_fields = []
    for idx, field_data in enumerate(fields_json):
        field_name = field_data.get("name", "")
        field_label = field_data.get("label", field_name)
        field_id = field_by_name.get(field_name, -1)
        
        enriched_fields.append({
            **field_data,
            "field_id": field_id,
            "field_index": idx,
            "field_label": field_label
        })
    
    try:
        submissions_count = len(template.submissions)
    except Exception as e:
        logger.error(f"Error getting submissions count: {str(e)}")
        submissions_count = 0
    
    return {
        "id": template.id,
        "name": template.template_name,
        "filename": extract_clean_filename(template.original_filename),
        "fields": enriched_fields,
        "form_id": form_id,
        "created_at": template.created_at.isoformat() if template.created_at else None,
        "submissions_count": submissions_count
    }


@router.post("/submit")
async def submit_form(
    request: Request,
    template_id: int = Query(...),
    user_id: int | None = Query(None, description="ID của user (optional, admin only)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit form data cho template"""
    effective_user_id = resolve_effective_user_id(current_user, user_id)
    form_id = get_or_create_word_form_id(db, effective_user_id)
    logger.info(f"submit_form called: template_id={template_id}, user_id={effective_user_id}, form_id={form_id}")
    
    template = db.query(WordTemplate).filter(
        WordTemplate.id == template_id,
        WordTemplate.user_id == effective_user_id
    ).first()
    if not template:
        logger.error(f"Template {template_id} not found")
        raise HTTPException(status_code=404, detail="Template không tồn tại")
    
    # Get JSON data from request body
    try:
        data = await request.json()
        if not isinstance(data, dict):
            data = {}
    except Exception as e:
        logger.error(f"Error parsing JSON: {str(e)}", exc_info=True)
        data = {}
    
    logger.info(f"Received form data: {data}")
    
    try:
        # Lưu submission
        submission = WordSubmission(
            template_id=template_id,
            user_id=effective_user_id,
            submission_data=json.dumps(data or {})
        )
        db.add(submission)
        db.commit()
        db.refresh(submission)
        
        logger.info(f"Submission saved: {submission.id}")
        
        # Lưu entries
        try:
            fields_json = parse_template_fields(template.fields_json)
            logger.info(f"Template has {len(fields_json)} fields")
            field_by_name = ensure_template_fields_exist(db, form_id, fields_json)
            entries_to_insert: list[Entry] = []
            
            for field_data in fields_json:
                field_name = field_data.get("name", "")
                logger.info(f"Processing field: {field_name}")
                
                # Lấy giá trị từ form submit
                value = data.get(field_name, "").strip()
                if not value:
                    logger.info(f"  Field {field_name} has no value, skipping")
                    continue
                
                logger.info(f"  Field {field_name} value: '{value}'")
                
                field_id = field_by_name.get(field_name)
                if not field_id:
                    logger.warning(f"  Field mapping missing for {field_name}, skipping")
                    continue
                
                # Lưu entry
                entry = Entry(
                    user_id=effective_user_id,
                    field_id=field_id,
                    form_id=form_id,
                    value=value
                )
                entries_to_insert.append(entry)

            if entries_to_insert:
                db.add_all(entries_to_insert)
                db.commit()
                logger.info(f"Saved {len(entries_to_insert)} entries for submission {submission.id}")
        
        except Exception as e:
            logger.error(f"Error saving entries: {str(e)}", exc_info=True)
            # Không throw error, submission đã lưu
        
        logger.info(f"Submit completed for submission {submission.id}")
        return {
            "status": "success",
            "submission_id": submission.id,
            "message": "Submit thành công"
        }
    
    except Exception as e:
        logger.error(f"Error in submit_form: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@router.get("/submissions")
async def get_submissions(
    template_id: int = Query(None),
    user_id: int | None = Query(None, description="ID của user (optional, admin only)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lấy danh sách submission"""
    effective_user_id = resolve_effective_user_id(current_user, user_id)

    query = db.query(WordSubmission).filter(WordSubmission.user_id == effective_user_id)
    
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
    user_id: int | None = Query(None, description="ID của user (optional, admin only)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lấy chi tiết một submission"""
    effective_user_id = resolve_effective_user_id(current_user, user_id)

    submission = db.query(WordSubmission).filter(
        WordSubmission.id == submission_id,
        WordSubmission.user_id == effective_user_id
    ).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission không tồn tại")
    
    return {
        "id": submission.id,
        "template_id": submission.template_id,
        "template_name": submission.template.template_name,
        "data": json.loads(submission.submission_data) if submission.submission_data else {},
        "created_at": submission.created_at.isoformat(),
        "updated_at": submission.created_at.isoformat()
    }


@router.put("/submission/{submission_id}")
async def update_submission(
    submission_id: int,
    request: Request,
    user_id: int | None = Query(None, description="ID của user (optional, admin only)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cập nhật dữ liệu submission"""
    effective_user_id = resolve_effective_user_id(current_user, user_id)

    submission = db.query(WordSubmission).filter(
        WordSubmission.id == submission_id,
        WordSubmission.user_id == effective_user_id
    ).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission không tồn tại")
    
    try:
        # Đọc JSON body từ request
        data = await request.json()
        if data is None:
            data = {}
        
        submission.submission_data = json.dumps(data)
        db.commit()
        db.refresh(submission)
        
        return {
            "status": "success",
            "message": "Cập nhật submission thành công",
            "id": submission.id,
            "data": json.loads(submission.submission_data)
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Lỗi cập nhật: {str(e)}")


@router.delete("/submission/{submission_id}")
async def delete_submission(
    submission_id: int,
    user_id: int | None = Query(None, description="ID của user (optional, admin only)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Xóa submission"""
    effective_user_id = resolve_effective_user_id(current_user, user_id)

    submission = db.query(WordSubmission).filter(
        WordSubmission.id == submission_id,
        WordSubmission.user_id == effective_user_id
    ).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission không tồn tại")
    
    try:
        db.delete(submission)
        db.commit()
        
        return {
            "status": "success",
            "message": "Xóa submission thành công"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Lỗi xóa: {str(e)}")


@router.delete("/template/{template_id}")
async def delete_template(
    template_id: int,
    user_id: int | None = Query(None, description="ID của user (optional, admin only)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Xóa template"""
    effective_user_id = resolve_effective_user_id(current_user, user_id)

    template = db.query(WordTemplate).filter(
        WordTemplate.id == template_id,
        WordTemplate.user_id == effective_user_id
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
