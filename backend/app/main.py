from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.core.logger import logger
from app.api.routes import suggestions, word
from app.db.session import engine, Base

# Tạo các table nếu chưa tồn tại
Base.metadata.create_all(bind=engine)

# Khởi tạo FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="API tự động điền mẫu với gợi ý từ lịch sử sử dụng AI"
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(suggestions.router)
app.include_router(word.router)

# Mount static files from backend/app/static
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Mount UI files from root ui folder
ui_dir = os.path.join(os.path.dirname(__file__), "..", "..", "ui")
if os.path.exists(ui_dir):
    app.mount("/ui", StaticFiles(directory=ui_dir), name="ui")


@app.get("/form", tags=["ui"])
async def form_page():
    """Serve the form HTML page"""
    from fastapi.responses import HTMLResponse
    with open(os.path.join(static_dir, "form.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/", tags=["health"])
async def root():
    """Root endpoint - serve word upload page"""
    from fastapi.responses import HTMLResponse
    try:
        with open(os.path.join(static_dir, "word-upload.html"), "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except:
        return {
            "message": "AutoFill AI System API",
            "version": "1.0.0",
            "status": "running",
            "ui": "/static/word-upload.html"
        }


@app.get("/health", tags=["health"])
async def health():
    """Health check endpoint"""
    logger.info("Health check called")
    return {
        "status": "ok",
        "service": "autofill-ai-system"
    }


@app.get("/api/v1", tags=["info"])
async def api_info():
    """API info endpoint"""
    logger.info("API info called")
    return {
        "name": settings.PROJECT_NAME,
        "version": "1.0.0",
        "endpoints": {
            "suggestions": "/api/suggestions",
            "suggestions_history": "/api/suggestions/history",
            "field_stats": "/api/suggestions/stats"
        }
    }


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {settings.PROJECT_NAME} server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
