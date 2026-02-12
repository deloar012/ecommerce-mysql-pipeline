from flask import Blueprint, request, jsonify
from backend.models.db import get_db_cursor
from backend.utils.security import token_required, generate_order_number
import json

orders = Blueprint('orders', __name__)

@orders.route('', methods=['GET'])
@token_required
def get_orders():
    """Get user's orders"""
    try:
        status = request.args.get('status')
        
        with get_db_cursor() as cursor:
            query = """
                SELECT o.*, 
                       JSON_ARRAYAGG(
                           JSON_OBJECT(
                               'product_name', oi.product_name,
                               'quantity', oi.quantity,
                               'price', oi.price
                           )
                       ) as items
                FROM orders o
                LEFT JOIN order_items oi ON o.id = oi.order_id
                WHERE o.user_id = %s
            """
            params = [request.user_id]
            
            if status:
                query += " AND o.status = %s"
                params.append(status)
            
            query += " GROUP BY o.id ORDER BY o.created_at DESC"
            
            cursor.execute(query, tuple(params))
            orders_list = cursor.fetchall()
            
            # Parse JSON items
            for order in orders_list:
                if order['items']:
                    order['items'] = json.loads(order['items'])
            
            return jsonify({
                'success': True,
                'orders': orders_list
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@orders.route('/<int:order_id>', methods=['GET'])
@token_required
def get_order(order_id):
    """Get single order details"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM orders
                WHERE id = %s AND user_id = %s
            """, (order_id, request.user_id))
            
            order = cursor.fetchone()
            
            if not order:
                return jsonify({
                    'success': False,
                    'message': 'Order not found'
                }), 404
            
            cursor.execute("""
                SELECT * FROM order_items
                WHERE order_id = %s
            """, (order_id,))
            
            order['items'] = cursor.fetchall()
            
            return jsonify({
                'success': True,
                'order': order
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@orders.route('', methods=['POST'])
@token_required
def create_order():
    """Create new order"""
    try:
        data = request.get_json()
        
        items = data.get('items', [])
        shipping_address = data.get('shipping_address', {})
        payment_method = data.get('payment_method')
        subtotal = data.get('subtotal')
        shipping = data.get('shipping')
        tax = data.get('tax')
        discount = data.get('discount', 0)
        total = data.get('total')
        
        if not items or not payment_method:
            return jsonify({
                'success': False,
                'message': 'Items and payment method are required'
            }), 400
        
        with get_db_cursor() as cursor:
            # Generate order number
            order_number = generate_order_number()
            
            # Create order
            cursor.execute("""
                INSERT INTO orders (
                    user_id, order_number, status, subtotal, tax, 
                    shipping, discount, total, payment_method, 
                    shipping_address
                )
                VALUES (%s, %s, 'pending', %s, %s, %s, %s, %s, %s, %s)
            """, (
                request.user_id, order_number, subtotal, tax,
                shipping, discount, total, payment_method,
                json.dumps(shipping_address)
            ))
            
            order_id = cursor.lastrowid
            
            # Add order items
            for item in items:
                cursor.execute("""
                    INSERT INTO order_items (
                        order_id, product_id, product_name, quantity, price
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    order_id, item['id'], item['name'],
                    item['quantity'], item['price']
                ))
                
                # Update product stock
                cursor.execute("""
                    UPDATE products SET stock = stock - %s
                    WHERE id = %s
                """, (item['quantity'], item['id']))
            
            # Clear cart
            cursor.execute("DELETE FROM cart WHERE user_id = %s", (request.user_id,))
            
            return jsonify({
                'success': True,
                'message': 'Order placed successfully',
                'order_id': order_id,
                'order_number': order_number
            }), 201
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@orders.route('/<int:order_id>/cancel', methods=['PUT'])
@token_required
def cancel_order(order_id):
    """Cancel order"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT status FROM orders
                WHERE id = %s AND user_id = %s
            """, (order_id, request.user_id))
            
            order = cursor.fetchone()
            
            if not order:
                return jsonify({
                    'success': False,
                    'message': 'Order not found'
                }), 404
            
            if order['status'] not in ['pending', 'processing']:
                return jsonify({
                    'success': False,
                    'message': 'Order cannot be cancelled'
                }), 400
            
            cursor.execute("""
                UPDATE orders SET status = 'cancelled'
                WHERE id = %s
            """, (order_id,))
            
            return jsonify({
                'success': True,
                'message': 'Order cancelled successfully'
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ============================================================================
# backend/routes/payment_routes.py
# ============================================================================

from flask import Blueprint, request, jsonify
from backend.utils.security import token_required

payments = Blueprint('payments', __name__)

@payments.route('/process', methods=['POST'])
@token_required
def process_payment():
    """Process payment (placeholder for payment gateway integration)"""
    try:
        data = request.get_json()
        
        order_id = data.get('order_id')
        payment_method = data.get('payment_method')
        amount = data.get('amount')
        
        # Here you would integrate with actual payment gateway
        # For now, we'll just simulate success
        
        return jsonify({
            'success': True,
            'message': 'Payment processed successfully',
            'transaction_id': f'TXN{order_id}123456'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@payments.route('/verify', methods=['POST'])
@token_required
def verify_payment():
    """Verify payment status"""
    try:
        data = request.get_json()
        transaction_id = data.get('transaction_id')
        
        # Verify with payment gateway
        
        return jsonify({
            'success': True,
            'status': 'verified',
            'transaction_id': transaction_id
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

