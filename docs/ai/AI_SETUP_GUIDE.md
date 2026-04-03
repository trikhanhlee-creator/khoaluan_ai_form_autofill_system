# 🚀 AI API Management System - Quick Start Guide

## 📦 What Was Created

Your new AI API management system includes:

### Directory Structure

```
backend/
├── app/
│   ├── api/
│   │   └── providers/
│   │       ├── __init__.py
│   │       ├── config.py          # Configuration management
│   │       └── openrouter.py      # OpenRouter API client
│   │
│   ├── services/
│   │   └── ai/
│   │       ├── __init__.py
│   │       ├── thinking.py        # Deep analysis service
│   │       └── suggestions.py     # Suggestions service
│   │
│   └── api/routes/
│       └── ai.py                  # API endpoints (NEW)
│
├── .env.example                   # Environment template
└── test_ai_services.py            # Test suite

```

## ⚙️ Setup Steps

### 1. **Configure Environment**

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# OPENROUTER_API_KEY=your_actual_key_here
```

### 2. **Install Dependencies**

```bash
pip install python-dotenv requests
```

Or update your `requirements.txt`:

```
requests>=2.31.0
python-dotenv>=1.0.0
```

### 3. **Load Environment Variables**

Update [backend/app/main.py](./backend/app/main.py) to load environment at startup:

```python
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
```

### 4. **Register AI Routes**

Update [backend/app/main.py](./backend/app/main.py) to register the AI blueprint:

```python
from app.api.routes.ai import ai_bp

# Register blueprint
app.register_blueprint(ai_bp)
```

## 🧪 Test the Setup

```bash
cd backend
python test_ai_services.py
```

Expected output shows successful calls to:

- ✓ Text analysis
- ✓ Insights generation
- ✓ Suggestions generation
- ✓ Alternative suggestions
- ✓ Quick suggestions

## 🔌 API Endpoints

Once registered, you'll have these endpoints:

### Thinking Endpoints

```
POST /api/ai/think/analyze
POST /api/ai/think/insights
```

### Suggestions Endpoints

```
POST /api/ai/suggest/improvements
POST /api/ai/suggest/alternatives
POST /api/ai/suggest/quick
```

### Utility Endpoints

```
GET /api/ai/models
```

## 📝 Usage Examples

### Using Services Directly (Python)

```python
from app.services.ai import ThinkingService, SuggestionsService

# Thinking service
thinking = ThinkingService()
analysis = thinking.analyze_text("Your text here")

# Suggestions service
suggestions = SuggestionsService()
result = suggestions.generate_suggestions("Your text")
```

### Using API Endpoints (cURL/Fetch)

```bash
# Get suggestions
curl -X POST http://localhost:5000/api/ai/suggest/improvements \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The big giant elephant was very large",
    "type": "clarity",
    "count": 5
  }'

# Get analysis
curl -X POST http://localhost:5000/api/ai/think/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your paragraph here",
    "focus_areas": ["clarity", "grammar"]
  }'
```

## 🔐 Security Checklist

- [ ] API key set in `.env` (not committed to git)
- [ ] `.env` file added to `.gitignore`
- [ ] `.env.example` has placeholder values
- [ ] API key rotated/regenerated (your key was exposed!)
- [ ] No hardcoded API keys in source files
- [ ] All secrets loaded from environment variables

## 📊 Configuration

### Available Models

From OpenRouter (via [config.py](./backend/app/api/providers/config.py)):

| Model | Best For | Speed | Cost |
|-------|----------|-------|------|
| `openai/gpt-4o` | Deep analysis | Slow | High |
| `openai/gpt-4o-mini` | Quick suggestions | Fast | Low |
| `google/gemini-2.0-flash-exp:free` | General tasks | Very Fast | Free |
| `anthropic/claude-3-haiku` | Lightweight | Fast | Low |

### Temperature & Tokens

Configured per service in `ModelConfig`:

- **Thinking**: Temperature 0.7, 2000 tokens (creative)
- **Suggestions**: Temperature 0.5, 1500 tokens (balanced)

## 🐛 Troubleshooting

### "Module not found" Error

```bash
pip install -r requirements.txt
cd backend
```

### "API Key not found" Error

Check that:
1. `.env` file exists in `backend/` directory
2. `OPENROUTER_API_KEY` is set correctly
3. `dotenv` is loaded in `main.py`

### API Request Fails

- Verify API key is active (check OpenRouter dashboard)
- Check internet connection
- Review error response for specific issue
- Check logs: `backend/logs/app.log`

## 📚 Documentation

- [AI_API_MANAGEMENT.md](./AI_API_MANAGEMENT.md) - Detailed documentation
- [backend/app/api/providers/config.py](./backend/app/api/providers/config.py) - Configuration
- [backend/app/api/providers/openrouter.py](./backend/app/api/providers/openrouter.py) - API client
- [backend/app/services/ai/thinking.py](./backend/app/services/ai/thinking.py) - Thinking service
- [backend/app/services/ai/suggestions.py](./backend/app/services/ai/suggestions.py) - Suggestions service
- [backend/app/api/routes/ai.py](./backend/app/api/routes/ai.py) - API routes

## 🎯 Next Steps

1. ✅ Setup environment variables
2. ✅ Install dependencies
3. ✅ Run tests: `python test_ai_services.py`
4. ✅ Update `main.py` to register routes
5. ✅ Test API endpoints
6. ✅ Integrate with your frontend
7. ✅ Monitor usage and costs

## 💡 Tips

- Use environment variables for all configuration
- Cache results when possible to save API costs
- Monitor token usage in logs
- Use faster models (gpt-4o-mini) for suggestions
- Use powerful models (gpt-4o) only for complex analysis

---

**Need help?** Check the documentation files or review the source code comments.
