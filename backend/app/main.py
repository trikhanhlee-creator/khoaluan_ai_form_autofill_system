from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import os
from urllib.parse import quote

from app.core.config import settings
from app.core.logger import logger
from app.api.routes import suggestions, word, form_replacement, excel, composer, auth, form_edit, admin
from app.db.session import engine, Base, SessionLocal, get_db
from app.db.models import User, UserActivity

# Tạo các table nếu chưa tồn tại
Base.metadata.create_all(bind=engine)

# Khởi tạo FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="API tự động điền mẫu với gợi ý từ lịch sử sử dụng AI"
)


@app.on_event("startup")
async def ensure_legacy_schema_compatibility():
    """Patch legacy DB schema before serving requests."""
    db = SessionLocal()
    try:
        word.ensure_forms_schema_compatibility(db)
        recovered_admin = auth.ensure_default_admin_privilege(db)
        if recovered_admin:
            logger.info(f"Default admin check completed with user: {recovered_admin.username}")
        else:
            logger.warning("No active admin found and no fallback admin account could be recovered")
    except Exception as e:
        logger.error(f"Legacy schema compatibility check failed: {e}")
    finally:
        db.close()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(suggestions.router)
app.include_router(word.router)
app.include_router(form_replacement.router)
app.include_router(excel.router)
app.include_router(composer.router)
app.include_router(form_edit.router)
app.include_router(admin.router)

# Mount static files from backend/app/static
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Mount UI files from root ui folder
ui_dir = os.path.join(os.path.dirname(__file__), "..", "..", "ui")
if os.path.exists(ui_dir):
    app.mount("/ui", StaticFiles(directory=ui_dir), name="ui")


def _redirect_to_login(request: Request):
    next_path = quote(request.url.path, safe="")
    return RedirectResponse(url=f"/login?mode=login&next={next_path}", status_code=303)


def _resolve_feature_name(path: str) -> str:
    if path == "/":
        return "home"
    if path.startswith("/composer"):
        return "composer"
    if path.startswith("/word-upload"):
        return "word_upload"
    if path.startswith("/excel-data-form"):
        return "excel_data_form"
    if path.startswith("/excel-form"):
        return "excel_form"
    if path.startswith("/excel"):
        return "excel_upload"
    if path.startswith("/form"):
        return "form"
    if path.startswith("/user-account"):
        return "user_account"
    if path.startswith("/admin-dashboard"):
        return "admin_dashboard"
    if path.startswith("/admin-users"):
        return "admin_users"
    if path.startswith("/admin-forms"):
        return "admin_forms"
    if path.startswith("/admin-reports"):
        return "admin_reports"
    if path.startswith("/admin-audit-log"):
        return "admin_audit_log"
    if path.startswith("/admin-account"):
        return "admin_account"
    return "unknown"


def _record_user_activity(
    db: Session,
    user_id: int,
    request: Request,
    activity_type: str = "page_view",
    description: str = "",
):
    """Persist per-user website activity for auditing and personal history."""
    try:
        entry = UserActivity(
            user_id=user_id,
            activity_type=activity_type,
            feature=_resolve_feature_name(request.url.path),
            path=request.url.path,
            method=request.method,
            description=description or f"User accessed {request.url.path}",
        )
        db.add(entry)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.warning(f"Failed to record user activity: {e}")


def _authorize_user_ui(request: Request, db: Session):
    """Ensure logged-in users can access user functionality pages."""
    user = auth.get_authenticated_user_from_request(request, db)
    if not user:
        return None, _redirect_to_login(request)
    return user, None


def _authorize_admin_ui(request: Request, db: Session):
    """Ensure only admin users can access admin HTML pages."""
    user, auth_response = _authorize_user_ui(request, db)
    if auth_response:
        return None, auth_response
    if not user.is_admin:
        return None, RedirectResponse(url="/", status_code=303)
    return user, None


@app.get("/login", tags=["ui"])
async def login_page():
    """Serve the login page"""
    from fastapi.responses import HTMLResponse
    try:
        with open(os.path.join(static_dir, "login.html"), "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        logger.error(f"Error loading login.html: {e}")
        return HTMLResponse(content="<h1>Login page not found</h1>", status_code=404)


@app.get("/user-account", tags=["ui"])
async def user_account_page(request: Request, db: Session = Depends(get_db)):
    """Serve the user account management page"""
    from fastapi.responses import HTMLResponse

    user, auth_response = _authorize_user_ui(request, db)
    if auth_response:
        return auth_response

    _record_user_activity(db, user.id, request, description="Opened user account page")

    try:
        with open(os.path.join(static_dir, "user-account.html"), "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        logger.error(f"Error loading user-account.html: {e}")
        return HTMLResponse(content="<h1>User account page not found</h1>", status_code=404)


@app.get("/form", tags=["ui"])
async def form_page(request: Request, db: Session = Depends(get_db)):
    """Serve the form HTML page"""
    from fastapi.responses import HTMLResponse

    user, auth_response = _authorize_user_ui(request, db)
    if auth_response:
        return auth_response

    _record_user_activity(db, user.id, request, description="Opened form page")

    with open(os.path.join(static_dir, "form.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/excel", tags=["ui"])
async def excel_page(request: Request, db: Session = Depends(get_db)):
    """Serve the Excel upload page"""
    from fastapi.responses import HTMLResponse

    user, auth_response = _authorize_user_ui(request, db)
    if auth_response:
        return auth_response

    _record_user_activity(db, user.id, request, description="Opened Excel upload page")

    try:
        with open(os.path.join(static_dir, "excel-upload.html"), "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        logger.error(f"Error loading excel-upload.html: {e}")
        raise


@app.get("/word-upload", tags=["ui"])
async def word_upload_page(request: Request, db: Session = Depends(get_db)):
    """Serve the Word upload page"""
    from fastapi.responses import HTMLResponse

    user, auth_response = _authorize_user_ui(request, db)
    if auth_response:
        return auth_response

    _record_user_activity(db, user.id, request, description="Opened Word upload page")

    try:
        with open(os.path.join(static_dir, "word-upload.html"), "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        logger.error(f"Error loading word-upload.html: {e}")
        raise


@app.get("/excel-form/{session_id}", tags=["ui"])
async def excel_form_page(session_id: str, request: Request, db: Session = Depends(get_db)):
    """Serve the Excel form page"""
    from fastapi.responses import HTMLResponse

    user, auth_response = _authorize_user_ui(request, db)
    if auth_response:
        return auth_response

    _record_user_activity(db, user.id, request, description=f"Opened Excel form session {session_id}")

    try:
        with open(os.path.join(static_dir, "excel-form.html"), "r", encoding="utf-8") as f:
            content = f.read()
            # Inject session_id into the page
            content = content.replace("{{SESSION_ID}}", session_id)
            return HTMLResponse(content=content)
    except Exception as e:
        logger.error(f"Error loading excel-form.html: {e}")
        raise


@app.get("/excel-data-form/{session_id}", tags=["ui"])
async def excel_data_form_page(session_id: str, request: Request, db: Session = Depends(get_db)):
    """Serve the Excel data auto-fill form page"""
    from fastapi.responses import HTMLResponse

    user, auth_response = _authorize_user_ui(request, db)
    if auth_response:
        return auth_response

    _record_user_activity(db, user.id, request, description=f"Opened Excel data form session {session_id}")

    try:
        with open(os.path.join(static_dir, "excel-data-form.html"), "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        logger.error(f"Error loading excel-data-form.html: {e}")
        raise


@app.get("/", tags=["ui"])
async def root(request: Request, db: Session = Depends(get_db)):
    """Root endpoint - serve main menu"""
    from fastapi.responses import HTMLResponse

    user, auth_response = _authorize_user_ui(request, db)
    if auth_response:
        return auth_response

    _record_user_activity(db, user.id, request, description="Opened main menu")

    try:
        with open(os.path.join(static_dir, "menu.html"), "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except:
        return {
            "message": "AutoFill AI System API",
            "version": "1.0.0",
            "status": "running",
            "menu": "/static/menu.html"
        }

@app.get("/composer", tags=["ui"])
async def composer_page(request: Request, db: Session = Depends(get_db)):
    """Serve the document composer page"""
    from fastapi.responses import HTMLResponse

    user, auth_response = _authorize_user_ui(request, db)
    if auth_response:
        return auth_response

    _record_user_activity(db, user.id, request, description="Opened document composer")

    try:
        with open(os.path.join(static_dir, "composer.html"), "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        logger.error(f"Error loading composer.html: {e}")
        raise


# ==================== ADMIN PAGES ====================

@app.get("/admin-dashboard", tags=["ui"])
async def admin_dashboard_page(request: Request, db: Session = Depends(get_db)):
    """Serve the admin dashboard page"""
    from fastapi.responses import HTMLResponse

    user, auth_response = _authorize_admin_ui(request, db)
    if auth_response:
        return auth_response

    _record_user_activity(db, user.id, request, activity_type="feature_access", description="Opened admin dashboard")

    try:
        with open(os.path.join(static_dir, "admin-dashboard.html"), "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        logger.error(f"Error loading admin-dashboard.html: {e}")
        return HTMLResponse(content="<h1>Admin dashboard page not found</h1>", status_code=404)


@app.get("/admin-users", tags=["ui"])
async def admin_users_page(request: Request, db: Session = Depends(get_db)):
    """Serve the admin users management page"""
    from fastapi.responses import HTMLResponse

    user, auth_response = _authorize_admin_ui(request, db)
    if auth_response:
        return auth_response

    _record_user_activity(db, user.id, request, activity_type="feature_access", description="Opened admin users")

    try:
        with open(os.path.join(static_dir, "admin-users.html"), "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        logger.error(f"Error loading admin-users.html: {e}")
        return HTMLResponse(content="<h1>Admin users page not found</h1>", status_code=404)


@app.get("/admin-forms", tags=["ui"])
async def admin_forms_page(request: Request, db: Session = Depends(get_db)):
    """Serve the admin forms management page"""
    from fastapi.responses import HTMLResponse

    user, auth_response = _authorize_admin_ui(request, db)
    if auth_response:
        return auth_response

    _record_user_activity(db, user.id, request, activity_type="feature_access", description="Opened admin forms")

    try:
        with open(os.path.join(static_dir, "admin-forms.html"), "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        logger.error(f"Error loading admin-forms.html: {e}")
        return HTMLResponse(content="<h1>Admin forms page not found</h1>", status_code=404)


@app.get("/admin-reports", tags=["ui"])
async def admin_reports_page(request: Request, db: Session = Depends(get_db)):
    """Serve the admin reports page"""
    from fastapi.responses import HTMLResponse

    user, auth_response = _authorize_admin_ui(request, db)
    if auth_response:
        return auth_response

    _record_user_activity(db, user.id, request, activity_type="feature_access", description="Opened admin reports")

    try:
        with open(os.path.join(static_dir, "admin-reports.html"), "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        logger.error(f"Error loading admin-reports.html: {e}")
        return HTMLResponse(content="<h1>Admin reports page not found</h1>", status_code=404)


@app.get("/admin-audit-log", tags=["ui"])
async def admin_audit_log_page(request: Request, db: Session = Depends(get_db)):
    """Serve the admin audit log page"""
    from fastapi.responses import HTMLResponse

    user, auth_response = _authorize_admin_ui(request, db)
    if auth_response:
        return auth_response

    _record_user_activity(db, user.id, request, activity_type="feature_access", description="Opened admin audit log")

    try:
        with open(os.path.join(static_dir, "admin-audit-log.html"), "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        logger.error(f"Error loading admin-audit-log.html: {e}")
        return HTMLResponse(content="<h1>Admin audit log page not found</h1>", status_code=404)


@app.get("/admin-account", tags=["ui"])
async def admin_account_page(request: Request, db: Session = Depends(get_db)):
    """Serve the admin account settings page"""
    from fastapi.responses import HTMLResponse

    user, auth_response = _authorize_admin_ui(request, db)
    if auth_response:
        return auth_response

    _record_user_activity(db, user.id, request, activity_type="feature_access", description="Opened admin account")

    try:
        with open(os.path.join(static_dir, "admin-account.html"), "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        logger.error(f"Error loading admin-account.html: {e}")
        return HTMLResponse(content="<h1>Admin account page not found</h1>", status_code=404)

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
