# backend/routes/auth_routes.py
from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.utils.email_service import (
    send_verification_email, 
    send_password_reset_email,
    generate_verification_code,
    store_verification_code,
    verify_code
)
from backend.models.user_model import (
    create_user, 
    get_user_by_email, 
    check_email_exists,
    update_user_password
)
from backend.utils.password_hash import hash_password, verify_password
from backend.utils.security import generate_token
import secrets

auth = Blueprint('auth', __name__)

# Store password reset tokens (in production, use Redis or database)
password_reset_tokens = {}

@auth.route('/send-verification', methods=['POST'])
def send_verification():
    """Send verification code to email"""
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({
                'success': False,
                'message': 'Email is required'
            }), 400

        # Generate verification code
        code = generate_verification_code()
        
        # Store the code
        store_verification_code(email, code)
        
        # Send email
        email_sent = send_verification_email(email, code)
        
        if email_sent:
            return jsonify({
                'success': True,
                'message': 'Verification code sent to your email',
                'code': code  # Remove this in production!
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send email. Please check email configuration.'
            }), 500

    except Exception as e:
        print(f"Error in send_verification: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500

@auth.route('/verify-code', methods=['POST'])
def verify_verification_code():
    """Verify the email verification code"""
    try:
        data = request.get_json()
        email = data.get('email')
        code = data.get('code')

        if not email or not code:
            return jsonify({
                'success': False,
                'message': 'Email and code are required'
            }), 400

        # Verify the code
        is_valid = verify_code(email, code)
        
        if is_valid:
            return jsonify({
                'success': True,
                'message': 'Code verified successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired verification code'
            }), 400

    except Exception as e:
        print(f"Error in verify_code: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

@auth.route('/check-email', methods=['POST'])
def check_email():
    """Check if email already exists"""
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({
                'success': False,
                'message': 'Email is required'
            }), 400

        exists = check_email_exists(email)
        
        return jsonify({
            'success': True,
            'exists': exists
        }), 200

    except Exception as e:
        print(f"Error in check_email: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

@auth.route('/register', methods=['POST'])
def register():
    """Register a new user (after email verification)"""
    try:
        data = request.get_json()
        
        # Extract data
        full_name = data.get('full_name')
        email = data.get('email')
        mobile = data.get('mobile')
        password = data.get('password')

        # Validation
        if not all([full_name, email, mobile, password]):
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            }), 400

        # Check if email already exists
        if check_email_exists(email):
            return jsonify({
                'success': False,
                'message': 'Email already registered'
            }), 400

        # Hash password
        hashed_password = hash_password(password)

        # Create user
        user_id = create_user(full_name, email, mobile, hashed_password)

        if user_id:
            return jsonify({
                'success': True,
                'message': 'Registration successful',
                'user_id': user_id
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to create user'
            }), 500

    except Exception as e:
        print(f"Error in register: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500

@auth.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400

        # Get user
        user = get_user_by_email(email)

        if not user:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401

        # Verify password
        if not verify_password(password, user['password_hash']):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401

        # Generate token
        token = generate_token(user['user_id'])

        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': {
                'user_id': user['user_id'],
                'full_name': user['full_name'],
                'email': user['email'],
                'mobile': user['mobile']
            }
        }), 200

    except Exception as e:
        print(f"Error in login: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

@auth.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Send password reset email"""
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({
                'success': False,
                'message': 'Email is required'
            }), 400

        # Check if user exists
        user = get_user_by_email(email)
        
        if not user:
            # For security, don't reveal if email exists or not
            return jsonify({
                'success': True,
                'message': 'If this email is registered, you will receive a password reset link'
            }), 200

        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        
        # Store token (in production, store in database with expiry)
        from datetime import datetime, timedelta
        password_reset_tokens[reset_token] = {
            'email': email,
            'expiry': datetime.now() + timedelta(hours=1)
        }

        # Send reset email
        email_sent = send_password_reset_email(email, reset_token)

        if email_sent:
            return jsonify({
                'success': True,
                'message': 'Password reset link sent to your email',
                'token': reset_token  # Remove this in production!
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send email'
            }), 500

    except Exception as e:
        print(f"Error in forgot_password: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

@auth.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password with token"""
    try:
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('password')

        if not token or not new_password:
            return jsonify({
                'success': False,
                'message': 'Token and new password are required'
            }), 400

        # Verify token
        if token not in password_reset_tokens:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired reset token'
            }), 400

        token_data = password_reset_tokens[token]
        
        # Check if expired
        from datetime import datetime
        if datetime.now() > token_data['expiry']:
            del password_reset_tokens[token]
            return jsonify({
                'success': False,
                'message': 'Reset token has expired'
            }), 400

        # Hash new password
        hashed_password = hash_password(new_password)

        # Update password
        success = update_user_password(token_data['email'], hashed_password)

        if success:
            # Remove used token
            del password_reset_tokens[token]
            
            return jsonify({
                'success': True,
                'message': 'Password reset successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to reset password'
            }), 500

    except Exception as e:
        print(f"Error in reset_password: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

@auth.route('/verify-token', methods=['POST'])
def verify_token():
    """Verify if auth token is valid"""
    try:
        data = request.get_json()
        token = data.get('token')

        if not token:
            return jsonify({
                'success': False,
                'message': 'Token is required'
            }), 400

        # Verify token (implement your token verification logic)
        # This is a placeholder - implement actual JWT verification
        
        return jsonify({
            'success': True,
            'message': 'Token is valid'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Invalid token'
        }), 401
