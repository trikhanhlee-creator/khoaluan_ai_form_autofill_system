"""
OpenRouter API Provider
Handles communication with OpenRouter AI services
"""
import requests
from typing import Dict, List, Optional, Any
import logging
from .config import AIConfig, ModelConfig

logger = logging.getLogger(__name__)


class OpenRouterProvider:
    """OpenRouter API client for AI operations"""
    
    def __init__(self):
        self.config = AIConfig()
        self.endpoint = self.config.ENDPOINTS["chat"]
        self.headers = self.config.HEADERS
        
    def _make_request(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make a request to OpenRouter API
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use (defaults to configured model)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters
            
        Returns:
            API response data
        """
        if not model:
            model = self.config.MODEL
            
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }
        
        try:
            response = requests.post(
                self.endpoint,
                headers=self.headers,
                json=payload,
                timeout=self.config.TIMEOUT
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenRouter API error: {str(e)}")
            raise
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        **kwargs
    ) -> str:
        """
        Send a chat message and get response
        
        Args:
            messages: Chat message history
            model: Optional model override
            **kwargs: Additional parameters
            
        Returns:
            Response text
        """
        response = self._make_request(messages, model=model, **kwargs)
        return response["choices"][0]["message"]["content"]
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        return self.config.AVAILABLE_MODELS
