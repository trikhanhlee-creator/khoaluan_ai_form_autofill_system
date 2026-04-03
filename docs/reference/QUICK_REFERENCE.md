# ⚡ AI API Management - Quick Reference

## 🎯 What You Now Have

A complete **API management system** for:
- ✅ Deep text analysis (thinking service)
- ✅ Smart suggestions (suggestions service)
- ✅ Multiple AI models via OpenRouter
- ✅ RESTful API endpoints
- ✅ Secure configuration management
- ✅ Error handling & logging

---

## 🚀 Step-by-Step Setup (5 minutes)

### 1️⃣ Configure API Key
```bash
# Copy example
cp backend/.env.example backend/.env

# Edit backend/.env:
# OPENROUTER_API_KEY=your_new_key_here
# (Generate new key at https://openrouter.ai)
```

### 2️⃣ Install Dependencies
```bash
pip install python-dotenv requests
```

### 3️⃣ Update main.py
```python
# At top of backend/app/main.py
from dotenv import load_dotenv
from app.api.routes.ai import ai_bp

# After creating Flask app
load_dotenv()
app.register_blueprint(ai_bp)
```

### 4️⃣ Test Setup
```bash
cd backend
python test_ai_services.py
```

### 5️⃣ Use It!
**Python:**
```python
from app.services.ai import ThinkingService, SuggestionsService

# Analyze text
thinking = ThinkingService()
analysis = thinking.analyze_text("Your text here")

# Get suggestions
suggestions = SuggestionsService()
result = suggestions.generate_suggestions("Your text")
```

**API (HTTP):**
```bash
curl -X POST http://localhost:5000/api/ai/suggest/improvements \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text", "type": "clarity", "count": 5}'
```

---

## 📚 API Endpoints

### Thinking Endpoints
```
POST /api/ai/think/analyze
  body: { "text": "...", "focus_areas": [...], "context": "..." }

POST /api/ai/think/insights
  body: { "text": "...", "insight_type": "writing_quality|clarity|tone|..." }
```

### Suggestion Endpoints
```
POST /api/ai/suggest/improvements
  body: { "text": "...", "type": "clarity|grammar|style|...", "count": 5 }

POST /api/ai/suggest/alternatives
  body: { "text": "...", "context": "..." }

POST /api/ai/suggest/quick
  body: { "text": "..." }
```

### Utility
```
GET /api/ai/models
  returns: { "models": [...], "count": ... }
```

---

## 📁 File Structure

```
backend/
├── app/api/providers/        ← NEW: API management
│   ├── config.py             (configuration)
│   └── openrouter.py         (API client)
├── app/services/ai/          ← NEW: AI services
│   ├── thinking.py           (analysis)
│   └── suggestions.py        (recommendations)
├── app/api/routes/
│   └── ai.py                 ← NEW: endpoints
├── .env.example              ← NEW: config template
├── .env                       ← CREATE: add your key here
├── .gitignore                ← NEW: don't commit .env
└── test_ai_services.py       ← NEW: test suite
```

---

## 🔐 Security

### ✅ Do This
- Store API key in `.env`
- Add `.env` to `.gitignore`
- Commit `.env.example` with placeholders
- Load environment at startup
- Rotate key regularly

### ❌ Don't Do This
- Hardcode API keys
- Commit `.env` file
- Share API keys in messages
- Log sensitive data

### ⚠️ Right Now
1. **Regenerate your exposed API key**
   - Go to https://openrouter.ai
   - Revoke old key
   - Create new key
   - Update `.env`

---

## 🧪 Testing

```bash
# Run complete test suite
cd backend
python test_ai_services.py

# Expected output:
# ✓ Text analysis successful
# ✓ Insights generated successfully
# ✓ Suggestions generated successfully
# ✓ Alternatives suggested successfully
# ✓ Quick suggestion generated successfully
```

---

## 📊 Service Features

### ThinkingService
```python
thinking = ThinkingService()

# Deep analysis
thinking.analyze_text(
    text="...",
    focus_areas=["clarity", "grammar"],
    context="academic paper"
)

# Insights by type
thinking.generate_insights(
    text="...",
    insight_type="writing_quality"  # or: clarity, readability, structure, tone
)
```

### SuggestionsService
```python
suggestions = SuggestionsService()

# Multiple suggestions
suggestions.generate_suggestions(
    text="...",
    suggestion_type="clarity",  # or: grammar, style, conciseness, engagement
    count=5
)

# Alternative phrasings
suggestions.suggest_alternatives(
    text="phrase to replace",
    context="surrounding text"
)

# Quick single suggestion
suggestions.quick_suggestion("Your text")
```

---

## 🎨 Customization

### Change Default Model
Edit `backend/app/api/providers/config.py`:
```python
MODEL = os.getenv("DEFAULT_MODEL", "openai/gpt-4o")
```

### Change Temperature/Tokens
Edit `backend/app/api/providers/config.py`:
```python
TEMPERATURES = {
    "thinking": 0.7,      # More random
    "suggestions": 0.5,   # Balanced
}

MAX_TOKENS = {
    "thinking": 2000,
    "suggestions": 1500,
}
```

### Available Models
```
- openai/gpt-4o              (most capable, highest cost)
- openai/gpt-4o-mini         (balanced, lower cost) ← DEFAULT
- google/gemini-2.0-flash    (very fast, free)
- anthropic/claude-3-haiku   (lightweight)
- meta-llama/llama-3.1-8b    (open source, free)
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Module not found" | `pip install -r requirements.txt` |
| "API Key not found" | Check `.env` file exists and has key |
| "Connection error" | Verify internet connection |
| "401 Unauthorized" | API key is invalid or expired |
| "Rate limited" | Wait or upgrade OpenRouter plan |

---

## 💡 Pro Tips

1. **Cache results** - Save API responses to avoid duplicate calls
2. **Use fast models** - Use `gpt-4o-mini` for suggestions
3. **Batch requests** - Send multiple requests together when possible
4. **Monitor costs** - Log token usage from API responses
5. **Set timeouts** - Prevent hanging requests (default: 30s)

---

## 📞 Documentation

- **[AI_API_MANAGEMENT.md](./AI_API_MANAGEMENT.md)** - Full documentation
- **[AI_SETUP_GUIDE.md](./AI_SETUP_GUIDE.md)** - Setup guide
- **[AI_SYSTEM_SUMMARY.md](./AI_SYSTEM_SUMMARY.md)** - Files summary

---

## ✨ What's Next?

1. ✅ Copy `.env.example` to `.env`
2. ✅ Add your API key
3. ✅ Install dependencies
4. ✅ Update `main.py`
5. ✅ Run tests
6. ✅ Deploy endpoints
7. ✅ Integrate with UI

---

**Ready to go! 🚀**
