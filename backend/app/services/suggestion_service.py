from sqlalchemy.orm import Session
from app.db.repositories.entry_repo import EntryRepository
from app.ai.rule_engine import RuleEngine
from app.core.config import settings
from app.core.logger import logger
from app.db.models import Entry, Suggestion
from typing import List, Dict
from datetime import datetime
from sqlalchemy import func


class SuggestionService:
    """
    Service để xử lý logic gợi ý
    - Lấy dữ liệu từ repository
    - Sử dụng AI rule engine để tạo gợi ý
    - Lưu entry từ plugin
    """

    @staticmethod
    def get_suggestions(
        db: Session,
        user_id: int,
        field_id: int,
        top_k: int = None
    ) -> List[Dict]:
        """
        Lấy top gợi ý cho một field của user
        
        Logic:
        1. Lấy TẤT CẢ entries từ lịch sử
        2. Kiểm tra có >= 2 entries không
        3. Nếu đủ → tính tần suất + recency
        4. Trả top 5 gợi ý
        
        Args:
            db: Database session
            user_id: ID của user
            field_id: ID của field
            top_k: Số lượng gợi ý top (mặc định 5)
            
        Returns:
            Danh sách dict chứa gợi ý (rỗng nếu < 2 entries)
        """
        try:
            if top_k is None:
                top_k = 5  # Default 5 suggestions

            logger.info(f"Getting suggestions for user_id={user_id}, field_id={field_id}")

            # Lấy TẤT CẢ entries từ lịch sử
            entries = EntryRepository.get_recent_entries(
                db=db,
                user_id=user_id,
                field_id=field_id,
                limit=1000  # Lấy tất cả
            )

            if not entries:
                logger.info(f"No entries found for user_id={user_id}, field_id={field_id}")
                return []

            logger.info(f"Found {len(entries)} entries for field_id={field_id}")

            # Kiểm tra có >= 2 entries không
            if len(entries) < 2:
                logger.info(f"Not enough entries ({len(entries)} < 2) for suggestions")
                return []

            # Sinh gợi ý (max 5)
            suggestions = RuleEngine.generate_suggestions(entries, top_k=min(top_k, 5))

            logger.info(f"Generated {len(suggestions)} suggestions")
            return suggestions

        except Exception as e:
            logger.error(f"Error getting suggestions: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def save_entry(
        db: Session,
        user_id: int,
        field_id: int,
        form_id: int,
        value: str
    ) -> Dict:
        """
        Lưu entry từ plugin vào database
        Không tạo suggestions table - suggestions được lấy trực tiếp từ entries
        
        Args:
            db: Database session
            user_id: ID của user
            field_id: ID của field
            form_id: ID của form
            value: Giá trị được nhập
            
        Returns:
            Dict chứa status và entry_id
        """
        try:
            logger.info(f"Saving entry: user_id={user_id}, field_id={field_id}, value={value}")
            
            # Tạo entry mới
            new_entry = Entry(
                user_id=user_id,
                field_id=field_id,
                form_id=form_id,
                value=value,
                created_at=datetime.utcnow()
            )
            
            # Lưu vào database
            db.add(new_entry)
            db.commit()
            db.refresh(new_entry)
            
            logger.info(f"Entry saved with ID: {new_entry.id}")
            
            return {
                "status": "success",
                "entry_id": new_entry.id,
                "message": "Entry saved successfully"
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving entry: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def _update_suggestions_cache(
        db: Session,
        user_id: int,
        field_id: int,
        new_value: str
    ):
        """
        Cập nhật bảng suggestions cache sau khi lưu entry mới
        
        Logic:
        - Nếu giá trị đã tồn tại: tăng frequency
        - Nếu giá trị chưa tồn tại: thêm mới với frequency=1
        """
        try:
            logger.info(f"Updating suggestions cache: user_id={user_id}, field_id={field_id}, value={new_value}")
            
            # Kiểm tra suggestion đã tồn tại
            existing_suggestion = db.query(Suggestion).filter(
                Suggestion.user_id == user_id,
                Suggestion.field_id == field_id,
                Suggestion.suggested_value == new_value
            ).first()
            
            if existing_suggestion:
                # Tăng frequency
                existing_suggestion.frequency += 1
                existing_suggestion.ranking = existing_suggestion.frequency
                existing_suggestion.updated_at = datetime.utcnow()
                logger.info(f"Updated suggestion: frequency → {existing_suggestion.frequency}")
            else:
                # Thêm mới
                new_suggestion = Suggestion(
                    user_id=user_id,
                    field_id=field_id,
                    suggested_value=new_value,
                    frequency=1,
                    ranking=1,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(new_suggestion)
                logger.info(f"Created new suggestion")
            
            db.commit()
            logger.info(f"Suggestions cache updated successfully")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating suggestions cache: {str(e)}", exc_info=True)
            # Không raise - nếu cache update fail, entry vẫn lưu được

    @staticmethod
    def get_suggestions_with_history(
        db: Session,
        user_id: int,
        field_id: int,
        days: int = None,
        top_k: int = None
    ) -> List[Dict]:
        """
        Lấy gợi ý dựa trên lịch sử trong khoảng thời gian
        
        Args:
            db: Database session
            user_id: ID của user
            field_id: ID của field
            days: Số ngày quay lại (mặc định 30)
            top_k: Số lượng gợi ý top (mặc định từ config)
            
        Returns:
            Danh sách dict chứa gợi ý
        """
        try:
            if days is None:
                days = settings.HISTORY_LOOKBACK_DAYS
            if top_k is None:
                top_k = settings.TOP_SUGGESTIONS_COUNT

            logger.info(f"Getting suggestions with history for user_id={user_id}, field_id={field_id}, days={days}")

            # Lấy entries trong khoảng thời gian
            entries = EntryRepository.get_entries_by_field(
                db=db,
                user_id=user_id,
                field_id=field_id,
                days=days
            )

            if not entries:
                logger.warning(f"No entries found in the last {days} days for user_id={user_id}, field_id={field_id}")
                return []

            logger.info(f"Found {len(entries)} entries in the last {days} days")

            # Tính tần suất và trả top gợi ý
            suggestions = RuleEngine.generate_suggestions(entries, top_k=top_k)

            logger.info(f"Generated {len(suggestions)} suggestions from history")
            return suggestions

        except Exception as e:
            logger.error(f"Error getting suggestions with history: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def get_field_statistics(
        db: Session,
        user_id: int,
        field_id: int
    ) -> Dict:
        """
        Lấy thống kê về entries cho một field
        
        Args:
            db: Database session
            user_id: ID của user
            field_id: ID của field
            
        Returns:
            Dict chứa thống kê
        """
        try:
            # Đếm tổng entries
            total_entries = EntryRepository.count_field_entries(
                db=db,
                user_id=user_id,
                field_id=field_id
            )

            # Lấy recent entries
            recent_entries = EntryRepository.get_recent_entries(
                db=db,
                user_id=user_id,
                field_id=field_id,
                limit=10
            )

            # Tính tần suất
            frequency = RuleEngine.calculate_frequency(recent_entries)

            return {
                "total_entries": total_entries,
                "recent_entries_count": len(recent_entries),
                "unique_values": len(frequency),
                "frequency_distribution": frequency
            }

        except Exception as e:
            logger.error(f"Error getting field statistics: {str(e)}", exc_info=True)
            raise
