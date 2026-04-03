"""
Thinking Service
Provides deep analysis and reasoning for text passages
"""
from typing import Dict, List, Optional, Any
import logging
from ..providers import OpenRouterProvider, ModelConfig

logger = logging.getLogger(__name__)


class ThinkingService:
    """Service for deep analysis and thinking operations"""
    
    def __init__(self):
        self.provider = OpenRouterProvider()
        self.model = ModelConfig.THINKING_MODEL
        self.temperature = ModelConfig.TEMPERATURES["thinking"]
        self.max_tokens = ModelConfig.MAX_TOKENS["thinking"]
    
    def analyze_text(
        self,
        text: str,
        focus_areas: Optional[List[str]] = None,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform deep analysis on text passage
        
        Args:
            text: Text to analyze
            focus_areas: Specific areas to focus on (e.g., ["clarity", "grammar", "tone"])
            context: Additional context about the text
            
        Returns:
            Analysis results with insights
        """
        focus_prompt = ""
        if focus_areas:
            focus_prompt = f"Focus on these areas: {', '.join(focus_areas)}."
        
        context_prompt = ""
        if context:
            context_prompt = f"Context: {context}"
        
        prompt = f"""Analyze the following text passage in depth:

{context_prompt}

Text to analyze:
{text}

{focus_prompt}

Provide:
1. Key themes and main ideas
2. Structure and flow analysis
3. Strengths and weaknesses
4. Suggestions for improvement
5. Overall assessment"""
        
        messages = [
            {"role": "system", "content": "You are an expert text analyst. Provide deep, thoughtful analysis."},
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
                "analysis": response,
                "model_used": self.model,
            }
        except Exception as e:
            logger.error(f"Thinking service error: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
            }
    
    def generate_insights(
        self,
        text: str,
        insight_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Generate specific insights about text
        
        Args:
            text: Text passage
            insight_type: Type of insight (general, writing_quality, readability, etc.)
            
        Returns:
            Generated insights
        """
        prompts = {
            "general": "Provide general insights about this text",
            "writing_quality": "Analyze the writing quality, style, and effectiveness",
            "readability": "Assess readability, clarity, and audience comprehension",
            "structure": "Analyze the logical structure and organization",
            "tone": "Evaluate the tone, voice, and emotional impact",
        }
        
        prompt = prompts.get(insight_type, prompts["general"])
        
        messages = [
            {"role": "system", "content": "You are a writing expert. Provide insightful, constructive feedback."},
            {"role": "user", "content": f"{prompt}:\n\n{text}"}
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
                "insight_type": insight_type,
                "insights": response,
            }
        except Exception as e:
            logger.error(f"Insight generation error: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
            }
