"""
Authentication routes for user login
"""
from fastapi import APIRouter, HTTPException, Response, Request, Depends
from fastapi.responses import JSONResponse, HTMLResponse
import os
from typing import Optional
from datetime import datetime, timedelta
import json
import base64
import hashlib
import hmac
import time
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.db.session import get_db
from app.db.models import User, UserActivity
from app.core.security import get_password_hash, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])

sessions = {}  # session_id -> user_info
user_profile_cache = {}  # user_id -> profile extras not mapped in current DB schema

SESSION_TTL_SECONDS = int(os.getenv("SESSION_TTL_SECONDS", str(60 * 60 * 24 * 2)))  # 2 days inactivity
GUEST_MODE_COOKIE = "guest_mode"


def _get_session_secret() -> str:
    return os.getenv("SESSION_SECRET", "autofill-dev-session-secret")


def generate_session_token(user_id: int) -> str:
    issued_at = int(time.time())
    payload = f"{user_id}:{issued_at}"
    signature = hmac.new(
        _get_session_secret().encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    raw = f"{payload}:{signature}".encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("utf-8")


def verify_session_token(token: Optional[str]) -> Optional[int]:
    if not token:
        return None

    try:
        decoded = base64.urlsafe_b64decode(token.encode("utf-8")).decode("utf-8")
        user_id_str, issued_at_str, signature = decoded.split(":", 2)

        payload = f"{user_id_str}:{issued_at_str}"
        expected_signature = hmac.new(
            _get_session_secret().encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            return None

        issued_at = int(issued_at_str)
        if (int(time.time()) - issued_at) > SESSION_TTL_SECONDS:
            return None

        user_id = int(user_id_str)
        return user_id if user_id > 0 else None
    except Exception:
        return None


def _set_session_cookie(response: Response, user_id: int) -> str:
    """Issue a signed session token and attach it as a browser-session cookie."""
    session_id = generate_session_token(user_id)
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="Lax"
    )
    return session_id


def _set_guest_mode_cookie(response: Response) -> None:
    """Mark browser as guest mode using a session cookie (clears on browser close)."""
    response.set_cookie(
        key=GUEST_MODE_COOKIE,
        value="1",
        httponly=False,
        samesite="Lax"
    )


def _clear_guest_mode_cookie(response: Response) -> None:
    response.delete_cookie(GUEST_MODE_COOKIE)


def get_authenticated_user_from_request(request: Request, db: Session) -> Optional[User]:
    token = request.cookies.get("session_id")
    user_id = verify_session_token(token)
    if not user_id:
        return None

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        return None

    return user


def ensure_default_admin_privilege(db: Session) -> Optional[User]:
    """Recover default admin role when the system has no active admin."""
    active_admin = db.query(User).filter(
        User.is_admin == True,
        User.is_active == True,
    ).first()
    if active_admin:
        return active_admin

    fallback_admin = db.query(User).filter(
        or_(
            func.lower(User.username) == "admin",
            func.lower(User.email) == "admin@example.com",
        )
    ).order_by(User.id.asc()).first()

    if not fallback_admin:
        return None

    fallback_admin.is_admin = True
    fallback_admin.is_active = True
    fallback_admin.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(fallback_admin)
    return fallback_admin

def generate_session_id():
    """Generate a simple session ID"""
    import uuid
    return str(uuid.uuid4())


@router.post("/guest/start")
async def start_guest_mode():
    """Start guest mode session (browser-session scoped)."""
    response = JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": "Đã bật chế độ dùng miễn phí. Lịch sử sẽ mất khi tắt trình duyệt.",
            "mode": "guest",
        }
    )
    _set_guest_mode_cookie(response)
    return response

@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    """Handle user login"""
    try:
        data = await request.json()
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        
        if not username or not password:
            return JSONResponse(
                status_code=400,
                content={"error": "Tên đăng nhập và mật khẩu không được để trống"}
            )
        
        # Support login by username or email
        user = db.query(User).filter(
            or_(
                func.lower(User.username) == username.lower(),
                func.lower(User.email) == username.lower(),
            )
        ).first()
        if not user:
            return JSONResponse(
                status_code=401,
                content={"error": "Tên đăng nhập hoặc mật khẩu không chính xác"}
            )

        # Support legacy plaintext values while migrating existing data
        password_ok = verify_password(password, user.password_hash) or (user.password_hash == password)
        if not password_ok:
            return JSONResponse(
                status_code=401,
                content={"error": "Tên đăng nhập hoặc mật khẩu không chính xác"}
            )

        user.last_login = datetime.utcnow()
        db.add(UserActivity(
            user_id=user.id,
            activity_type="login",
            feature="auth",
            path="/login",
            method="POST",
            description="User login successful",
        ))
        db.commit()
        db.refresh(user)
        
        # Create session
        user_info = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": bool(user.is_admin),
            "login_time": datetime.utcnow().isoformat()
        }
        
        # Return session ID as cookie
        response = JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": f"Đăng nhập thành công. Chào {user_info['username']}!",
                "user": {
                    "username": user_info["username"],
                    "email": user_info["email"],
                    "is_admin": user_info["is_admin"]
                }
            }
        )
        session_id = _set_session_cookie(response, user.id)
        _clear_guest_mode_cookie(response)
        sessions[session_id] = user_info
        return response
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Lỗi đăng nhập: {str(e)}"}
        )

@router.post("/signup")
async def signup(request: Request, db: Session = Depends(get_db)):
    """Handle user registration"""
    try:
        data = await request.json()
        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        
        # Validation
        if not username or not email or not password:
            return JSONResponse(
                status_code=400,
                content={"error": "Vui lòng điền đầy đủ thông tin"}
            )
        
        # Check username length
        if len(username) < 3 or len(username) > 20:
            return JSONResponse(
                status_code=400,
                content={"error": "Tên đăng nhập phải từ 3-20 ký tự"}
            )
        
        # Check password length
        if len(password) < 6:
            return JSONResponse(
                status_code=400,
                content={"error": "Mật khẩu phải có tối thiểu 6 ký tự"}
            )
        
        # Check if username already exists
        existing_username = db.query(User).filter(func.lower(User.username) == username.lower()).first()
        if existing_username:
            return JSONResponse(
                status_code=409,
                content={"error": "Tên đăng nhập đã tồn tại"}
            )
        
        # Check if email already exists
        existing_email = db.query(User).filter(func.lower(User.email) == email.lower()).first()
        if existing_email:
            return JSONResponse(
                status_code=409,
                content={"error": "Email đã được sử dụng"}
            )

        # Create new user
        new_user = User(
            username=username,
            email=email,
            password_hash=get_password_hash(password),
            is_admin=False,
            is_active=True
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "message": "Đăng ký thành công! Vui lòng đăng nhập.",
                "user": {
                    "username": username,
                    "email": email
                }
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Lỗi đăng ký: {str(e)}"}
        )

@router.post("/logout")
async def logout(request: Request, db: Session = Depends(get_db)):
    """Handle user logout"""
    try:
        user = get_authenticated_user_from_request(request, db)
        session_id = request.cookies.get("session_id")
        if session_id and session_id in sessions:
            del sessions[session_id]

        if user:
            db.add(UserActivity(
                user_id=user.id,
                activity_type="logout",
                feature="auth",
                path="/logout",
                method="POST",
                description="User logged out",
            ))
            db.commit()
        
        response = JSONResponse(
            status_code=200,
            content={"success": True, "message": "Đã đăng xuất"}
        )
        response.delete_cookie("session_id")
        _clear_guest_mode_cookie(response)
        return response
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Lỗi đăng xuất: {str(e)}"}
        )

@router.get("/session")
async def get_session(request: Request, db: Session = Depends(get_db)):
    """Get current session info"""
    try:
        user = get_authenticated_user_from_request(request, db)
        if user:
            response = JSONResponse(
                status_code=200,
                content={
                    "authenticated": True,
                    "guest": False,
                    "mode": "authenticated",
                    "user": {
                        "user_id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "is_admin": bool(user.is_admin),
                        "full_name": (user_profile_cache.get(user.id) or {}).get("full_name", ""),
                        "phone": (user_profile_cache.get(user.id) or {}).get("phone", ""),
                        "address": (user_profile_cache.get(user.id) or {}).get("address", ""),
                        "language": (user_profile_cache.get(user.id) or {}).get("language", "vi"),
                    }
                }
            )
            _set_session_cookie(response, user.id)
            return response
        else:
            guest_mode = request.cookies.get(GUEST_MODE_COOKIE) == "1"
            return JSONResponse(
                status_code=200,
                content={
                    "authenticated": False,
                    "guest": guest_mode,
                    "mode": "guest" if guest_mode else "anonymous",
                }
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.get("/check-auth")
async def check_auth(request: Request, db: Session = Depends(get_db)):
    """Check if user is authenticated"""
    user = get_authenticated_user_from_request(request, db)
    if user:
        response = JSONResponse(
            status_code=200,
            content={
                "authenticated": True,
                "guest": False,
                "mode": "authenticated",
                "user": {
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_admin": bool(user.is_admin),
                }
            }
        )
        _set_session_cookie(response, user.id)
        return response
    guest_mode = request.cookies.get(GUEST_MODE_COOKIE) == "1"
    return JSONResponse(
        status_code=200,
        content={
            "authenticated": False,
            "guest": guest_mode,
            "mode": "guest" if guest_mode else "anonymous",
        }
    )


@router.get("/activity-history")
async def get_activity_history(request: Request, limit: int = 50, db: Session = Depends(get_db)):
    """Get website usage history for current authenticated user only."""
    user = get_authenticated_user_from_request(request, db)
    if not user:
        return JSONResponse(
            status_code=401,
            content={"error": "Bạn chưa đăng nhập"}
        )

    safe_limit = max(1, min(limit, 200))
    rows = (
        db.query(UserActivity)
        .filter(UserActivity.user_id == user.id)
        .order_by(UserActivity.created_at.desc())
        .limit(safe_limit)
        .all()
    )

    activities = []
    for row in rows:
        activities.append({
            "id": row.id,
            "activity_type": row.activity_type,
            "feature": row.feature,
            "path": row.path,
            "method": row.method,
            "description": row.description,
            "created_at": row.created_at.isoformat() if row.created_at else None,
        })

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "total": len(activities),
            "activities": activities,
        }
    )

@router.put("/update-profile")
async def update_profile(request: Request, db: Session = Depends(get_db)):
    """Update user profile information"""
    try:
        user = get_authenticated_user_from_request(request, db)
        if not user:
            return JSONResponse(
                status_code=401,
                content={"error": "Bạn chưa đăng nhập"}
            )
        
        data = await request.json()

        # Persist fields available in current DB schema
        user.email = data.get("email", user.email)
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)

        # Keep extended profile settings in memory for current runtime
        user_profile_cache[user.id] = {
            "full_name": data.get("full_name", ""),
            "phone": data.get("phone", ""),
            "address": data.get("address", ""),
            "language": data.get("language", "vi"),
        }
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Cập nhật hồ sơ thành công",
                "user": {
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_admin": bool(user.is_admin),
                    "full_name": user_profile_cache[user.id]["full_name"],
                    "phone": user_profile_cache[user.id]["phone"],
                    "address": user_profile_cache[user.id]["address"],
                    "language": user_profile_cache[user.id]["language"],
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Lỗi cập nhật hồ sơ: {str(e)}"}
        )

@router.post("/change-password")
async def change_password(request: Request, db: Session = Depends(get_db)):
    """Change user password"""
    try:
        user = get_authenticated_user_from_request(request, db)
        if not user:
            return JSONResponse(
                status_code=401,
                content={"error": "Bạn chưa đăng nhập"}
            )
        
        data = await request.json()
        current_password = data.get("current_password", "").strip()
        new_password = data.get("new_password", "").strip()
        
        if not current_password or not new_password:
            return JSONResponse(
                status_code=400,
                content={"error": "Vui lòng điền đầy đủ thông tin"}
            )
        
        if len(new_password) < 6:
            return JSONResponse(
                status_code=400,
                content={"error": "Mật khẩu mới phải có ít nhất 6 ký tự"}
            )
        
        # Verify current password
        password_ok = verify_password(current_password, user.password_hash) or (user.password_hash == current_password)
        if not password_ok:
            return JSONResponse(
                status_code=401,
                content={"error": "Mật khẩu hiện tại không chính xác"}
            )

        # Update password
        user.password_hash = get_password_hash(new_password)
        db.commit()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Thay đổi mật khẩu thành công"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Lỗi thay đổi mật khẩu: {str(e)}"}
        )
