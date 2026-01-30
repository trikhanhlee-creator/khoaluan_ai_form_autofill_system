from collections import Counter
from typing import List, Dict, Tuple
from datetime import datetime
from app.db.models import Entry


class RuleEngine:
    """
    Engine AI để xử lý logic gợi ý dựa trên quy tắc
    - Tính tần suất của các giá trị
    - Tính recency (gần nhất) của các giá trị
    - Xếp hạng: tần suất (cao) -> gần nhất (mới)
    - Yêu cầu tối thiểu 2 entries mới gợi ý
    """

    @staticmethod
    def calculate_frequency(entries: List[Entry]) -> Dict[str, int]:
        """
        Tính tần suất xuất hiện của các giá trị
        
        Args:
            entries: Danh sách các Entry
            
        Returns:
            Dict với key là giá trị, value là tần suất
        """
        if not entries:
            return {}

        # Lấy danh sách giá trị từ entries
        values = [entry.value for entry in entries]
        
        # Sử dụng Counter để tính tần suất
        frequency = Counter(values)
        
        return dict(frequency)

    @staticmethod
    def get_last_occurrence(entries: List[Entry]) -> Dict[str, datetime]:
        """
        Lấy thời gian gần nhất mà mỗi giá trị được nhập
        
        Args:
            entries: Danh sách các Entry
            
        Returns:
            Dict với key là giá trị, value là datetime gần nhất
        """
        if not entries:
            return {}
        
        last_occurrence = {}
        for entry in entries:
            if entry.value not in last_occurrence:
                last_occurrence[entry.value] = entry.created_at
            else:
                # Giữ lại thời gian mới nhất (lớn nhất)
                if entry.created_at > last_occurrence[entry.value]:
                    last_occurrence[entry.value] = entry.created_at
        
        return last_occurrence

    @staticmethod
    def rank_suggestions(
        entries: List[Entry],
        top_k: int = 5
    ) -> List[Tuple[str, int, int, datetime]]:
        """
        Xếp hạng gợi ý dựa trên:
        1. Tần suất (cao nhất)
        2. Thời gian gần nhất (mới nhất)
        
        Args:
            entries: Danh sách các Entry
            top_k: Số lượng gợi ý top (mặc định 5)
            
        Returns:
            Danh sách tuple (giá_trị, tần_suất, xếp_hạng, thời_gian_gần_nhất)
        """
        if not entries:
            return []

        # Tính tần suất
        frequency = RuleEngine.calculate_frequency(entries)
        
        # Lấy thời gian gần nhất
        last_occurrence = RuleEngine.get_last_occurrence(entries)

        # Tạo danh sách để sắp xếp
        items = [
            (value, freq, last_occurrence[value])
            for value, freq in frequency.items()
        ]
        
        # Sắp xếp: frequency cao -> thấp, nếu frequency bằng thì created_at mới -> cũ
        sorted_items = sorted(
            items,
            key=lambda x: (-x[1], -x[2].timestamp())
        )

        # Lấy top_k gợi ý
        top_suggestions = sorted_items[:top_k]

        # Tạo danh sách tuple với xếp hạng
        result = [
            (value, freq, rank + 1, last_dt)
            for rank, (value, freq, last_dt) in enumerate(top_suggestions)
        ]

        return result

    @staticmethod
    def generate_suggestions(
        entries: List[Entry],
        top_k: int = 5
    ) -> List[Dict]:
        """
        Sinh ra danh sách gợi ý từ lịch sử entries
        
        Yêu cầu:
        - Tối thiểu 2 entries mới gợi ý
        - Xếp hạng theo: tần suất (cao) -> gần nhất (mới)
        - Trả max 5 gợi ý
        
        Args:
            entries: Danh sách các Entry từ lịch sử
            top_k: Số lượng gợi ý top (mặc định 5)
            
        Returns:
            Danh sách dict chứa:
                - suggested_value: Giá trị gợi ý
                - frequency: Tần suất xuất hiện
                - ranking: Xếp hạng (1, 2, 3,...)
                - last_used: Thời gian gần nhất sử dụng
        """
        # Kiểm tra có đủ entries không (tối thiểu 2)
        if len(entries) < 2:
            return []
        
        # Xếp hạng theo tần suất + recency
        ranked = RuleEngine.rank_suggestions(entries, top_k)
        
        # Chuyển thành dict
        suggestions = [
            {
                "suggested_value": value,
                "frequency": freq,
                "ranking": rank,
                "last_used": last_dt.isoformat() if last_dt else None
            }
            for value, freq, rank, last_dt in ranked
        ]
        
        return suggestions

    @staticmethod
    def validate_entries(entries: List[Entry], min_count: int = 2) -> bool:
        """
        Kiểm tra xem có đủ entries để tạo gợi ý không
        Mặc định yêu cầu tối thiểu 2 entries
        
        Args:
            entries: Danh sách các Entry
            min_count: Số lượng entry tối thiểu (mặc định 2)
        """
        return len(entries) >= min_count
