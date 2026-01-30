from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Field, Entry
from app.services.suggestion_service import SuggestionService
from app.schemas.suggestion import (
    SuggestionsListResponse,
    SuggestionResponse,
    FieldStatisticsResponse
)
from app.core.logger import logger

router = APIRouter(
    prefix="/api/suggestions",
    tags=["suggestions"],
    responses={404: {"description": "Not found"}}
)


@router.get("")
async def get_suggestions(
    user_id: int = Query(..., description="ID của user"),
    field_id: int = Query(..., description="ID của field"),
    top_k: int = Query(5, description="Số lượng gợi ý top (mặc định 5, max 5)"),
    db: Session = Depends(get_db)
):
    """
    API GET /api/suggestions
    
    Input:
    - user_id: ID của user
    - field_id: ID của field
    - top_k: Số lượng gợi ý top
    
    Output:
    - Danh sách gợi ý với value, frequency, ranking
    """
    try:
        logger.info(f"Request suggestions: user_id={user_id}, field_id={field_id}, top_k={top_k}")
        
        # Validate input
        if user_id <= 0 or field_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="user_id và field_id phải là số dương"
            )
        
        if top_k <= 0 or top_k > 5:
            raise HTTPException(
                status_code=400,
                detail="top_k phải từ 1 đến 5"
            )
        
        # Get entries với raw query
        entries = db.query(Entry).filter(
            Entry.user_id == user_id,
            Entry.field_id == field_id
        ).all()
        
        logger.info(f"Found {len(entries)} entries for field {field_id}")
        
        # Build suggestions - group by value and count frequency
        suggestions = []
        if len(entries) >= 2:
            # Group by value và count frequency
            value_counts = {}
            for entry in entries:
                if entry.value not in value_counts:
                    value_counts[entry.value] = 0
                value_counts[entry.value] += 1
            
            # Chuyển thành list suggestions
            suggestions = [
                {"value": val, "frequency": count, "ranking": count}
                for val, count in sorted(value_counts.items(), key=lambda x: -x[1])[:5]
            ]
        
        logger.info(f"Generated {len(suggestions)} suggestions")
        
        return {
            "user_id": user_id,
            "field_id": field_id,
            "suggestions": suggestions,
            "total_count": len(suggestions),
            "message": "Suggestions retrieved successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_suggestions: {str(e)}", exc_info=True)
        return {
            "user_id": user_id,
            "field_id": field_id,
            "suggestions": [],
            "total_count": 0,
            "message": f"Error: {str(e)}"
        }


@router.get(
    "/debug",
    summary="Debug suggestions endpoint",
    description="Test endpoint"
)
async def debug_suggestions(
    user_id: int = Query(1),
    field_index: int = Query(0),
    form_id: int = Query(1),
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"[DEBUG] Starting: user_id={user_id}, field_index={field_index}, form_id={form_id}")
        
        # Step 1: Get fields
        fields = db.query(Field).filter(Field.form_id == form_id).all()
        logger.info(f"[DEBUG] Found {len(fields)} fields")
        
        if not fields or field_index >= len(fields):
            return {"error": f"Not enough fields. Total: {len(fields) if fields else 0}, Index: {field_index}"}
        
        field = fields[field_index]
        logger.info(f"[DEBUG] Field: id={field.id}, name={field.field_name}")
        
        # Just return field info, don't call service
        return {
            "success": True,
            "field": {"id": field.id, "name": field.field_name},
            "suggestions": [],
            "count": 0
        }
    except Exception as e:
        logger.error(f"[DEBUG] Error: {str(e)}", exc_info=True)
        return {"error": str(e)}


# Endpoint /by-index disabled - use /suggestions?user_id=X&field_id=Y instead

@router.get(
    "/by-name",
    response_model=SuggestionsListResponse,
    summary="Get suggestions for a field by name",
    description="Lấy gợi ý theo tên field (dùng cho Word forms)"
)
async def get_suggestions_by_name(
    user_id: int = Query(..., description="ID của user"),
    field_name: str = Query(..., description="Tên field (e.g. họ_và_tên)"),
    form_id: int = Query(1, description="ID của form (mặc định 1)"),
    top_k: int = Query(5, description="Số lượng gợi ý top (mặc định 5, max 5)"),
    db: Session = Depends(get_db)
):
    """
    API GET /api/suggestions/by-name
    
    Lấy gợi ý dựa trên tên field thay vì field_id
    Tự động tìm field_id từ field_name và form_id
    
    Input:
    - user_id: ID của user
    - field_name: Tên field (e.g. họ_và_tên)
    - form_id: ID của form (mặc định 1)
    - top_k: Số lượng gợi ý top
    
    Output:
    - Danh sách gợi ý
    """
    try:
        logger.info(f"Request suggestions by name: user_id={user_id}, field_name={field_name}, top_k={top_k}")
        
        # Validate input
        if user_id <= 0:
            raise HTTPException(status_code=400, detail="user_id phải là số dương")
        
        if not field_name:
            raise HTTPException(status_code=400, detail="field_name không được để trống")
        
        if top_k <= 0 or top_k > 5:
            raise HTTPException(status_code=400, detail="top_k phải từ 1 đến 5")
        
        # Tìm field theo field_name
        field = db.query(Field).filter(
            Field.form_id == form_id,
            Field.field_name == field_name
        ).first()
        
        if not field:
            logger.warning(f"Field not found: form_id={form_id}, field_name={field_name}")
            # Trả empty list nếu field không tồn tại
            return SuggestionsListResponse(
                user_id=user_id,
                field_id=0,
                suggestions=[],
                total_count=0
            )
        
        # Gọi service để lấy gợi ý
        suggestions = SuggestionService.get_suggestions(
            db=db,
            user_id=user_id,
            field_id=field.id,
            top_k=top_k
        )
        
        logger.info(f"Successfully retrieved {len(suggestions)} suggestions for field {field_name}")
        
        return SuggestionsListResponse(
            user_id=user_id,
            field_id=field.id,
            suggestions=suggestions,
            total_count=len(suggestions)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_suggestions_by_name: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Lỗi khi lấy gợi ý")



@router.get(
    "/history",
    response_model=SuggestionsListResponse,
    summary="Get suggestions based on history",
    description="Lấy gợi ý dựa vào lịch sử trong khoảng thời gian"
)
async def get_suggestions_with_history(
    user_id: int = Query(..., description="ID của user"),
    field_id: int = Query(..., description="ID của field"),
    days: int = Query(30, description="Số ngày quay lại (mặc định 30)"),
    top_k: int = Query(3, description="Số lượng gợi ý top (mặc định 3)"),
    db: Session = Depends(get_db)
):
    """
    API GET /api/suggestions/history
    
    Lấy gợi ý dựa vào lịch sử trong khoảng thời gian cụ thể
    """
    try:
        logger.info(f"Request suggestions with history: user_id={user_id}, field_id={field_id}, days={days}, top_k={top_k}")
        
        # Validate input
        if user_id <= 0 or field_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="user_id và field_id phải là số dương"
            )
        
        if days <= 0 or days > 365:
            raise HTTPException(
                status_code=400,
                detail="days phải từ 1 đến 365"
            )
        
        if top_k <= 0 or top_k > 10:
            raise HTTPException(
                status_code=400,
                detail="top_k phải từ 1 đến 10"
            )
        
        # Gọi service để lấy gợi ý
        suggestions = SuggestionService.get_suggestions_with_history(
            db=db,
            user_id=user_id,
            field_id=field_id,
            days=days,
            top_k=top_k
        )
        
        logger.info(f"Successfully retrieved {len(suggestions)} suggestions from history")
        
        return SuggestionsListResponse(
            user_id=user_id,
            field_id=field_id,
            suggestions=suggestions,
            total_count=len(suggestions),
            message=f"Suggestions retrieved from {days} days of history"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_suggestions_with_history: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Lỗi khi lấy gợi ý từ lịch sử"
        )


@router.get(
    "/stats",
    response_model=FieldStatisticsResponse,
    summary="Get field statistics",
    description="Lấy thống kê về entries của một field"
)
async def get_field_stats(
    user_id: int = Query(..., description="ID của user"),
    field_id: int = Query(..., description="ID của field"),
    db: Session = Depends(get_db)
):
    """
    API GET /api/suggestions/stats
    
    Lấy thống kê về entries của một field
    """
    try:
        logger.info(f"Request stats: user_id={user_id}, field_id={field_id}")
        
        # Validate input
        if user_id <= 0 or field_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="user_id và field_id phải là số dương"
            )
        
        # Gọi service để lấy thống kê
        stats = SuggestionService.get_field_statistics(
            db=db,
            user_id=user_id,
            field_id=field_id
        )
        
        logger.info(f"Successfully retrieved stats: {stats}")
        
        return FieldStatisticsResponse(**stats)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_field_stats: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Lỗi khi lấy thống kê"
        )

@router.post(
    "/save",
    summary="Save entry from plugin",
    description="Lưu entry từ Word plugin vào database"
)
async def save_entry(
    user_id: int = Query(..., description="ID của user"),
    field_id: int = Query(..., description="ID của field"),
    form_id: int = Query(..., description="ID của form"),
    value: str = Query(..., description="Giá trị được nhập"),
    db: Session = Depends(get_db)
):
    """
    API POST /api/suggestions/save
    
    Lưu entry từ Word plugin.
    Plugin sẽ gọi endpoint này mỗi khi user nhập xong một field.
    
    Input:
    - user_id: ID của user
    - field_id: ID của field
    - form_id: ID của form
    - value: Giá trị được nhập
    
    Output:
    - status: "success" hoặc error
    - entry_id: ID của entry vừa được lưu
    """
    try:
        logger.info(f"Saving entry: user_id={user_id}, field_id={field_id}, value={value}")
        
        # Validate input
        if user_id <= 0 or field_id <= 0 or form_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="user_id, field_id, form_id phải là số dương"
            )
        
        if not value or len(value.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="value không được để trống"
            )
        
        # Gọi service để lưu entry
        result = SuggestionService.save_entry(
            db=db,
            user_id=user_id,
            field_id=field_id,
            form_id=form_id,
            value=value.strip()
        )
        
        logger.info(f"Entry saved successfully: {result}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in save_entry: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Lỗi khi lưu entry"
        )