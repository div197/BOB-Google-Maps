"""bob_api.auth

Authentication and authorization for BOB Google Maps API v0.6.0
Simple API key-based authentication with divine security.

Made with 🙏 following Niṣkāma Karma Yoga principles
"""

import os
from typing import Optional
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader

from .config import get_settings

settings = get_settings()

# Security schemes
security = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(
    api_key: Optional[str] = Security(api_key_header),
    token: Optional[HTTPAuthorizationCredentials] = Security(security)
) -> Optional[str]:
    """
    Verify API key from header or bearer token.
    
    Supports both:
    - X-API-Key header
    - Authorization: Bearer <api-key>
    
    Returns the API key if valid, None if no authentication required.
    """
    # If no API key is configured, allow all requests
    if not settings.API_KEY:
        return None
    
    # Check X-API-Key header
    if api_key and api_key == settings.API_KEY:
        return api_key
    
    # Check Authorization header
    if token and token.credentials == settings.API_KEY:
        return token.credentials
    
    # If API key is required but not provided or invalid
    if settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return None


async def get_current_user(api_key: str = Security(verify_api_key)) -> dict:
    """
    Get current user information based on API key.
    
    For now, returns a simple user object.
    In the future, this could integrate with a user database.
    """
    if not api_key:
        return {"user_id": "anonymous", "permissions": ["read"]}
    
    # TODO: Implement proper user management
    # For now, all valid API keys get admin permissions
    return {
        "user_id": "api_user",
        "permissions": ["read", "write", "admin"],
        "api_key": api_key[:8] + "..." if api_key else None
    }


def require_admin(current_user: dict = Security(get_current_user)) -> dict:
    """
    Require admin permissions for endpoint access.
    """
    if "admin" not in current_user.get("permissions", []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permissions required"
        )
    return current_user


def create_api_key() -> str:
    """
    Generate a new API key.
    
    This is a simple implementation for demonstration.
    In production, use a more sophisticated key generation system.
    """
    import secrets
    import string
    
    alphabet = string.ascii_letters + string.digits
    return "bob_" + "".join(secrets.choice(alphabet) for _ in range(32)) 