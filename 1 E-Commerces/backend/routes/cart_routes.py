# backend/routes/cart_routes.py
from flask import Blueprint, request, jsonify
from backend.models.db import get_db_cursor
from backend.utils.security import token_required
from backend.utils.validators import validate_quantity

cart = Blueprint('cart', __name__)

@cart.route('', methods=['GET'])
@token_required
def get_cart():
    """Get user's cart"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT c.id, c.quantity, p.id as product_id, p.name, p.price, 
                       p.stock, p.image_url, p.category
                FROM cart c
                JOIN products p ON c.product_id = p.id
                WHERE c.user_id = %s AND p.is_active = TRUE
            """, (request.user_id,))
            
            cart_items = cursor.fetchall()
            
            total = sum(item['price'] * item['quantity'] for item in cart_items)
            
            return jsonify({
                'success': True,
                'cart': cart_items,
                'total': float(total)
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@cart.route('/add', methods=['POST'])
@token_required
def add_to_cart():
    """Add item to cart"""
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        is_valid, error = validate_quantity(quantity)
        if not is_valid:
            return jsonify({'success': False, 'message': error}), 400
        
        with get_db_cursor() as cursor:
            # Check product exists and has stock
            cursor.execute("""
                SELECT stock FROM products 
                WHERE id = %s AND is_active = TRUE
            """, (product_id,))
            
            product = cursor.fetchone()
            if not product:
                return jsonify({
                    'success': False,
                    'message': 'Product not found'
                }), 404
            
            if product['stock'] < quantity:
                return jsonify({
                    'success': False,
                    'message': 'Insufficient stock'
                }), 400
            
            # Check if already in cart
            cursor.execute("""
                SELECT id, quantity FROM cart
                WHERE user_id = %s AND product_id = %s
            """, (request.user_id, product_id))
            
            existing = cursor.fetchone()
            
            if existing:
                new_quantity = existing['quantity'] + quantity
                if new_quantity > product['stock']:
                    return jsonify({
                        'success': False,
                        'message': 'Insufficient stock'
                    }), 400
                
                cursor.execute("""
                    UPDATE cart SET quantity = %s
                    WHERE id = %s
                """, (new_quantity, existing['id']))
            else:
                cursor.execute("""
                    INSERT INTO cart (user_id, product_id, quantity)
                    VALUES (%s, %s, %s)
                """, (request.user_id, product_id, quantity))
            
            return jsonify({
                'success': True,
                'message': 'Item added to cart'
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@cart.route('/update/<int:cart_id>', methods=['PUT'])
@token_required
def update_cart_item(cart_id):
    """Update cart item quantity"""
    try:
        data = request.get_json()
        quantity = data.get('quantity')
        
        is_valid, error = validate_quantity(quantity)
        if not is_valid:
            return jsonify({'success': False, 'message': error}), 400
        
        with get_db_cursor() as cursor:
            cursor.execute("""
                UPDATE cart SET quantity = %s
                WHERE id = %s AND user_id = %s
            """, (quantity, cart_id, request.user_id))
            
            if cursor.rowcount == 0:
                return jsonify({
                    'success': False,
                    'message': 'Cart item not found'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Cart updated'
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@cart.route('/remove/<int:cart_id>', methods=['DELETE'])
@token_required
def remove_from_cart(cart_id):
    """Remove item from cart"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                DELETE FROM cart
                WHERE id = %s AND user_id = %s
            """, (cart_id, request.user_id))
            
            if cursor.rowcount == 0:
                return jsonify({
                    'success': False,
                    'message': 'Cart item not found'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Item removed from cart'
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@cart.route('/clear', methods=['DELETE'])
@token_required
def clear_cart():
    """Clear entire cart"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("DELETE FROM cart WHERE user_id = %s", (request.user_id,))
            
            return jsonify({
                'success': True,
                'message': 'Cart cleared'
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500