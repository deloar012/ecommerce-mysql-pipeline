"""
Security utilities for authentication and authorization
"""

import jwt
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from backend.config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES
from backend.models.db import get_db_cursor


def generate_token(user_id, expires_delta=None):
    """Generate JWT token for user"""
    if expires_delta is None:
        expires_delta = JWT_ACCESS_TOKEN_EXPIRES
    
    expire = datetime.utcnow() + expires_delta
    
    payload = {
        'user_id': user_id,
        'exp': expire,
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return token


def decode_token(token):
    """Decode JWT token and return user_id"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({
                    'success': False,
                    'message': 'Invalid token format'
                }), 401
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token is missing'
            }), 401
        
        # Decode token
        user_id = decode_token(token)
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired token'
            }), 401
        
        # Verify user exists and is active
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    SELECT id, full_name, email, is_active
                    FROM users
                    WHERE id = %s
                """, (user_id,))
                
                user = cursor.fetchone()
                
                if not user:
                    return jsonify({
                        'success': False,
                        'message': 'User not found'
                    }), 401
                
                if not user['is_active']:
                    return jsonify({
                        'success': False,
                        'message': 'Account is deactivated'
                    }), 401
                
                # Add user to request context
                request.current_user = user
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Authentication failed'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def generate_verification_code(length=6):
    """Generate random numeric verification code"""
    return ''.join(secrets.choice('0123456789') for _ in range(length))


def generate_reset_token():
    """Generate secure password reset token"""
    return secrets.token_urlsafe(32)


def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    @token_required
    def decorated_function(*args, **kwargs):
        user = request.current_user
        
        # Check if user is admin (you can add an is_admin field to users table)
        # For now, check if email is admin email
        if user['email'] != 'admin@shophub.com':
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def sanitize_input(text):
    """Basic input sanitization"""
    if not text:
        return text
    
    # Remove potential XSS attempts
    dangerous_chars = ['<', '>', '"', "'", '&', '`']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()


def validate_ip(ip_address):
    """Validate IP address format"""
    import re
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(pattern, ip_address):
        parts = ip_address.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    return False


def rate_limit_check(user_id, action, max_attempts=5, window_minutes=15):
    """
    Check if user has exceeded rate limit for an action
    Returns (allowed: bool, remaining_attempts: int)
    """
    # This is a simple in-memory rate limiter
    # In production, use Redis or database-based solution
    
    # For now, just return allowed
    return True, max_attempts


def generate_order_number():
    """Generate unique order number"""
    import random
    import string
    from datetime import datetime
    
    # Format: ORD-YYYYMMDD-XXXXXX
    date_part = datetime.now().strftime('%Y%m%d')
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    return f"ORD-{date_part}-{random_part}"