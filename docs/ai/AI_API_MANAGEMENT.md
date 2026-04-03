# AI API Management Documentation

## 📁 Directory Structure

```
backend/
├── app/
│   ├── api/
│   │   └── providers/          # API Provider implementations
│   │       ├── config.py       # Configuration management
│   │       ├── openrouter.py   # OpenRouter API client
│   │       └── __init__.py
│   │
│   └── services/
│       └── ai/                 # AI Services
│           ├── thinking.py     # Deep analysis & thinking
│           ├── suggestions.py  # Suggestions & recommendations
│           └── __init__.py
```

## 🔧 Setup

### 1. Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` with your actual API key:

```
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxx
```

### 2. Update requirements.txt

Add requests library if not already present:

```
requests>=2.31.0
python-dotenv>=1.0.0
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 💡 Usage Examples

### Thinking Service

```python
from app.services.ai import ThinkingService

thinking = ThinkingService()

# Deep analysis of text
result = thinking.analyze_text(
    text="Your text here",
    focus_areas=["clarity", "structure"],
    context="Academic paper"
)
print(result["analysis"])

# Generate specific insights
insights = thinking.generate_insights(
    text="Your text",
    insight_type="writing_quality"
)
```

### Suggestions Service

```python
from app.services.ai import SuggestionsService

suggestions = SuggestionsService()

# Generate improvement suggestions
result = suggestions.generate_suggestions(
    text="Your text here",
    suggestion_type="clarity",
    count=5
)
print(result["suggestions"])

# Get alternative phrasings
alts = suggestions.suggest_alternatives(
    text="phrase to rephrase",
    context="surrounding context"
)

# Quick single suggestion
quick = suggestions.quick_suggestion("Your text segment")
```

## 🔑 Available Models

From OpenRouter:

- **Powerful**: `openai/gpt-4o` (for thinking/analysis)
- **Balanced**: `openai/gpt-4o-mini` (for suggestions)
- **Fast & Free**: `google/gemini-2.0-flash-exp:free`
- **Creative**: `google/gemini-pro`
- **Lightweight**: `anthropic/claude-3-haiku`, `meta-llama/llama-3.1-8b-instruct:free`

## 📊 Configuration Options

### Thinking Service

- **Model**: `openai/gpt-4o` (more capable)
- **Temperature**: 0.7 (creative analysis)
- **Max Tokens**: 2000

### Suggestions Service

- **Model**: `openai/gpt-4o-mini` (faster)
- **Temperature**: 0.5 (balanced)
- **Max Tokens**: 1500

Customize in [config.py](./app/api/providers/config.py)

## 🚨 Security

- **Never commit `.env` file** - it contains sensitive API keys
- Use environment variables for all secrets
- Rotate API keys regularly
- Monitor API usage and costs on OpenRouter dashboard

## 📝 Integration with Routes

Create API endpoints in [api/routes/ai.py](./app/api/routes/ai.py):

```python
from flask import Blueprint, request, jsonify
from app.services.ai import ThinkingService, SuggestionsService

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/api/thinking', methods=['POST'])
def think():
    data = request.json
    service = ThinkingService()
    result = service.analyze_text(
        text=data.get('text'),
        focus_areas=data.get('focus_areas')
    )
    return jsonify(result)

@ai_bp.route('/api/suggestions', methods=['POST'])
def suggest():
    data = request.json
    service = SuggestionsService()
    result = service.generate_suggestions(
        text=data.get('text'),
        suggestion_type=data.get('type', 'general')
    )
    return jsonify(result)
```

## 🐛 Error Handling

All services return a response dict with status:

```python
{
    "status": "success" | "error",
    "message": "error message if failed",
    # ... service-specific fields
}
```

Check `status` before using results.

## 💰 Cost Optimization

- Use `gpt-4o-mini` for suggestions (cheaper)
- Use `gpt-4o` only for complex thinking tasks
- Use free models when available
- Monitor token usage in API logs
