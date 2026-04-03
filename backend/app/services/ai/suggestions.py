"""
Suggestions Service
Provides smart recommendations and suggestions for text passages
"""
from typing import Dict, List, Optional, Any
import logging
from ..providers import OpenRouterProvider, ModelConfig

logger = logging.getLogger(__name__)


class SuggestionsService:
    """Service for generating intelligent suggestions"""
    
    def __init__(self):
        self.provider = OpenRouterProvider()
        self.model = ModelConfig.SUGGESTIONS_MODEL
        self.temperature = ModelConfig.TEMPERATURES["suggestions"]
        self.max_tokens = ModelConfig.MAX_TOKENS["suggestions"]
    
    def generate_suggestions(
        self,
        text: str,
        suggestion_type: str = "general",
        count: int = 5
    ) -> Dict[str, Any]:
        """
        Generate suggestions for improving text
        
        Args:
            text: Text passage to suggest improvements for
            suggestion_type: Type of suggestions (general, grammar, style, clarity, etc.)
            count: Number of suggestions to generate
            
        Returns:
            List of suggestions
        """
        type_prompts = {
            "general": "Provide general improvement suggestions",
            "grammar": "Provide grammar and punctuation corrections",
            "clarity": "Provide suggestions to improve clarity and readability",
            "style": "Provide style and tone improvements",
            "conciseness": "Provide suggestions to make the text more concise",
            "engagement": "Provide suggestions to make the text more engaging",
        }
        
        prompt = type_prompts.get(suggestion_type, type_prompts["general"])
        
        full_prompt = f"""Text passage:
{text}

{prompt}

Please provide exactly {count} specific, actionable suggestions. Format each as:
- [Suggestion #]: [Your suggestion]
Include why each suggestion would help."""
        
        messages = [
            {"role": "system", "content": "You are a writing coach. Provide practical, constructive suggestions."},
            {"role": "user", "content": full_prompt}
        ]
        
        try:
            response = self.provider.chat(
                messages,
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return {
                "status": "success",
                "suggestion_type": suggestion_type,
                "suggestions": response,
                "count": count,
            }
        except Exception as e:
            logger.error(f"Suggestions service error: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
            }
    
    def suggest_alternatives(
        self,
        text: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Suggest alternative phrasings or wordings
        
        Args:
            text: Text segment to find alternatives for
            context: Surrounding context
            
        Returns:
            Alternative suggestions
        """
        context_info = f"Context: {context}\n\n" if context else ""
        
        prompt = f"""{context_info}Suggest 3-5 alternative ways to express:
"{text}"

For each alternative:
1. Provide the alternative phrasing
2. Explain when/why to use it
3. Rate its effectiveness (high/medium/low)"""
        
        messages = [
            {"role": "system", "content": "You are a language expert. Provide clear, practical alternatives."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.provider.chat(
                messages,
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return {
                "status": "success",
                "original": text,
                "alternatives": response,
            }
        except Exception as e:
            logger.error(f"Alternatives service error: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
            }
    
    def quick_suggestion(self, text: str) -> Dict[str, Any]:
        """
        Quick, single suggestion for text segment
        
        Args:
            text: Text to get suggestion for
            
        Returns:
            Single suggestion
        """
        messages = [
            {"role": "system", "content": "You are a writing assistant. Provide one concise improvement."},
            {"role": "user", "content": f"Suggest one improvement for: {text}"}
        ]
        
        try:
            response = self.provider.chat(
                messages,
                model=self.model,
                temperature=self.temperature,
                max_tokens=500
            )
            
            return {
                "status": "success",
                "suggestion": response,
            }
        except Exception as e:
            logger.error(f"Quick suggestion error: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
            }
