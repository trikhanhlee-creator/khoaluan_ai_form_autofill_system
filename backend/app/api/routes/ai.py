"""
AI API Routes
Endpoints for thinking and suggestions services
"""
from flask import Blueprint, request, jsonify
from app.services.ai import ThinkingService, SuggestionsService
import logging

logger = logging.getLogger(__name__)

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')


# ============ THINKING ROUTES ============

@ai_bp.route('/think/analyze', methods=['POST'])
def analyze_text():
    """
    Deep analysis of text passage
    
    Request body:
    {
        "text": "paragraph to analyze",
        "focus_areas": ["clarity", "grammar"],  # optional
        "context": "additional context"  # optional
    }
    """
    try:
        data = request.json
        text = data.get('text')
        
        if not text:
            return jsonify({"error": "text field is required"}), 400
        
        service = ThinkingService()
        result = service.analyze_text(
            text=text,
            focus_areas=data.get('focus_areas'),
            context=data.get('context')
        )
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Analyze text error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@ai_bp.route('/think/insights', methods=['POST'])
def generate_insights():
    """
    Generate insights about text
    
    Request body:
    {
        "text": "text to analyze",
        "insight_type": "writing_quality"  # optional
    }
    """
    try:
        data = request.json
        text = data.get('text')
        
        if not text:
            return jsonify({"error": "text field is required"}), 400
        
        service = ThinkingService()
        result = service.generate_insights(
            text=text,
            insight_type=data.get('insight_type', 'general')
        )
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Generate insights error: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ============ SUGGESTIONS ROUTES ============

@ai_bp.route('/suggest/improvements', methods=['POST'])
def get_suggestions():
    """
    Get improvement suggestions for text
    
    Request body:
    {
        "text": "text to improve",
        "type": "clarity",  # optional: grammar, style, clarity, conciseness, engagement
        "count": 5  # optional: number of suggestions
    }
    """
    try:
        data = request.json
        text = data.get('text')
        
        if not text:
            return jsonify({"error": "text field is required"}), 400
        
        service = SuggestionsService()
        result = service.generate_suggestions(
            text=text,
            suggestion_type=data.get('type', 'general'),
            count=data.get('count', 5)
        )
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Get suggestions error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@ai_bp.route('/suggest/alternatives', methods=['POST'])
def get_alternatives():
    """
    Get alternative phrasings
    
    Request body:
    {
        "text": "phrase to rephrase",
        "context": "surrounding context"  # optional
    }
    """
    try:
        data = request.json
        text = data.get('text')
        
        if not text:
            return jsonify({"error": "text field is required"}), 400
        
        service = SuggestionsService()
        result = service.suggest_alternatives(
            text=text,
            context=data.get('context')
        )
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Get alternatives error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@ai_bp.route('/suggest/quick', methods=['POST'])
def quick_suggestion():
    """
    Quick suggestion for text segment
    
    Request body:
    {
        "text": "text segment"
    }
    """
    try:
        data = request.json
        text = data.get('text')
        
        if not text:
            return jsonify({"error": "text field is required"}), 400
        
        service = SuggestionsService()
        result = service.quick_suggestion(text)
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Quick suggestion error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@ai_bp.route('/models', methods=['GET'])
def list_models():
    """Get available models"""
    try:
        service = ThinkingService()
        models = service.provider.get_available_models()
        
        return jsonify({
            "status": "success",
            "models": models,
            "count": len(models)
        })
    
    except Exception as e:
        logger.error(f"List models error: {str(e)}")
        return jsonify({"error": str(e)}), 500
