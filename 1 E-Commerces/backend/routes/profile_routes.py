
# ============================================================================
# backend/routes/profile_routes.py
# ============================================================================

from flask import Blueprint, request, jsonify
from backend.models.db import get_db_cursor
from backend.utils.security import token_required
from backend.utils.validators import validate_email, validate_mobile
from backend.utils.password_hash import hash_password, verify_password

profile = Blueprint('profile', __name__)

@profile.route('', methods=['GET'])
@token_required
def get_profile():
    """Get user profile"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT id, full_name, email, mobile, created_at, last_login
                FROM users WHERE id = %s
            """, (request.user_id,))
            
            user = cursor.fetchone()
            
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'User not found'
                }), 404
            
            return jsonify({
                'success': True,
                'profile': user
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@profile.route('', methods=['PUT'])
@token_required
def update_profile():
    """Update user profile"""
    try:
        data = request.get_json()
        
        with get_db_cursor() as cursor:
            update_fields = []
            params = []
            
            if 'full_name' in data:
                update_fields.append("full_name = %s")
                params.append(data['full_name'])
            
            if 'email' in data:
                is_valid, error = validate_email(data['email'])
                if not is_valid:
                    return jsonify({'success': False, 'message': error}), 400
                update_fields.append("email = %s")
                params.append(data['email'])
            
            if 'mobile' in data:
                is_valid, error = validate_mobile(data['mobile'])
                if not is_valid:
                    return jsonify({'success': False, 'message': error}), 400
                update_fields.append("mobile = %s")
                params.append(data['mobile'])
            
            if not update_fields:
                return jsonify({
                    'success': False,
                    'message': 'No fields to update'
                }), 400
            
            params.append(request.user_id)
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
            
            cursor.execute(query, tuple(params))
            
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully'
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@profile.route('/change-password', methods=['PUT'])
@token_required
def change_password():
    """Change user password"""
    try:
        data = request.get_json()
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({
                'success': False,
                'message': 'Current and new passwords are required'
            }), 400
        
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT password_hash FROM users WHERE id = %s
            """, (request.user_id,))
            
            user = cursor.fetchone()
            
            if not verify_password(current_password, user['password_hash']):
                return jsonify({
                    'success': False,
                    'message': 'Current password is incorrect'
                }), 400
            
            new_hash = hash_password(new_password)
            
            cursor.execute("""
                UPDATE users SET password_hash = %s WHERE id = %s
            """, (new_hash, request.user_id))
            
            return jsonify({
                'success': True,
                'message': 'Password changed successfully'
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@profile.route('/addresses', methods=['GET'])
@token_required
def get_addresses():
    """Get user addresses"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM addresses
                WHERE user_id = %s
                ORDER BY is_default DESC, created_at DESC
            """, (request.user_id,))
            
            addresses = cursor.fetchall()
            
            return jsonify({
                'success': True,
                'addresses': addresses
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@profile.route('/addresses', methods=['POST'])
@token_required
def add_address():
    """Add new address"""
    try:
        data = request.get_json()
        
        with get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO addresses (
                    user_id, address_type, full_name, phone,
                    address_line1, address_line2, city, state,
                    zip_code, country, is_default
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                request.user_id, data.get('address_type', 'shipping'),
                data['full_name'], data['phone'], data['address_line1'],
                data.get('address_line2', ''), data['city'], data['state'],
                data['zip_code'], data['country'], data.get('is_default', False)
            ))
            
            return jsonify({
                'success': True,
                'message': 'Address added successfully',
                'address_id': cursor.lastrowid
            }), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500