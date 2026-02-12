# """
# Database Initialization Script
# Run this script to create all necessary tables and insert sample data
# """

# from backend.models.db import init_database, get_db_cursor
# from backend.utils.password_hash import hash_password

# def insert_sample_products():
#     """Insert sample products"""
#     products = [
#         ('Wireless Headphones', 'Premium noise-cancelling wireless headphones with 30-hour battery life', 
#          'electronics', 79.99, 25, '🎧'),
#         ('Smart Watch', 'Fitness tracker with heart rate monitor and GPS', 
#          'electronics', 199.99, 15, '⌚'),
#         ('Running Shoes', 'Lightweight running shoes with advanced cushioning', 
#          'sports', 89.99, 30, '👟'),
#         ('Cotton T-Shirt', '100% organic cotton, comfortable and breathable', 
#          'clothing', 24.99, 50, '👕'),
#         ('Coffee Maker', 'Programmable coffee maker with thermal carafe', 
#          'home', 129.99, 12, '☕'),
#         ('Python Programming Book', 'Complete guide to Python programming for beginners', 
#          'books', 45.99, 20, '📚'),
#         ('Yoga Mat', 'Non-slip yoga mat with carrying strap', 
#          'sports', 34.99, 40, '🧘'),
#         ('Wireless Mouse', 'Ergonomic wireless mouse with precision tracking', 
#          'electronics', 29.99, 35, '🖱️'),
#         ('Denim Jeans', 'Classic fit denim jeans', 
#          'clothing', 59.99, 25, '👖'),
#         ('Backpack', 'Water-resistant backpack with laptop compartment', 
#          'accessories', 49.99, 30, '🎒'),
#         ('Bluetooth Speaker', 'Portable Bluetooth speaker with 360° sound', 
#          'electronics', 69.99, 20, '🔊'),
#         ('Sunglasses', 'UV protection sunglasses with polarized lenses', 
#          'accessories', 39.99, 45, '🕶️')
#     ]
    
#     try:
#         with get_db_cursor() as cursor:
#             cursor.executemany("""
#                 INSERT INTO products (name, description, category, price, stock, image_url)
#                 VALUES (%s, %s, %s, %s, %s, %s)
#             """, products)
#             print(f"✓ Inserted {len(products)} sample products")
#             return True
#     except Exception as e:
#         print(f"✗ Error inserting products: {e}")
#         return False

# def insert_sample_user():
#     """Insert a sample user for testing"""
#     try:
#         password_hash = hash_password('Test@1234')
        
#         with get_db_cursor() as cursor:
#             cursor.execute("""
#                 INSERT INTO users (full_name, email, mobile, password_hash, is_verified)
#                 VALUES (%s, %s, %s, %s, %s)
#             """, (
#                 'Test User',
#                 'test@example.com',
#                 '+1234567890',
#                 password_hash,
#                 True
#             ))
#             print("✓ Inserted sample user (email: test@example.com, password: Test@1234)")
#             return True
#     except Exception as e:
#         print(f"✗ Error inserting sample user: {e}")
#         return False

# def main():
#     """Main initialization function"""
#     print("=" * 50)
#     print("ShopHub E-Commerce Database Initialization")
#     print("=" * 50)
    
#     # Initialize database tables
#     print("\n1. Creating database tables...")
#     if init_database():
#         print("✓ Database tables created successfully")
#     else:
#         print("✗ Failed to create database tables")
#         return
    
#     # Insert sample products
#     print("\n2. Inserting sample products...")
#     if insert_sample_products():
#         print("✓ Sample products inserted successfully")
#     else:
#         print("✗ Failed to insert sample products")
    
#     # Insert sample user
#     print("\n3. Inserting sample user...")
#     if insert_sample_user():
#         print("✓ Sample user inserted successfully")
#     else:
#         print("✗ Failed to insert sample user")
    
#     print("\n" + "=" * 50)
#     print("Database initialization complete!")
#     print("=" * 50)
#     print("\nYou can now:")
#     print("1. Run the Flask app: python backend/app.py")
#     print("2. Login with: test@example.com / Test@1234")
#     print("3. Access API at: http://localhost:5000")
#     print("\n")

# if __name__ == "__main__":
#     main()
"""
Database Initialization Script
Run this to set up your database with sample data
"""

import mysql.connector
from backend.config import DB_CONFIG
from backend.utils.password_hash import hash_password

def init_database():
    """Initialize database with tables and sample data"""
    
    try:
        # Connect to MySQL (without database)
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
        cursor = conn.cursor()
        
        print("✅ Connected to MySQL")
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        print(f"✅ Database '{DB_CONFIG['database']}' created/selected")
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                mobile VARCHAR(20),
                password_hash VARCHAR(255) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                is_verified BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_email (email)
            )
        """)
        print("✅ Users table created")
        
        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                category VARCHAR(100) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                stock INT DEFAULT 0,
                image_url VARCHAR(500),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_category (category),
                INDEX idx_price (price)
            )
        """)
        print("✅ Products table created")
        
        # Create orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                order_number VARCHAR(50) UNIQUE NOT NULL,
                status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
                subtotal DECIMAL(10, 2) NOT NULL,
                shipping DECIMAL(10, 2) DEFAULT 0,
                tax DECIMAL(10, 2) DEFAULT 0,
                total DECIMAL(10, 2) NOT NULL,
                shipping_address JSON,
                payment_method VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_user_id (user_id),
                INDEX idx_status (status)
            )
        """)
        print("✅ Orders table created")
        
        # Create order_items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                product_id INT NOT NULL,
                product_name VARCHAR(255) NOT NULL,
                quantity INT NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                INDEX idx_order_id (order_id)
            )
        """)
        print("✅ Order items table created")
        
        # Insert sample products
        sample_products = [
            ('Wireless Headphones', 'Premium noise-cancelling wireless headphones with 30-hour battery life', 'electronics', 79.99, 25, '🎧'),
            ('Smart Watch', 'Fitness tracker with heart rate monitor and GPS', 'electronics', 199.99, 15, '⌚'),
            ('Running Shoes', 'Lightweight running shoes with advanced cushioning', 'sports', 89.99, 30, '👟'),
            ('Cotton T-Shirt', '100% organic cotton, comfortable and breathable', 'clothing', 24.99, 50, '👕'),
            ('Coffee Maker', 'Programmable coffee maker with thermal carafe', 'home', 129.99, 12, '☕'),
            ('Python Programming Book', 'Complete guide to Python programming for beginners', 'books', 45.99, 20, '📚'),
            ('Bluetooth Speaker', 'Portable waterproof speaker with 12-hour battery', 'electronics', 59.99, 18, '🔊'),
            ('Yoga Mat', 'Non-slip exercise mat with carrying strap', 'sports', 34.99, 40, '🧘'),
            ('Laptop Backpack', 'Durable backpack with padded laptop compartment', 'accessories', 49.99, 22, '🎒'),
            ('Water Bottle', 'Insulated stainless steel bottle, 32oz', 'sports', 29.99, 35, '💧'),
            ('Desk Lamp', 'LED desk lamp with adjustable brightness', 'home', 39.99, 28, '💡'),
            ('Wireless Mouse', 'Ergonomic wireless mouse with precision tracking', 'electronics', 24.99, 45, '🖱️')
        ]
        
        # Check if products exist
        cursor.execute("SELECT COUNT(*) as count FROM products")
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.executemany("""
                INSERT INTO products (name, description, category, price, stock, image_url)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, sample_products)
            conn.commit()
            print(f"✅ Inserted {len(sample_products)} sample products")
        else:
            print(f"ℹ️  Products table already has {count} products")
        
        # Create sample user
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE email = 'admin@shophub.com'")
        if cursor.fetchone()[0] == 0:
            admin_password = hash_password('Admin@123')
            cursor.execute("""
                INSERT INTO users (full_name, email, mobile, password_hash, is_verified)
                VALUES (%s, %s, %s, %s, %s)
            """, ('Admin User', 'admin@shophub.com', '+1234567890', admin_password, True))
            conn.commit()
            print("✅ Created admin user (email: admin@shophub.com, password: Admin@123)")
        else:
            print("ℹ️  Admin user already exists")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✅ Database initialization completed successfully!")
        print("="*60)
        print("\nYou can now:")
        print("1. Start the Flask server: python backend/run.py")
        print("2. Test the API: http://localhost:5000/api/products")
        print("3. Login with: admin@shophub.com / Admin@123")
        
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        print("\nPossible solutions:")
        print("1. Make sure MySQL is running")
        print("2. Check your credentials in backend/config.py")
        print("3. Verify MySQL port (default: 3306)")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Database Initialization...")
    print("="*60)
    init_database()