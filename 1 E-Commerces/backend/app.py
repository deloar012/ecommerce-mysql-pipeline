from flask import Flask, jsonify, send_from_directory, render_template, request, redirect, session, url_for
from flask_cors import CORS
import os
from backend.config import SECRET_KEY, CORS_ORIGINS
from backend.routes.auth_routes import auth
from backend.routes.product_routes import products
from backend.routes.cart_routes import cart
from backend.routes.order_routes import orders
from backend.routes.payment_routes import payments
from backend.routes.profile_routes import profile
from mysql.connector import pooling
import bcrypt

# Get correct paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
FRONTEND_FOLDER = os.path.join(os.path.dirname(BASE_DIR), 'frontend')

# Initialize Flask App with correct template folder
app = Flask(__name__, 
            template_folder=TEMPLATE_DIR,
            static_folder=FRONTEND_FOLDER)
app.secret_key = SECRET_KEY

print(f"📁 Template folder: {TEMPLATE_DIR}")
print(f"📁 Frontend folder: {FRONTEND_FOLDER}")

# ------------------ MySQL Connection Pool ------------------
try:
    db_pool = pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,
        host="localhost",
        user="root",
        password="deloar@8172",
        database="ecommerce_db"
    )
    print("✅ Database connection pool created successfully")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    db_pool = None

# Enable CORS - Allow all origins for development
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Register API Blueprints
app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(products, url_prefix="/api/products")
app.register_blueprint(cart, url_prefix="/api/cart")
app.register_blueprint(orders, url_prefix="/api/orders")
app.register_blueprint(payments, url_prefix="/api/payments")
app.register_blueprint(profile, url_prefix="/api/profile")

# ------------------ ADMIN ROUTES ------------------

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        password_input = request.form.get('password', '')
        # Check admin password
        if password_input == 'deloar@8172':
            session['admin'] = True
            return redirect('/admin/dashboard')
        else:
            return render_template('admin_login.html', error="Invalid password")
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    """Admin dashboard for managing products"""
    if 'admin' not in session:
        return redirect('/admin/login')
    
    if request.method == 'POST':
        try:
            data = request.form
            if db_pool is None:
                return "Database connection not available", 500
            
            conn = db_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO products (name, price, description, category, stock, image_url)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                data.get('name'),
                data.get('price'),
                data.get('description'),
                data.get('category'),
                data.get('stock'),
                data.get('image_url')
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/admin/dashboard?success=Product added successfully')
        except Exception as e:
            return f"Error adding product: {e}", 500

    return render_template('admin_dashboard.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin', None)
    return redirect('/admin/login')

# ------------------ FRONTEND ROUTES ------------------

@app.route('/')
def serve_index():
    """Serve main index page"""
    try:
        return send_from_directory(FRONTEND_FOLDER, 'index.html')
    except Exception as e:
        return jsonify({
            'success': True,
            'message': 'ShopHub E-Commerce API v1.0',
            'error': 'Frontend files not found. API is working!',
            'endpoints': {
                'auth': '/api/auth',
                'products': '/api/products',
                'cart': '/api/cart',
                'orders': '/api/orders',
                'payments': '/api/payments',
                'profile': '/api/profile',
                'admin': '/admin/login'
            }
        })

@app.route('/products')
def products_page():
    """Serve product list page"""
    try:
        return send_from_directory(FRONTEND_FOLDER, 'product_list.html')
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'message': 'Product list page not found'
        }), 404

@app.route('/product/<int:product_id>')
def product_detail_page(product_id):
    """Serve product details page"""
    try:
        return send_from_directory(FRONTEND_FOLDER, 'product_details.html')
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'message': 'Product details page not found'
        }), 404

@app.route('/cart')
def cart_page():
    """Serve cart page"""
    try:
        return send_from_directory(FRONTEND_FOLDER, 'cart.html')
    except FileNotFoundError:
        return jsonify({'success': False, 'message': 'Cart page not found'}), 404

@app.route('/checkout')
def checkout_page():
    """Serve checkout page"""
    try:
        return send_from_directory(FRONTEND_FOLDER, 'checkout.html')
    except FileNotFoundError:
        return jsonify({'success': False, 'message': 'Checkout page not found'}), 404

@app.route('/login')
def login_page():
    """Serve login page"""
    try:
        return send_from_directory(FRONTEND_FOLDER, 'login.html')
    except FileNotFoundError:
        return jsonify({'success': False, 'message': 'Login page not found'}), 404

@app.route('/register')
def register_page():
    """Serve register page"""
    try:
        return send_from_directory(FRONTEND_FOLDER, 'register.html')
    except FileNotFoundError:
        return jsonify({'success': False, 'message': 'Register page not found'}), 404

@app.route('/profile')
def profile_page():
    """Serve profile page"""
    try:
        return send_from_directory(FRONTEND_FOLDER, 'profile.html')
    except FileNotFoundError:
        return jsonify({'success': False, 'message': 'Profile page not found'}), 404

@app.route('/orders')
def orders_page():
    """Serve orders page"""
    try:
        return send_from_directory(FRONTEND_FOLDER, 'orders.html')
    except FileNotFoundError:
        return jsonify({'success': False, 'message': 'Orders page not found'}), 404

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve other static files (CSS, JS, images, etc.)"""
    try:
        return send_from_directory(FRONTEND_FOLDER, filename)
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'message': f'File {filename} not found'
        }), 404

# ------------------ API ROUTES ------------------

@app.route("/api")
def api_home():
    """API root endpoint"""
    return jsonify({
        'success': True,
        'message': 'ShopHub E-Commerce API v1.0',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'products': '/api/products',
            'cart': '/api/cart',
            'orders': '/api/orders',
            'payments': '/api/payments',
            'profile': '/api/profile'
        }
    })

@app.route("/health")
def health_check():
    """Health check endpoint"""
    db_status = "connected" if db_pool is not None else "disconnected"
    return jsonify({
        'success': True,
        'status': 'healthy',
        'message': 'API is running',
        'database': db_status
    })

# ------------------ ERROR HANDLERS ------------------

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'message': 'Resource not found',
        'error': str(error)
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'message': 'Internal server error',
        'error': str(error)
    }), 500

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({
        'success': False,
        'message': 'Bad request',
        'error': str(error)
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    """Handle 401 errors"""
    return jsonify({
        'success': False,
        'message': 'Unauthorized access'
    }), 401

@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors"""
    return jsonify({
        'success': False,
        'message': 'Access forbidden'
    }), 403

# ------------------ CORS PREFLIGHT HANDLER ------------------

@app.before_request
def handle_preflight():
    """Handle CORS preflight requests"""
    if request.method == "OPTIONS":
        response = jsonify({'success': True})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        return response

# ------------------ RUN APPLICATION ------------------

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 ShopHub E-Commerce Server Starting...")
    print("=" * 60)
    print(f"📁 Template folder: {TEMPLATE_DIR}")
    print(f"📁 Frontend folder: {FRONTEND_FOLDER}")
    print(f"🌐 Main site: http://localhost:5000")
    print(f"🛍️  Products page: http://localhost:5000/products")
    print(f"📡 API: http://localhost:5000/api")
    print(f"🔐 Admin login: http://localhost:5000/admin/login")
    print(f"🏥 Health check: http://localhost:5000/health")
    print("=" * 60)
    
    # Check if template folder exists
    if not os.path.exists(TEMPLATE_DIR):
        print(f"⚠️  WARNING: Template folder not found at {TEMPLATE_DIR}")
        print(f"   Please create the folder and add admin_login.html and admin_dashboard.html")
    else:
        print(f"✅ Template folder exists")
        
    # Check if frontend folder exists
    if not os.path.exists(FRONTEND_FOLDER):
        print(f"⚠️  WARNING: Frontend folder not found at {FRONTEND_FOLDER}")
    else:
        print(f"✅ Frontend folder exists")
    
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)