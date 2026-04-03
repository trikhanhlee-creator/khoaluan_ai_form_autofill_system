"""
Service để tích hợp AI suggestions cho soạn thảo tài liệu
- Kết nối OpenAI/Gemini API
- Xử lý suggestions
- Lưu lịch sử soạn thảo
"""

from typing import List, Dict, Optional
from app.core.config import settings
from app.core.logger import logger
from sqlalchemy.orm import Session
from app.db.models import Document, CompositionHistory, User
from app.db.session import SessionLocal
from datetime import datetime
import json
import asyncio
import re


class AIComposerService:
    """Service cho AI document composition"""

    def __init__(self):
        """Khởi tạo AI service"""
        self.api_provider = settings.AI_PROVIDER  # openai | gemini | openrouter
        self.api_key = settings.AI_API_KEY
        self._init_ai_client()

    def _get_active_model(self) -> str:
        if self.api_provider == "openrouter":
            return settings.OPENROUTER_MODEL
        return settings.AI_MODEL or "gpt-4o-mini"

    def _init_ai_client(self):
        """Khởi tạo AI client (OpenAI, OpenRouter hoặc Gemini)"""
        try:
            if self.api_provider in ("openai", "openrouter"):
                try:
                    from openai import AsyncOpenAI
                    if self.api_provider == "openrouter":
                        openrouter_key = settings.OPENROUTER_API_KEY or self.api_key
                        if not openrouter_key:
                            logger.warning("OpenRouter API key is missing, using mock client")
                            self.client = None
                            return

                        self.api_key = openrouter_key
                        self.client = AsyncOpenAI(
                            api_key=openrouter_key,
                            base_url=settings.OPENROUTER_BASE_URL,
                            default_headers={
                                "HTTP-Referer": settings.OPENROUTER_SITE_URL,
                                "X-Title": settings.OPENROUTER_APP_NAME,
                            }
                        )
                        logger.info(f"OpenRouter client initialized with model: {self._get_active_model()}")
                    else:
                        self.client = AsyncOpenAI(api_key=self.api_key)
                        logger.info(f"AsyncOpenAI client initialized with model: {self._get_active_model()}")
                except ImportError:
                    logger.warning("OpenAI package not installed, using mock client")
                    self.client = None
            elif self.api_provider == "gemini":
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=self.api_key)
                    self.client = genai.GenerativeModel('gemini-pro')
                    logger.info("Gemini client initialized")
                except ImportError:
                    logger.warning("Google Generative AI package not installed, using mock client")
                    self.client = None
            else:
                logger.warning(f"Unknown AI provider: {self.api_provider}")
                self.client = None
        except Exception as e:
            logger.error(f"Error initializing AI client: {e}")
            self.client = None

    async def get_text_suggestions(
        self,
        context: str,
        max_suggestions: int = 3,
        suggestion_length: int = 10,
        mode: str = "continuation",
        original_text: Optional[str] = None,
        instruction: Optional[str] = None
    ) -> List[Dict]:
        """
        Lấy AI suggestions cho tiếp theo của text

        Args:
            context: Văn bản hiện tại (ngữ cảnh)
            max_suggestions: Số lượng suggestions (mặc định 3)
            suggestion_length: Độ dài trung bình của mỗi suggestion (từ)
            mode: continuation (viết tiếp) | rewrite (viết lại giữ ý)
            original_text: Câu/đoạn gốc cần viết lại (dùng cho mode rewrite)
            instruction: Yêu cầu chỉnh sửa do người dùng nhập

        Returns:
            Danh sách dict chứa suggestions
            Mỗi item: {'text': 'gợi ý', 'confidence': 0.8}
        """
        try:
            if not self.client:
                logger.warning("AI client not initialized, returning mock suggestions")
                return self._get_mock_suggestions(
                    context=context,
                    max_suggestions=max_suggestions,
                    mode=mode,
                    original_text=original_text,
                    instruction=instruction
                )

            logger.info(f"Getting suggestions for context: {context[:50]}...")

            if self.api_provider == "openai":
                suggestions = await self._get_openai_suggestions(
                    context, max_suggestions, suggestion_length, mode=mode, original_text=original_text, instruction=instruction
                )
            elif self.api_provider == "openrouter":
                suggestions = await self._get_openai_suggestions(
                    context, max_suggestions, suggestion_length, mode=mode, original_text=original_text, instruction=instruction
                )
            elif self.api_provider == "gemini":
                suggestions = await self._get_gemini_suggestions(
                    context, max_suggestions, suggestion_length, mode=mode, original_text=original_text, instruction=instruction
                )
            else:
                suggestions = self._get_mock_suggestions(
                    context=context,
                    max_suggestions=max_suggestions,
                    mode=mode,
                    original_text=original_text,
                    instruction=instruction
                )

            logger.info(f"Got {len(suggestions)} suggestions")
            return suggestions

        except Exception as e:
            logger.error(f"Error getting suggestions: {e}")
            return self._get_mock_suggestions(
                context=context,
                max_suggestions=max_suggestions,
                mode=mode,
                original_text=original_text,
                instruction=instruction
            )

    def _extract_last_sentence(self, context: str) -> str:
        text = (context or "").strip()
        if not text:
            return ""
        parts = re.split(r'(?<=[.!?…])\s+', text)
        return (parts[-1] or text).strip()

    def _normalize_suggestions(self, context: str, suggestions: List[Dict], max_suggestions: int) -> List[Dict]:
        """Chuẩn hóa để đảm bảo gợi ý là phần tiếp theo, không lặp lại ngữ cảnh."""
        normalized: List[Dict] = []
        seen = set()
        context_norm = re.sub(r'\s+', ' ', (context or '')).strip().lower()

        for item in suggestions:
            text = str(item.get("text", "")).strip().strip('"')
            if not text:
                continue

            text_norm = re.sub(r'\s+', ' ', text).strip().lower()
            if not text_norm:
                continue
            if text_norm in seen:
                continue
            # Tránh trường hợp mô hình lặp lại nguyên ngữ cảnh hoặc đoạn cuối
            if context_norm and (text_norm in context_norm or context_norm.endswith(text_norm)):
                continue

            seen.add(text_norm)
            normalized.append({
                "text": text,
                "confidence": float(item.get("confidence", 0.75)),
                "reason": item.get("reason", "Gợi ý tiếp nối theo ngữ cảnh")
            })

            if len(normalized) >= max_suggestions:
                break

        if normalized:
            return normalized

        return self._get_mock_suggestions(context, max_suggestions)

    def _normalize_rewrite_suggestions(
        self,
        context: str,
        original_text: str,
        suggestions: List[Dict],
        max_suggestions: int
    ) -> List[Dict]:
        """Chuẩn hóa gợi ý rewrite: giữ ý, khác cách diễn đạt, không lặp khuôn mẫu."""
        normalized: List[Dict] = []
        seen = set()
        source = re.sub(r'\s+', ' ', (original_text or '').strip()).lower()
        source_tokens = set(re.findall(r'\w+', source))

        for item in suggestions:
            text = str(item.get("text", "")).strip().strip('"')
            if not text:
                continue

            text_norm = re.sub(r'\s+', ' ', text).strip().lower()
            if not text_norm or text_norm in seen:
                continue

            # Loại trường hợp trả y nguyên câu gốc
            if source and text_norm == source:
                continue

            # Giữ mức độ gần nghĩa cơ bản bằng overlap từ khóa, nhưng vẫn cho phép diễn đạt linh hoạt
            candidate_tokens = set(re.findall(r'\w+', text_norm))
            if source_tokens and candidate_tokens:
                overlap_ratio = len(source_tokens & candidate_tokens) / max(1, len(source_tokens))
                if overlap_ratio < 0.2:
                    continue

            seen.add(text_norm)
            normalized.append({
                "text": text,
                "confidence": float(item.get("confidence", 0.82)),
                "reason": item.get("reason", "Viết lại tự nhiên hơn nhưng giữ nguyên ý chính")
            })

            if len(normalized) >= max_suggestions:
                break

        if normalized:
            return normalized

        return self._get_mock_suggestions(
            context=context,
            max_suggestions=max_suggestions,
            mode="rewrite",
            original_text=original_text
        )

    def _get_mock_suggestions(
        self,
        context: str,
        max_suggestions: int,
        mode: str = "continuation",
        original_text: Optional[str] = None,
        instruction: Optional[str] = None
    ) -> List[Dict]:
        """Trả về gợi ý fallback bám theo câu cuối để vẫn có tính tiếp nối."""
        if (mode or "continuation").strip().lower() == "rewrite":
            base = (original_text or context or "").strip()
            if base:
                instruction_hint = f"Yêu cầu: {instruction}." if instruction else ""
                return [
                    {
                        "text": base,
                        "confidence": 0.45,
                        "reason": f"Chưa kết nối AI thật nên tạm giữ nguyên nội dung gốc. {instruction_hint}".strip()
                    },
                    {
                        "text": re.sub(r'\s+', ' ', base).strip(),
                        "confidence": 0.42,
                        "reason": "Fallback local: chưa nhận được phản hồi hợp lệ từ model AI."
                    },
                ][:max_suggestions]

        last_sentence = self._extract_last_sentence(context)
        focus = " ".join(last_sentence.split()[-4:]).strip()
        focus_hint = f"{focus} " if focus else ""

        candidates = [
            {
                "text": f"Tiếp theo, {focus_hint}được làm rõ hơn bằng một ví dụ cụ thể để người đọc dễ hình dung.",
                "confidence": 0.72,
                "reason": "Mở rộng ý vừa nêu bằng ví dụ"
            },
            {
                "text": f"Từ đó, có thể thấy luận điểm này liên kết chặt với mục tiêu chung của nội dung bạn đang trình bày.",
                "confidence": 0.68,
                "reason": "Kết nối mạch ý hiện tại"
            },
            {
                "text": "Một hướng tiếp theo phù hợp là nêu ngắn gọn tác động thực tế, rồi chuyển sang phần giải pháp hoặc kết luận.",
                "confidence": 0.64,
                "reason": "Giữ cấu trúc mạch lạc"
            },
        ]
        return candidates[:max_suggestions]

    async def _get_openai_suggestions(
        self,
        context: str,
        max_suggestions: int,
        suggestion_length: int,
        mode: str = "continuation",
        original_text: Optional[str] = None,
        instruction: Optional[str] = None
    ) -> List[Dict]:
        """Lấy suggestions từ OpenAI"""
        try:
            mode_normalized = (mode or "continuation").strip().lower()
            if mode_normalized == "rewrite":
                source_text = (original_text or context or "").strip()
                user_instruction = (instruction or "").strip()
                prompt = f"""Bạn là trợ lý viết tiếng Việt chuyên VIẾT LẠI CÂU theo ngữ cảnh.
Nhiệm vụ: đề xuất {max_suggestions} phiên bản viết lại hay hơn cho câu gốc, nhưng vẫn GIỮ NGUYÊN ý nghĩa.

Ngữ cảnh xung quanh (để hiểu văn phong):
{context}

Câu gốc cần viết lại:
{source_text}

Yêu cầu chỉnh sửa của người dùng:
{user_instruction or "Không có yêu cầu bổ sung"}

Yêu cầu bắt buộc:
- Tuyệt đối không đổi nghĩa, không thêm thông tin mới làm lệch mục đích câu nói.
- Giữ nguyên ngôi xưng hô, sắc thái lịch sự/thân mật gần với câu gốc.
- Ưu tiên bám sát yêu cầu chỉnh sửa của người dùng nếu có.
- Viết tự nhiên, tránh các mẫu khuôn sáo lặp lại.
- Mỗi gợi ý là 1 câu hoàn chỉnh, khoảng {max(10, suggestion_length)} đến {max(18, suggestion_length + 10)} từ.
- Không dùng bullet, không thêm tiêu đề.
- Trả về JSON hợp lệ đúng cấu trúc dưới đây.

Định dạng JSON:
{{
    "suggestions": [
        {{"text": "câu viết lại 1", "confidence": 0.9, "reason": "vì sao cách diễn đạt này tốt hơn"}},
        {{"text": "câu viết lại 2", "confidence": 0.85, "reason": "vì sao cách diễn đạt này tốt hơn"}},
        {{"text": "câu viết lại 3", "confidence": 0.8, "reason": "vì sao cách diễn đạt này tốt hơn"}}
    ]
}}"""
            else:
                prompt = f"""Bạn là trợ lý viết tiếng Việt chuyên gợi ý VIẾT TIẾP.
Nhiệm vụ: đọc ngữ cảnh và đề xuất {max_suggestions} câu/đoạn NGẮN để tiếp nối mạch ý.

Ngữ cảnh hiện tại:
{context}

Yêu cầu bắt buộc:
- Chỉ viết phần tiếp theo, không lặp lại hoặc diễn giải lại nguyên văn ngữ cảnh.
- Mỗi gợi ý dài khoảng {suggestion_length} đến {suggestion_length + 8} từ.
- Giữ mạch logic với câu cuối của ngữ cảnh, tiếng Việt tự nhiên.
- Không dùng bullet, không thêm tiêu đề.
- Trả về JSON hợp lệ đúng cấu trúc dưới đây.

Định dạng JSON:
{{
    "suggestions": [
        {{"text": "phần viết tiếp 1", "confidence": 0.9}},
        {{"text": "phần viết tiếp 2", "confidence": 0.8}},
        {{"text": "phần viết tiếp 3", "confidence": 0.7}}
    ]
}}"""

            if self.api_provider == "openrouter":
                merged_prompt = (
                    "Bạn là trợ lý tiếng Việt. "
                    + ("Chuyên viết lại câu giữ nguyên ý nghĩa theo ngữ cảnh. " if mode_normalized == "rewrite" else "Chuyên viết tiếp mạch nội dung. ")
                    + "Luôn trả về JSON hợp lệ.\n\n"
                    + prompt
                )
                messages = [{"role": "user", "content": merged_prompt}]
            else:
                messages = [
                    {
                        "role": "system",
                        "content": (
                            "Bạn là trợ lý tiếng Việt.")
                            + (" Chuyên viết lại câu giữ nguyên ý nghĩa theo ngữ cảnh." if mode_normalized == "rewrite" else " Chuyên viết tiếp mạch nội dung.")
                            + " Luôn trả về JSON hợp lệ."
                    },
                    {"role": "user", "content": prompt}
                ]

            response = await self.client.chat.completions.create(
                model=self._get_active_model(),
                messages=messages,
                temperature=0.7,
                max_tokens=200
            )

            response_text = response.choices[0].message.content
            
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                suggestions = result.get("suggestions", [])
                if mode_normalized == "rewrite":
                    return self._normalize_rewrite_suggestions(
                        context=context,
                        original_text=original_text or context,
                        suggestions=suggestions,
                        max_suggestions=max_suggestions
                    )
                return self._normalize_suggestions(context, suggestions, max_suggestions)
            else:
                return self._get_mock_suggestions(
                    context=context,
                    max_suggestions=max_suggestions,
                    mode=mode_normalized,
                    original_text=original_text,
                    instruction=instruction
                )

        except Exception as e:
            logger.error(f"Chat API error ({self.api_provider}): {e}")
            return self._get_mock_suggestions(
                context=context,
                max_suggestions=max_suggestions,
                mode=mode,
                original_text=original_text,
                instruction=instruction
            )

    async def _get_gemini_suggestions(
        self,
        context: str,
        max_suggestions: int,
        suggestion_length: int,
        mode: str = "continuation",
        original_text: Optional[str] = None,
        instruction: Optional[str] = None
    ) -> List[Dict]:
        """Lấy suggestions từ Gemini (synchronous wrapper)"""
        try:
            mode_normalized = (mode or "continuation").strip().lower()
            if mode_normalized == "rewrite":
                source_text = (original_text or context or "").strip()
                user_instruction = (instruction or "").strip()
                prompt = f"""Bạn là trợ lý viết tiếng Việt chuyên VIẾT LẠI CÂU theo ngữ cảnh.
Nhiệm vụ: đề xuất {max_suggestions} phiên bản viết lại hay hơn cho câu gốc, nhưng vẫn GIỮ NGUYÊN ý nghĩa.

Ngữ cảnh xung quanh (để hiểu văn phong):
{context}

Câu gốc cần viết lại:
{source_text}

Yêu cầu chỉnh sửa của người dùng:
{user_instruction or "Không có yêu cầu bổ sung"}

Yêu cầu bắt buộc:
- Tuyệt đối không đổi nghĩa, không thêm thông tin mới làm lệch mục đích câu nói.
- Giữ nguyên ngôi xưng hô, sắc thái lịch sự/thân mật gần với câu gốc.
- Ưu tiên bám sát yêu cầu chỉnh sửa của người dùng nếu có.
- Viết tự nhiên, tránh các mẫu khuôn sáo lặp lại.
- Mỗi gợi ý là 1 câu hoàn chỉnh, khoảng {max(10, suggestion_length)} đến {max(18, suggestion_length + 10)} từ.
- Không dùng bullet, không thêm tiêu đề.
- Trả về JSON hợp lệ đúng cấu trúc dưới đây.

Định dạng JSON:
{{
    "suggestions": [
        {{"text": "câu viết lại 1", "confidence": 0.9, "reason": "vì sao cách diễn đạt này tốt hơn"}},
        {{"text": "câu viết lại 2", "confidence": 0.85, "reason": "vì sao cách diễn đạt này tốt hơn"}},
        {{"text": "câu viết lại 3", "confidence": 0.8, "reason": "vì sao cách diễn đạt này tốt hơn"}}
    ]
}}"""
            else:
                prompt = f"""Bạn là trợ lý viết tiếng Việt chuyên gợi ý VIẾT TIẾP.
Nhiệm vụ: đọc ngữ cảnh và đề xuất {max_suggestions} câu/đoạn NGẮN để tiếp nối mạch ý.

Ngữ cảnh hiện tại:
{context}

Yêu cầu bắt buộc:
- Chỉ viết phần tiếp theo, không lặp lại hoặc diễn giải lại nguyên văn ngữ cảnh.
- Mỗi gợi ý dài khoảng {suggestion_length} đến {suggestion_length + 8} từ.
- Giữ mạch logic với câu cuối của ngữ cảnh, tiếng Việt tự nhiên.
- Không dùng bullet, không thêm tiêu đề.
- Trả về JSON hợp lệ đúng cấu trúc dưới đây.

Định dạng JSON:
{{
    "suggestions": [
        {{"text": "phần viết tiếp 1", "confidence": 0.9}},
        {{"text": "phần viết tiếp 2", "confidence": 0.8}},
        {{"text": "phần viết tiếp 3", "confidence": 0.7}}
    ]
}}"""

            # Run in thread pool since Gemini API is sync
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.generate_content(prompt)
            )
            
            response_text = response.text
            
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                suggestions = result.get("suggestions", [])
                if mode_normalized == "rewrite":
                    return self._normalize_rewrite_suggestions(
                        context=context,
                        original_text=original_text or context,
                        suggestions=suggestions,
                        max_suggestions=max_suggestions
                    )
                return self._normalize_suggestions(context, suggestions, max_suggestions)
            else:
                return self._get_mock_suggestions(
                    context=context,
                    max_suggestions=max_suggestions,
                    mode=mode_normalized,
                    original_text=original_text,
                    instruction=instruction
                )

        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return self._get_mock_suggestions(
                context=context,
                max_suggestions=max_suggestions,
                mode=mode,
                original_text=original_text,
                instruction=instruction
            )

    def save_composition_action(
        self,
        db: Session,
        document_id: int,
        user_id: int,
        action_type: str,
        suggested_text: Optional[str] = None,
        original_text: Optional[str] = None,
        modified_text: Optional[str] = None,
        context: Optional[str] = None,
        accepted: int = 0
    ) -> Dict:
        """
        Lưu lịch sử soạn thảo (suggestion, edit, acceptance)

        Args:
            db: Database session
            document_id: ID của document
            user_id: ID của user
            action_type: 'suggestion', 'edit', 'acceptance'
            suggested_text: Text được gợi ý
            original_text: Text gốc
            modified_text: Text sau khi edit
            context: Ngữ cảnh
            accepted: 1 nếu accept, 0 nếu reject

        Returns:
            Dict với thông tin được lưu
        """
        try:
            history = CompositionHistory(
                document_id=document_id,
                user_id=user_id,
                action_type=action_type,
                suggested_text=suggested_text,
                original_text=original_text,
                modified_text=modified_text,
                context=context,
                accepted=accepted
            )
            db.add(history)
            db.commit()
            db.refresh(history)

            logger.info(f"Saved composition history: {history.id}")
            return {
                "id": history.id,
                "action_type": action_type,
                "created_at": history.created_at.isoformat()
            }

        except Exception as e:
            logger.error(f"Error saving composition history: {e}")
            db.rollback()
            return {}

    def save_document(
        self,
        db: Session,
        user_id: int,
        title: str,
        content: str,
        description: Optional[str] = None,
        document_id: Optional[int] = None
    ) -> Dict:
        """
        Lưu hoặc cập nhật document

        Args:
            db: Database session
            user_id: ID của user
            title: Tiêu đề tài liệu
            content: Nội dung tài liệu
            description: Mô tả tài liệu
            document_id: ID của document (nếu update)

        Returns:
            Dict với thông tin document
        """
        try:
            if document_id:
                # Cập nhật document hiện có
                doc = db.query(Document).filter(
                    Document.id == document_id,
                    Document.user_id == user_id
                ).first()
                
                if not doc:
                    logger.error(f"Document {document_id} not found")
                    return {}

                doc.title = title
                doc.content = content
                if description:
                    doc.description = description
                doc.updated_at = datetime.utcnow()
            else:
                # Tạo document mới
                doc = Document(
                    user_id=user_id,
                    title=title,
                    content=content,
                    description=description
                )
                db.add(doc)

            db.commit()
            db.refresh(doc)

            logger.info(f"Saved document: {doc.id}")
            return {
                "id": doc.id,
                "title": doc.title,
                "created_at": doc.created_at.isoformat(),
                "updated_at": doc.updated_at.isoformat()
            }

        except Exception as e:
            logger.error(f"Error saving document: {e}")
            db.rollback()
            return {}

    def get_document(
        self,
        db: Session,
        user_id: int,
        document_id: int
    ) -> Optional[Dict]:
        """
        Lấy document theo ID

        Args:
            db: Database session
            user_id: ID của user
            document_id: ID của document

        Returns:
            Dict với thông tin document hoặc None
        """
        try:
            doc = db.query(Document).filter(
                Document.id == document_id,
                Document.user_id == user_id
            ).first()

            if not doc:
                return None

            return {
                "id": doc.id,
                "title": doc.title,
                "content": doc.content,
                "description": doc.description,
                "created_at": doc.created_at.isoformat(),
                "updated_at": doc.updated_at.isoformat()
            }

        except Exception as e:
            logger.error(f"Error getting document: {e}")
            return None

    def list_documents(
        self,
        db: Session,
        user_id: int,
        limit: int = 20,
        offset: int = 0
    ) -> List[Dict]:
        """
        Liệt kê documents của user

        Args:
            db: Database session
            user_id: ID của user
            limit: Số lượng tối đa
            offset: Vị trí bắt đầu

        Returns:
            Danh sách dict chứa thông tin documents
        """
        try:
            docs = db.query(Document).filter(
                Document.user_id == user_id
            ).order_by(
                Document.updated_at.desc()
            ).offset(offset).limit(limit).all()

            return [
                {
                    "id": doc.id,
                    "title": doc.title,
                    "description": doc.description,
                    "created_at": doc.created_at.isoformat(),
                    "updated_at": doc.updated_at.isoformat(),
                    "content_preview": doc.content[:100] + "..." if len(doc.content) > 100 else doc.content
                }
                for doc in docs
            ]

        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            return []

    def delete_document(
        self,
        db: Session,
        user_id: int,
        document_id: int
    ) -> bool:
        """
        Xóa document

        Args:
            db: Database session
            user_id: ID của user
            document_id: ID của document

        Returns:
            True nếu thành công, False nếu thất bại
        """
        try:
            doc = db.query(Document).filter(
                Document.id == document_id,
                Document.user_id == user_id
            ).first()

            if not doc:
                return False

            db.delete(doc)
            db.commit()

            logger.info(f"Deleted document: {document_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            db.rollback()
            return False
