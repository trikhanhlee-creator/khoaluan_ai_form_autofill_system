from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta
from app.db.models import Entry
from app.core.config import settings


class EntryRepository:
    """Repository để lấy dữ liệu lịch sử nhập liệu (entries) từ database"""

    @staticmethod
    def get_recent_entries(
        db: Session,
        user_id: int,
        field_id: int,
        limit: int = None
    ) -> list[Entry]:
        """
        Lấy các entry gần nhất cho user và field cụ thể
        
        Args:
            db: Database session
            user_id: ID của user
            field_id: ID của field
            limit: Số lượng entry tối đa (mặc định từ config)
            
        Returns:
            Danh sách các Entry được sắp xếp theo thời gian giảm dần
        """
        if limit is None:
            limit = settings.MIN_HISTORY_ENTRIES

        entries = db.query(Entry).filter(
            Entry.user_id == user_id,
            Entry.field_id == field_id
        ).order_by(desc(Entry.created_at)).limit(limit).all()

        return entries

    @staticmethod
    def get_entries_by_field(
        db: Session,
        user_id: int,
        field_id: int,
        days: int = 30
    ) -> list[Entry]:
        """
        Lấy tất cả entry trong khoảng thời gian gần đây
        
        Args:
            db: Database session
            user_id: ID của user
            field_id: ID của field
            days: Số ngày quay lại (mặc định 30 ngày)
            
        Returns:
            Danh sách các Entry trong khoảng thời gian
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        entries = db.query(Entry).filter(
            Entry.user_id == user_id,
            Entry.field_id == field_id,
            Entry.created_at >= start_date
        ).order_by(desc(Entry.created_at)).all()

        return entries

    @staticmethod
    def count_field_entries(
        db: Session,
        user_id: int,
        field_id: int
    ) -> int:
        """
        Đếm số lượng entry cho một field
        
        Args:
            db: Database session
            user_id: ID của user
            field_id: ID của field
            
        Returns:
            Số lượng entry
        """
        count = db.query(Entry).filter(
            Entry.user_id == user_id,
            Entry.field_id == field_id
        ).count()

        return count

    @staticmethod
    def create_entry(
        db: Session,
        user_id: int,
        field_id: int,
        form_id: int,
        value: str
    ) -> Entry:
        """
        Tạo một entry mới
        
        Args:
            db: Database session
            user_id: ID của user
            field_id: ID của field
            form_id: ID của form
            value: Giá trị nhập vào
            
        Returns:
            Entry vừa được tạo
        """
        entry = Entry(
            user_id=user_id,
            field_id=field_id,
            form_id=form_id,
            value=value,
            created_at=datetime.utcnow()
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
