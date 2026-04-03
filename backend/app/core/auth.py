"""
Authentication utilities for the application
"""
from fastapi import HTTPException, status, Depends, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.core.logger import logger
from app.api.routes.auth import verify_session_token


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """
    Get current authenticated user from the session
    
    Get user based on session_id cookie.
    """
    try:
        session_id = request.cookies.get("session_id")
        user_id = verify_session_token(session_id)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )

        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

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
