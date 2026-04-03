"""
API routes cho soạn thảo tài liệu với AI suggestions
- GET/POST documents
- Lấy AI suggestions
- Lưu lịch sử soạn thảo
"""

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import json

from app.db.session import get_db
from app.core.logger import logger
from app.core.auth import get_current_user
from app.services.ai_composer_service import AIComposerService
from app.db.models import Document, User

# Khởi tạo composer service
composer_service = AIComposerService()

# Router
router = APIRouter(
    prefix="/api/composer",
    tags=["composer"],
    responses={404: {"description": "Not found"}},
)


# ============ Pydantic Models ============

class DocumentCreate(BaseModel):
    """Schema cho tạo document mới"""
    title: str
    content: str
    description: Optional[str] = None


class DocumentUpdate(BaseModel):
    """Schema cho cập nhật document"""
    title: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None


class SuggestionRequest(BaseModel):
    """Schema cho request suggestions"""
    context: str
    max_suggestions: int = 3
    suggestion_length: int = 10
    mode: str = "continuation"  # continuation | rewrite
    original_text: Optional[str] = None
    instruction: Optional[str] = None


class CompositionActionRequest(BaseModel):
    """Schema cho lưu composition action"""
    document_id: int
    action_type: str  # 'suggestion', 'edit', 'acceptance'
    suggested_text: Optional[str] = None
    original_text: Optional[str] = None
    modified_text: Optional[str] = None
    context: Optional[str] = None
    accepted: int = 0


class DocumentResponse(BaseModel):
    """Response schema cho document"""
    id: int
    title: str
    content: str
    description: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# ============ Endpoints ============

@router.post("/documents", response_model=dict)
async def create_document(
    doc_data: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Tạo document mới
    
    Tags:
        composer
    """
    try:
        logger.info(f"Creating document for user {current_user.id}")
        
        result = composer_service.save_document(
            db=db,
            user_id=current_user.id,
            title=doc_data.title,
            content=doc_data.content,
            description=doc_data.description
        )
        
        if not result:
            raise HTTPException(status_code=400, detail="Failed to create document")
        
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"Error creating document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents")
async def list_documents(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Liệt kê documents của user
    
    Tags:
        composer
    """
    try:
        logger.info(f"Listing documents for user {current_user.id}")
        
        documents = composer_service.list_documents(
            db=db,
            user_id=current_user.id,
            limit=limit,
            offset=offset
        )
        
        return {"success": True, "data": documents}
        
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents/{document_id}")
async def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lấy document theo ID
    
    Tags:
        composer
    """
    try:
        logger.info(f"Getting document {document_id} for user {current_user.id}")
        
        doc = composer_service.get_document(
            db=db,
            user_id=current_user.id,
            document_id=document_id
        )
        
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {"success": True, "data": doc}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/documents/{document_id}")
async def update_document(
    document_id: int,
    doc_data: DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cập nhật document
    
    Tags:
        composer
    """
    try:
        logger.info(f"Updating document {document_id} for user {current_user.id}")
        
        # Lấy document hiện có
        doc = db.query(Document).filter(
            Document.id == document_id,
            Document.user_id == current_user.id
        ).first()
        
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Cập nhật các field nếu được cung cấp
        if doc_data.title:
            doc.title = doc_data.title
        if doc_data.content:
            doc.content = doc_data.content
        if doc_data.description is not None:
            doc.description = doc_data.description
        
        db.commit()
        db.refresh(doc)
        
        return {"success": True, "data": {
            "id": doc.id,
            "title": doc.title,
            "updated_at": doc.updated_at.isoformat()
        }}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating document: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Xóa document
    
    Tags:
        composer
    """
    try:
        logger.info(f"Deleting document {document_id} for user {current_user.id}")
        
        success = composer_service.delete_document(
            db=db,
            user_id=current_user.id,
            document_id=document_id
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {"success": True, "message": "Document deleted"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/suggestions")
async def get_suggestions(
    suggestion_req: SuggestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lấy AI suggestions cho tiếp theo của text
    
    Tags:
        composer
    """
    try:
        logger.info(f"Getting suggestions for user {current_user.id}")
        
        suggestions = await composer_service.get_text_suggestions(
            context=suggestion_req.context,
            max_suggestions=suggestion_req.max_suggestions,
            suggestion_length=suggestion_req.suggestion_length,
            mode=suggestion_req.mode,
            original_text=suggestion_req.original_text,
            instruction=suggestion_req.instruction
        )
        
        return {"success": True, "data": suggestions}
        
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save-action")
async def save_composition_action(
    action_req: CompositionActionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lưu composition action (suggestion, edit, acceptance)
    
    Tags:
        composer
    """
    try:
        logger.info(f"Saving composition action for user {current_user.id}")
        
        result = composer_service.save_composition_action(
            db=db,
            document_id=action_req.document_id,
            user_id=current_user.id,
            action_type=action_req.action_type,
            suggested_text=action_req.suggested_text,
            original_text=action_req.original_text,
            modified_text=action_req.modified_text,
            context=action_req.context,
            accepted=action_req.accepted
        )
        
        if not result:
            raise HTTPException(status_code=400, detail="Failed to save action")
        
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"Error saving composition action: {e}")
        raise HTTPException(status_code=500, detail=str(e))
