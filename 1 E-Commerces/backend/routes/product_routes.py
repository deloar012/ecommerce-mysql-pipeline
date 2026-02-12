from flask import Blueprint, request, jsonify
from backend.models.db import get_db_cursor
from backend.utils.validators import validate_price, validate_quantity
from backend.utils.security import token_required
from backend.config import ITEMS_PER_PAGE

products = Blueprint('products', __name__)

@products.route('', methods=['GET'])
def get_products():
    """Get all products with filtering and pagination"""
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', ITEMS_PER_PAGE)), 100)
        category = request.args.get('category', '')
        search = request.args.get('search', '')
        sort_by = request.args.get('sort', 'created_at')
        order = request.args.get('order', 'DESC')
        
        # Build query
        query = "SELECT * FROM products WHERE is_active = TRUE"
        params = []
        
        if category:
            query += " AND category = %s"
            params.append(category)
        
        if search:
            query += " AND (name LIKE %s OR description LIKE %s)"
            search_term = f"%{search}%"
            params.extend([search_term, search_term])
        
        # Add sorting
        allowed_sorts = ['name', 'price', 'created_at']
        if sort_by in allowed_sorts:
            query += f" ORDER BY {sort_by} {order}"
        
        # Add pagination
        offset = (page - 1) * per_page
        query += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])
        
        with get_db_cursor() as cursor:
            # Get products
            cursor.execute(query, tuple(params))
            products_list = cursor.fetchall()
            
            # Get total count
            count_query = "SELECT COUNT(*) as total FROM products WHERE is_active = TRUE"
            count_params = []
            
            if category:
                count_query += " AND category = %s"
                count_params.append(category)
            
            if search:
                count_query += " AND (name LIKE %s OR description LIKE %s)"
                search_term = f"%{search}%"
                count_params.extend([search_term, search_term])
            
            cursor.execute(count_query, tuple(count_params))
            total = cursor.fetchone()['total']
            
            return jsonify({
                'success': True,
                'products': products_list,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            })
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@products.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product by ID"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM products
                WHERE id = %s AND is_active = TRUE
            """, (product_id,))
            
            product = cursor.fetchone()
            
            if not product:
                return jsonify({
                    'success': False,
                    'message': 'Product not found'
                }), 404
            
            return jsonify({
                'success': True,
                'product': product
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@products.route('/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT category, COUNT(*) as count
                FROM products
                WHERE is_active = TRUE
                GROUP BY category
                ORDER BY category
            """)
            
            categories = cursor.fetchall()
            
            return jsonify({
                'success': True,
                'categories': categories
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@products.route('/featured', methods=['GET'])
def get_featured_products():
    """Get featured products"""
    try:
        limit = int(request.args.get('limit', 8))
        
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM products
                WHERE is_active = TRUE
                ORDER BY created_at DESC
                LIMIT %s
            """, (limit,))
            
            featured = cursor.fetchall()
            
            return jsonify({
                'success': True,
                'products': featured
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@products.route('', methods=['POST'])
@token_required
def create_product():
    """Create new product (Admin only)"""
    try:
        data = request.get_json()
        
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        category = data.get('category', '').strip()
        price = data.get('price')
        stock = data.get('stock', 0)
        image_url = data.get('image_url', '').strip()
        
        # Validate
        if not name or not category:
            return jsonify({
                'success': False,
                'message': 'Name and category are required'
            }), 400
        
        is_valid, error = validate_price(price)
        if not is_valid:
            return jsonify({'success': False, 'message': error}), 400
        
        with get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO products (name, description, category, price, stock, image_url)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, description, category, price, stock, image_url))
            
            product_id = cursor.lastrowid
            
            return jsonify({
                'success': True,
                'message': 'Product created successfully',
                'product_id': product_id
            }), 201
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@products.route('/<int:product_id>', methods=['PUT'])
@token_required
def update_product(product_id):
    """Update product (Admin only)"""
    try:
        data = request.get_json()
        
        with get_db_cursor() as cursor:
            # Check if product exists
            cursor.execute("SELECT id FROM products WHERE id = %s", (product_id,))
            if not cursor.fetchone():
                return jsonify({
                    'success': False,
                    'message': 'Product not found'
                }), 404
            
            # Build update query
            update_fields = []
            params = []
            
            if 'name' in data:
                update_fields.append("name = %s")
                params.append(data['name'])
            
            if 'description' in data:
                update_fields.append("description = %s")
                params.append(data['description'])
            
            if 'category' in data:
                update_fields.append("category = %s")
                params.append(data['category'])
            
            if 'price' in data:
                is_valid, error = validate_price(data['price'])
                if not is_valid:
                    return jsonify({'success': False, 'message': error}), 400
                update_fields.append("price = %s")
                params.append(data['price'])
            
            if 'stock' in data:
                update_fields.append("stock = %s")
                params.append(data['stock'])
            
            if 'image_url' in data:
                update_fields.append("image_url = %s")
                params.append(data['image_url'])
            
            if not update_fields:
                return jsonify({
                    'success': False,
                    'message': 'No fields to update'
                }), 400
            
            params.append(product_id)
            query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = %s"
            
            cursor.execute(query, tuple(params))
            
            return jsonify({
                'success': True,
                'message': 'Product updated successfully'
            })
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@products.route('/<int:product_id>', methods=['DELETE'])
@token_required
def delete_product(product_id):
    """Soft delete product (Admin only)"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                UPDATE products SET is_active = FALSE
                WHERE id = %s
            """, (product_id,))
            
            if cursor.rowcount == 0:
                return jsonify({
                    'success': False,
                    'message': 'Product not found'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Product deleted successfully'
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500