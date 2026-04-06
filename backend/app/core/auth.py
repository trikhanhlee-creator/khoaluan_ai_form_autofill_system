"""
Authentication utilities for the application
"""
from fastapi import HTTPException, status, Depends, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.core.logger import logger
from app.core.security import get_password_hash
from app.api.routes.auth import verify_session_token


GUEST_EMAIL = "guest@autofill.local"
GUEST_USERNAME = "guest"
GUEST_PASSWORD_PLACEHOLDER = "guest-account-not-for-login"


def _get_or_create_guest_user(db: Session) -> User:
    """Return a shared guest user so anonymous visitors can use all non-admin features."""
    guest_user = db.query(User).filter(User.email == GUEST_EMAIL).first()
    if guest_user:
        if not guest_user.is_active:
            guest_user.is_active = True
            db.commit()
            db.refresh(guest_user)
        return guest_user

    guest_user = User(
        email=GUEST_EMAIL,
        username=GUEST_USERNAME,
        password_hash=get_password_hash(GUEST_PASSWORD_PLACEHOLDER),
        is_admin=False,
        is_active=True,
    )
    db.add(guest_user)
    db.commit()
    db.refresh(guest_user)
    return guest_user


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """
    Get current authenticated user from the session
    
    Get user based on session_id cookie.
    """
    try:
        session_id = request.cookies.get("session_id")
        user_id = verify_session_token(session_id)
        if not user_id:
            return _get_or_create_guest_user(db)

        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return _get_or_create_guest_user(db)

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def verify_admin(user: User) -> None:
    """
    Verify that user is an admin
    Raises HTTPException if not admin
    """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )


def verify_active(user: User) -> None:
    """
    Verify that user is active
    Raises HTTPException if not active
    """
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
