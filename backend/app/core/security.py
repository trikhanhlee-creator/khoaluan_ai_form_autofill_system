"""
Security utilities for password hashing and verification
"""
from passlib.context import CryptContext
from typing import Optional

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt
    """
    if not password:
        raise ValueError("Password cannot be empty")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hash
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def verify_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Verify password strength
    Returns: (is_valid, error_message)
    
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    if len(password) < 8:
        return False, "Mật khẩu phải có ít nhất 8 ký tự"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    if not has_upper:
        return False, "Mật khẩu phải có ít nhất một chữ in hoa"
    
    if not has_lower:
        return False, "Mật khẩu phải có ít nhất một chữ thường"
    
    if not has_digit:
        return False, "Mật khẩu phải có ít nhất một số"
    
    if not has_special:
        return False, "Mật khẩu phải có ít nhất một ký tự đặc biệt (!@#$%^&*...)"
    
    return True, None
